import os
from pathlib import Path
from typing import List, Optional
import requests
from fastapi import UploadFile, HTTPException, status

from app.core.config import REMOTE_UPLOAD_API_URL, REMOTE_UPLOAD_BASE_URL

# Config matched to PHP script (C:\xampp\htdocs\file_upload_api\upload.php)
# Allowed extensions: ['jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf', 'docx', 'txt', 'zip', 'csv']
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "pdf", "docx", "txt", "zip", "csv"}
# Maximum file size: 10 MB (10 * 1024 * 1024 bytes)
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def sanitize_directory(directory: Optional[str]) -> str:
    """
    Sanitize directory name to prevent path traversal, matching upload.php logic:
    trim(str_replace(['../', '..\\'], '', $requestedDirectory), '/\\')
    """
    if not directory:
        return "general"
    clean_dir = str(directory).replace("../", "").replace("..\\", "").strip("/\\ ")
    return clean_dir if clean_dir else "general"


def validate_file(file: UploadFile) -> str:
    """
    Validate filename, extension, and file size before sending to PHP upload API.
    Returns the lowercased file extension.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have a valid filename.",
        )

    file_ext = Path(file.filename).suffix.lstrip(".").lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extension '{file_ext}' is not allowed for file '{file.filename}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # Check file size if seekable
    try:
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)
        if size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File '{file.filename}' size ({size / (1024*1024):.2f} MB) exceeds limit of {MAX_FILE_SIZE_MB} MB.",
            )
    except (AttributeError, io.UnsupportedOperation):
        pass

    return file_ext


def upload_file_to_php_api(
    file: UploadFile,
    directory: str = "products",
    api_url: str = REMOTE_UPLOAD_API_URL,
    base_url: str = REMOTE_UPLOAD_BASE_URL,
) -> dict:
    """
    Upload a single file to PHP upload API (upload.php).
    Matches upload.php expectations:
      - $_POST['directory']
      - $_FILES['file']
      - Response with status, directory, uploaded_files, and failed_files
    """
    file_ext = validate_file(file)
    clean_dir = sanitize_directory(directory)

    try:
        file.file.seek(0)

        files = {
            "file": (
                file.filename,
                file.file,
                file.content_type or "application/octet-stream",
            )
        }
        data = {
            "directory": clean_dir
        }

        response = requests.post(
            api_url,
            files=files,
            data=data,
            timeout=30,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Remote upload API returned HTTP {response.status_code}: {response.text}",
            )

        result = response.json()

        if result.get("status") != "success":
            failed_info = result.get("failed_files", [])
            error_msg = result.get("message")
            if failed_info and len(failed_info) > 0:
                error_msg = failed_info[0].get("error", error_msg)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Remote upload failed: {error_msg or 'Unknown error from upload service'}",
            )

        uploaded_files = result.get("uploaded_files", [])
        if not uploaded_files:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Upload succeeded but no uploaded file details were returned.",
            )

        item = uploaded_files[0]
        raw_file_path = item.get("file_path", "").lstrip("/")
        clean_base_url = base_url.rstrip("/")

        full_url = f"{clean_base_url}/{raw_file_path}"
        relative_url = f"/{raw_file_path}"

        return {
            "status": "success",
            "directory": result.get("directory", f"uploads/{clean_dir}"),
            "image_url": full_url,
            "file_url": full_url,
            "relative_url": relative_url,
            "original_name": item.get("original_name", file.filename),
            "saved_name": item.get("saved_name"),
            "file_path": raw_file_path,
            "extension": item.get("extension", file_ext),
            "size": item.get("size", 0),
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to connect to remote upload server: {str(e)}",
        )


def upload_multiple_files_to_php_api(
    files: List[UploadFile],
    directory: str = "products",
    api_url: str = REMOTE_UPLOAD_API_URL,
    base_url: str = REMOTE_UPLOAD_BASE_URL,
) -> dict:
    """
    Upload multiple files to PHP upload API (upload.php).
    Sends multipart array 'files[]' and $_POST['directory'].
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided for upload.",
        )

    for f in files:
        validate_file(f)

    clean_dir = sanitize_directory(directory)

    try:
        files_payload = []
        for f in files:
            f.file.seek(0)
            files_payload.append(
                (
                    "files[]",
                    (
                        f.filename,
                        f.file,
                        f.content_type or "application/octet-stream",
                    ),
                )
            )

        data = {"directory": clean_dir}

        response = requests.post(
            api_url,
            files=files_payload,
            data=data,
            timeout=60,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Remote upload API returned HTTP {response.status_code}: {response.text}",
            )

        result = response.json()
        clean_base_url = base_url.rstrip("/")

        uploaded_list = []
        for item in result.get("uploaded_files", []):
            raw_path = item.get("file_path", "").lstrip("/")
            full_url = f"{clean_base_url}/{raw_path}"
            uploaded_list.append({
                "image_url": full_url,
                "file_url": full_url,
                "relative_url": f"/{raw_path}",
                "original_name": item.get("original_name"),
                "saved_name": item.get("saved_name"),
                "file_path": raw_path,
                "extension": item.get("extension"),
                "size": item.get("size"),
            })

        return {
            "status": result.get("status", "success"),
            "directory": result.get("directory", f"uploads/{clean_dir}"),
            "uploaded_files": uploaded_list,
            "failed_files": result.get("failed_files", []),
            "count": len(uploaded_list),
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to connect to remote upload server: {str(e)}",
        )
