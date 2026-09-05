from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PaymentOut(BaseModel):
    id: Optional[int] = None
    order_id: Optional[int] = None
    razorpay_order_id: Optional[str] = Field(None, max_length=100)
    razorpay_payment_id: Optional[str] = Field(None, max_length=100)
    amount: Optional[float] = Field(0.0, ge=0)
    currency: Optional[str] = Field("INR", max_length=10)
    status: Optional[str] = Field("pending", max_length=50)
    signature_verified: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create/update payment
class PaymentIn(PaymentOut):
    pass


# Request Schema to verify Razorpay payment signature
class RazorpayVerifyIn(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    order_id: Optional[int] = None
