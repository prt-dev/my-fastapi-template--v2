from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user
from app.schemas.cart import CartIn, CartOut
from app.controller.cart_controller import CartController

router = APIRouter(
    prefix="/carts",
    tags=["Carts"]
)


def _extract_user_id(current_user) -> int | None:
    if isinstance(current_user, dict):
        user_id = current_user.get("sub") or current_user.get("id")
    elif hasattr(current_user, "id"):
        user_id = current_user.id
    else:
        user_id = None
    return int(user_id) if user_id is not None else None


@router.get("/all", status_code=200)
def get_all_carts(
    user_id: int | None = None,
    product_id: int | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CartController.get_all_cart_items(
        db=db,
        user_id=user_id,
        product_id=product_id,
        search=search,
        page=page,
        limit=limit
    )


@router.get("/my-cart", status_code=200)
def get_my_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = _extract_user_id(current_user)
    return CartController.get_user_cart(db, user_id=user_id)


@router.get("/{cart_id}", response_model=CartOut, status_code=200)
def get_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CartController.get_cart_by_id(db, cart_id)


@router.post("/create", response_model=CartOut, status_code=201)
def create_cart_item(
    request: CartIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = _extract_user_id(current_user)
    return CartController.create_cart_item(db, request, current_user_id=user_id)


@router.put("/{cart_id}", response_model=CartOut, status_code=200)
def update_cart_item(
    cart_id: int,
    request: CartIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = _extract_user_id(current_user)
    return CartController.update_cart_item(db, cart_id, request, current_user_id=user_id)


@router.delete("/clear", status_code=200)
def clear_my_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = _extract_user_id(current_user)
    return CartController.clear_user_cart(db, user_id=user_id)


@router.delete("/{cart_id}", status_code=200)
def delete_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = _extract_user_id(current_user)
    return CartController.delete_cart_item(db, cart_id, current_user_id=user_id)
