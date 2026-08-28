import os
from pathlib import Path
import requests
from fastapi import UploadFile, HTTPException, status

from app.core.config import REMOTE_UPLOAD_API_URL, REMOTE_UPLOAD_BASE_URL

# Reference extensions allowed by PHP script (C:\xampp\htdocs\file_upload_api\upload.php)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "pdf", "docx", "txt", "zip", "csv"}
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def upload_file_to_php_api(
    file: UploadFile,
    directory: str = "products",
    api_url: str = REMOTE_UPLOAD_API_URL,
    base_url: str = REMOTE_UPLOAD_BASE_URL,
) -> dict:
    """
    Uploads a single file to the remote PHP upload API (https://apiapp.hotelmahalaiims.com/uploads.php)
    based on the reference C:\\xampp\\htdocs\\file_upload_api\\upload.php.

    :param file: FastAPI UploadFile object
    :param directory: Destination directory name ($_POST['directory'] in PHP)
    :param api_url: Remote Core PHP API endpoint
    :param base_url: Base URL to construct absolute file URLs
    :return: Formatted response dict containing file_url, relative_url, saved_name, size, etc.
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
            detail=f"Extension '{file_ext}' is not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    try:
        # Reset file cursor before reading
        file.file.seek(0)

        # Multipart form payload matching PHP $_FILES and $_POST
        files = {
            "file": (
                file.filename,
                file.file,
                file.content_type or "application/octet-stream"
            )
        }
        data = {
            "directory": directory or "general"
        }

        # Send POST request to the remote PHP endpoint
        response = requests.post(
            api_url,
            files=files,
            data=data,
            timeout=30
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Remote upload API returned status {response.status_code}: {response.text}",
            )

        result = response.json()

        if result.get("status") != "success":
            failed_info = result.get("failed_files", [])
            error_msg = result.get("message")
            if failed_info and len(failed_info) > 0:
                error_msg = failed_info[0].get("error", error_msg)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Upload failed: {error_msg or 'Unknown error from upload service'}",
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
    files: list[UploadFile],
    directory: str = "products",
    api_url: str = REMOTE_UPLOAD_API_URL,
    base_url: str = REMOTE_UPLOAD_BASE_URL,
) -> dict:
    """
    Uploads multiple files in batch to the remote PHP upload API matching $_FILES['files'].
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No files provided for upload.",
        )

    for f in files:
        if not f.filename:
            continue
        ext = Path(f.filename).suffix.lstrip(".").lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File '{f.filename}' has unsupported extension '{ext}'.",
            )

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
                        f.content_type or "application/octet-stream"
                    )
                )
            )

        data = {"directory": directory or "general"}

        response = requests.post(
            api_url,
            files=files_payload,
            data=data,
            timeout=60
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Remote upload API returned status {response.status_code}: {response.text}",
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
            "directory": result.get("directory"),
            "uploaded_files": uploaded_list,
            "failed_files": result.get("failed_files", []),
            "count": len(uploaded_list),
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to connect to remote upload server: {str(e)}",
        )
