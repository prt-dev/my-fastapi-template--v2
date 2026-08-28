from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserOut
from app.schemas.product import ProductOut


class CartOut(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    variant: Optional[str] = Field(None, max_length=255)
    quantity: Optional[int] = Field(1, ge=1)
    price: Optional[float] = Field(0.0, ge=0)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user: Optional[UserOut] = None
    product: Optional[ProductOut] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create/update cart
class CartIn(CartOut):
    pass

