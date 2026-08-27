from fastapi import APIRouter, Depends, File, UploadFile, Query, status
from app.core.dependency import get_current_user
from app.utils.file_upload import save_upload_image

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/image", status_code=status.HTTP_201_CREATED)
def upload_single_image(
    file: UploadFile = File(...),
    folder: str = Query("products", description="Subfolder within uploads directory"),
    current_user=Depends(get_current_user),
):
    result = save_upload_image(file=file, folder=folder)
    return result


@router.post("/images", status_code=status.HTTP_201_CREATED)
def upload_multiple_images(
    files: list[UploadFile] = File(...),
    folder: str = Query("products", description="Subfolder within uploads directory"),
    current_user=Depends(get_current_user),
):
    """
    Upload multiple image files.
    """
    results = [save_upload_image(file=f, folder=folder) for f in files]
    return {
        "images": results,
        "count": len(results),
    }
