from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user
from app.schemas.payment import PaymentIn, PaymentOut, RazorpayVerifyIn
from app.controller.payment_controller import PaymentController

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.get("/all", status_code=200)
def get_all_payments(
    order_id: int | None = None,
    status: str | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PaymentController.get_all_payments(
        db=db,
        order_id=order_id,
        status=status,
        search=search,
        page=page,
        limit=limit
    )


@router.get("/order/{order_id}", response_model=list[PaymentOut], status_code=200)
def get_payments_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PaymentController.get_payments_by_order_id(db, order_id)


@router.get("/{payment_id}", response_model=PaymentOut, status_code=200)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PaymentController.get_payment_by_id(db, payment_id)


@router.post("/create", response_model=PaymentOut, status_code=201)
def create_payment(
    request: PaymentIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PaymentController.create_payment(db, request)


@router.post("/verify", response_model=PaymentOut, status_code=200)
def verify_razorpay_payment(
    request: RazorpayVerifyIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PaymentController.verify_razorpay_payment(db, request)


@router.put("/{payment_id}", response_model=PaymentOut, status_code=200)
def update_payment(
    payment_id: int,
    request: PaymentIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PaymentController.update_payment(db, payment_id, request)


@router.delete("/{payment_id}", status_code=200)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PaymentController.delete_payment(db, payment_id)
