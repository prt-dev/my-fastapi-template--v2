from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_optional_current_user
from app.schemas.order import OrderIn, OrderOut
from app.schemas.payment import PaymentOut
from app.schemas.razorpay import RazorpayVerifyIn
from app.controller.razorpay_controller import RazorpayController

router = APIRouter(
    tags=["Razorpay"]
)


def _extract_user_id(current_user) -> int | None:
    if isinstance(current_user, dict):
        user_id = current_user.get("sub") or current_user.get("id")
    elif hasattr(current_user, "id"):
        user_id = current_user.id
    else:
        user_id = None
    return int(user_id) if user_id is not None else None


@router.post("/razorpay/create-order", response_model=OrderOut, status_code=201)
@router.post("/orders/create-razorpay-order", response_model=OrderOut, status_code=201)
def create_razorpay_order(
    request: OrderIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user)
):
    user_id = _extract_user_id(current_user)
    return RazorpayController.create_razorpay_order(db, request, current_user_id=user_id)


@router.post("/razorpay/verify", response_model=PaymentOut, status_code=200)
@router.post("/payments/verify", response_model=PaymentOut, status_code=200)
def verify_razorpay_payment(
    request: RazorpayVerifyIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user)
):
    return RazorpayController.verify_razorpay_payment(db, request)
