import razorpay
from typing import Optional, Dict, Any
from app.core.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

razorpay_client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID or "", RAZORPAY_KEY_SECRET or "")
)


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


def verify_payment(
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
):
    return razorpay_client.utility.verify_payment_signature(
        {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }
    )


def get_payment(payment_id: str):
    return razorpay_client.payment.fetch(
        payment_id
    )


def get_order(order_id: str):
    return razorpay_client.order.fetch(
        order_id
    )


class RazorpayService:

    @staticmethod
    def create_order(
        amount: int,
        currency: str = "INR",
        receipt: Optional[str] = None,
        notes: Optional[Dict[str, Any]] = None,
    ):
        return create_order(
            amount=amount,
            currency=currency,
            receipt=receipt,
            notes=notes,
        )

    @staticmethod
    def verify_payment(
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ):
        return verify_payment(
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
        )

    @staticmethod
    def get_payment(payment_id: str):
        return get_payment(payment_id)

    @staticmethod
    def get_order(order_id: str):
        return get_order(order_id)
