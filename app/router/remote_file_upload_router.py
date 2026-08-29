from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status

from app.core.dependency import get_current_user
from app.utils.remote_file_upload import (
    upload_file_to_php_api,
    upload_multiple_files_to_php_api,
)

router = APIRouter(
    prefix="/remote-upload",
    tags=["Remote File Upload"],
)


@router.post("/file", status_code=status.HTTP_201_CREATED)
@router.post("/image", status_code=status.HTTP_201_CREATED)
def upload_single_remote_file(
    file: UploadFile = File(..., description="File to upload"),
    directory: Optional[str] = Form(None, description="Subdirectory under uploads/ (e.g. products, categories, blogs)"),
    folder: Optional[str] = Form(None, description="Alias for directory via Form data"),
    dir_query: Optional[str] = Query(None, alias="directory", description="Subdirectory via Query parameter"),
    folder_query: Optional[str] = Query(None, alias="folder", description="Alias for directory via Query parameter"),
    current_user=Depends(get_current_user),
):
    """
    Upload a single file/image to the remote PHP upload service (upload.php).
    Accepts directory via either Form data or Query parameter (defaults to 'products').
    """
    target_dir = directory or folder or dir_query or folder_query or "products"
    return upload_file_to_php_api(file=file, directory=target_dir)


@router.post("/files", status_code=status.HTTP_201_CREATED)
@router.post("/images", status_code=status.HTTP_201_CREATED)
def upload_multiple_remote_files(
    files: List[UploadFile] = File(..., description="Multiple files to upload"),
    directory: Optional[str] = Form(None, description="Subdirectory under uploads/ (e.g. products, categories, blogs)"),
    folder: Optional[str] = Form(None, description="Alias for directory via Form data"),
    dir_query: Optional[str] = Query(None, alias="directory", description="Subdirectory via Query parameter"),
    folder_query: Optional[str] = Query(None, alias="folder", description="Alias for directory via Query parameter"),
    current_user=Depends(get_current_user),
):
    """
    Upload multiple files/images to the remote PHP upload service (upload.php).
    Accepts directory via either Form data or Query parameter (defaults to 'products').
    """
    target_dir = directory or folder or dir_query or folder_query or "products"
    return upload_multiple_files_to_php_api(files=files, directory=target_dir)
