from typing import Optional, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserOut
from app.schemas.product import ProductOut


class CartOut(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    products: Optional[Union[str, Any]] = None
    product_id: Optional[int] = None
    variant: Optional[str] = Field(None, max_length=255)
    quantity: Optional[int] = None
    price: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user: Optional[UserOut] = None
    product: Optional[ProductOut] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create cart
class CartIn(BaseModel):
    user_id: Optional[int] = None
    products: Union[str, Any]
    product_id: Optional[int] = None
    variant: Optional[str] = Field(None, max_length=255)
    quantity: Optional[int] = None
    price: Optional[float] = None


# Request Schema to update cart
class CartUpdate(BaseModel):
    user_id: Optional[int] = None
    products: Optional[Union[str, Any]] = None
    product_id: Optional[int] = None
    variant: Optional[str] = Field(None, max_length=255)
    quantity: Optional[int] = None
    price: Optional[float] = None
