import hmac
import hashlib
from typing import Optional, Dict, Any
import razorpay
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from app.models.order import Order
from app.repositories.order_repository import OrderRepository

razorpay_client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID or "", RAZORPAY_KEY_SECRET or "")
)


class RazorpayService:

    client = razorpay_client

    @staticmethod
    def create_order(
        amount: int,
        currency: str = "INR",
        receipt: Optional[str] = None,
        notes: Optional[Dict[str, Any]] = None,
    ):
        data: Dict[str, Any] = {
            "amount": int(amount),
            "currency": currency,
        }
        if receipt:
            data["receipt"] = receipt
        if notes:
            data["notes"] = notes

        return razorpay_client.order.create(data=data)

    @staticmethod
    def RazorpayOrder(
        db: Session,
        order: Optional[Order] = None,
        order_id: Optional[int] = None,
    ) -> Order:
        if order is None and order_id is not None:
            order = OrderRepository.get_by_id(db, order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

        if not order:
            raise HTTPException(status_code=400, detail="Order instance or order_id is required")

        if order.amount and order.amount > 0 and not order.razorpay_order_id:
            try:
                amount_in_paise = int(round(float(order.amount) * 100))
                currency = order.currency or "INR"
                rzp_order = RazorpayService.create_order(
                    amount=amount_in_paise,
                    currency=currency,
                    receipt=order.order_number,
                    notes={
                        "order_number": order.order_number,
                        "order_id": str(order.id),
                        "user_id": str(order.user_id),
                    },
                )
                if rzp_order and "id" in rzp_order:
                    order = OrderRepository.update(db, order, {"razorpay_order_id": rzp_order["id"]})
            except Exception as e:
                print(f"Warning: Could not create Razorpay order: {e}")

        return order

    create_razorpay_order = RazorpayOrder

    @staticmethod
    def verify_signature(
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ) -> bool:
        if not RAZORPAY_KEY_SECRET:
            raise HTTPException(
                status_code=500,
                detail="RAZORPAY_KEY_SECRET is not configured on the server"
            )

        try:
            razorpay_client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )
            return True
        except Exception:
            body_to_sign = f"{razorpay_order_id}|{razorpay_payment_id}"
            expected_signature = hmac.new(
                RAZORPAY_KEY_SECRET.encode("utf-8"),
                body_to_sign.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, razorpay_signature):
                raise HTTPException(
                    status_code=400,
                    detail="Razorpay payment signature verification failed"
                )
            return True

    verify_payment = verify_signature

    @staticmethod
    def get_payment(payment_id: str):
        return razorpay_client.payment.fetch(payment_id)

    @staticmethod
    def get_order(order_id: str):
        return razorpay_client.order.fetch(order_id)
