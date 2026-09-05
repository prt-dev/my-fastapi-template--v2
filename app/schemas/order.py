from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserOut
from app.schemas.payment import PaymentOut


class OrderOut(BaseModel):
    id: Optional[int] = None
    order_number: Optional[str] = Field(None, max_length=100)
    user_id: Optional[int] = None
    amount: Optional[float] = Field(0.0, ge=0)
    currency: Optional[str] = Field("INR", max_length=10)
    status: Optional[str] = Field("pending", max_length=50)
    razorpay_order_id: Optional[str] = Field(None, max_length=100)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user: Optional[UserOut] = None
    payments: Optional[List[PaymentOut]] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create/update order
class OrderIn(OrderOut):
    phone: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None

