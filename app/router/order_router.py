from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user, get_optional_current_user
from app.schemas.order import OrderIn, OrderOut
from app.controller.order_controller import OrderController

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
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
def get_all_orders(
    user_id: int | None = None,
    status: str | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return OrderController.get_all_orders(
        db=db,
        user_id=user_id,
        status=status,
        search=search,
        page=page,
        limit=limit
    )


@router.get("/my-orders", response_model=list[OrderOut], status_code=200)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = _extract_user_id(current_user)
    return OrderController.get_user_orders(db, user_id=user_id)


@router.get("/number/{order_number}", response_model=OrderOut, status_code=200)
def get_order_by_number(
    order_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return OrderController.get_order_by_number(db, order_number)


@router.get("/{order_id}", response_model=OrderOut, status_code=200)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return OrderController.get_order_by_id(db, order_id)


@router.post("/create", response_model=OrderOut, status_code=201)
def create_order(
    request: OrderIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user)
):
    user_id = _extract_user_id(current_user)
    return OrderController.create_order(db, request, current_user_id=user_id)


@router.put("/{order_id}", response_model=OrderOut, status_code=200)
def update_order(
    order_id: int,
    request: OrderIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return OrderController.update_order(db, order_id, request)


@router.delete("/{order_id}", status_code=200)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return OrderController.delete_order(db, order_id)
