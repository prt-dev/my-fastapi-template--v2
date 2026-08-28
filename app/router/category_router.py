from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user
from app.schemas.category import CategoryIn, CategoryOut
from app.controller.category_controller import CategoryController

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/all", status_code=200)
def get_all_categories(
    parent_id: int | None = None,
    search: str | None = None,
    status: int | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CategoryController.get_all_categories(
        db=db,
        parent_id=parent_id,
        search=search,
        status=status,
        page=page,
        limit=limit
    )


@router.get("/slug/{slug}", response_model=CategoryOut, status_code=200)
def get_category_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CategoryController.get_category_by_slug(db, slug)


@router.get("/{category_id}", response_model=CategoryOut, status_code=200)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CategoryController.get_category_by_id(db, category_id)


@router.post("/create", response_model=CategoryOut, status_code=201)
def create_category(
    request: CategoryIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CategoryController.create_category(db, request)


@router.put("/{category_id}", response_model=CategoryOut, status_code=200)
def update_category(
    category_id: int,
    request: CategoryIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CategoryController.update_category(db, category_id, request)


@router.delete("/{category_id}", status_code=200)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CategoryController.delete_category(db, category_id)
