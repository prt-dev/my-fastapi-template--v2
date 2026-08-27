

import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

BASE_UPLOAD_DIR = Path("uploads")
# BASE_UPLOAD_DIR = Path("app/uploads")


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
}
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def save_upload_image(file: UploadFile, folder: str = None) -> dict:
    
    if not file.content_type or file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Allowed types: JPEG, PNG, WEBP, GIF, SVG.",
        )

    ext = ALLOWED_IMAGE_TYPES.get(file.content_type)
    if not ext and file.filename:
        suffix = Path(file.filename).suffix.lower()
        if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}:
            ext = suffix

    if not ext:
        ext = ".jpg"

    # Create destination folder (e.g. uploads/products)
    target_dir = BASE_UPLOAD_DIR / folder
    target_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    destination_path = target_dir / unique_filename

    # Read and save file with size check
    file_size = 0
    with destination_path.open("wb") as buffer:
        while chunk := file.file.read(1024 * 1024):  # Read in 1MB chunks
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE_BYTES:
                buffer.close()
                if destination_path.exists():
                    destination_path.unlink()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB.",
                )
            buffer.write(chunk)

    relative_url = f"/uploads/{folder}/{unique_filename}"

    return {
        "image_url": relative_url,
        "filename": unique_filename,
        "original_name": file.filename,
        "content_type": file.content_type,
        "size": file_size,
    }


def delete_upload_file(file_url: str | None) -> bool:
    """
    Deletes an uploaded file given its relative URL (e.g. /uploads/products/xyz.jpg).
    """
    if not file_url or not file_url.startswith("/uploads/"):
        return False

    relative_path = file_url.lstrip("/")
    file_path = Path(relative_path)

    # Prevent directory traversal
    try:
        resolved = file_path.resolve()
        if not str(resolved).startswith(str(BASE_UPLOAD_DIR.resolve())):
            return False
    except Exception:
        return False

    if file_path.exists() and file_path.is_file():
        try:
            file_path.unlink()
            return True
        except OSError:
            return False

    return False
