from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user
from app.schemas.product import ProductIn, ProductOut
from app.controller.product_controller import ProductController

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# router = APIRouter(
#     prefix="/admin/products",
#     tags=["Admin Products"],
#     dependencies=[Depends(require_admin)],

@router.get("/all", status_code=200)
def get_all_products(
    category_id: int | None = None,
    search: str | None = None,
    status: int | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ProductController.get_all_products(
        db=db,
        category_id=category_id,
        search=search,
        status=status,
        page=page,
        limit=limit
    )


@router.get("/{product_id}", response_model=ProductOut, status_code=200)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ProductController.get_product_by_id(db, product_id)


@router.post("/create", response_model=ProductOut, status_code=201)
def create_product(
    request: ProductIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ProductController.create_product(db, request)


@router.put("/{product_id}", response_model=ProductOut, status_code=200)
def update_product(
    product_id: int,
    request: ProductIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ProductController.update_product(db, product_id, request)


@router.delete("/{product_id}", status_code=200)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ProductController.delete_product(db, product_id)
