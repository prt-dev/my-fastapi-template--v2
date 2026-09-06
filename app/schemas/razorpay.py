from typing import Optional
from pydantic import BaseModel


class RazorpayVerifyIn(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    order_id: Optional[int] = None
