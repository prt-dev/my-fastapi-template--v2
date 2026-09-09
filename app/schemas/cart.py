from typing import Optional, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator

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
    status: Optional[Union[int, str]] = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user: Optional[UserOut] = None
    product: Optional[ProductOut] = None

    @field_validator("status", mode="before")
    @classmethod
    def parse_status(cls, v):
        if v is None:
            return v
        if isinstance(v, (int, float)):
            return int(v)
        if isinstance(v, str):
            if v.isdigit() or (v.startswith('-') and v[1:].isdigit()):
                return int(v)
            return v
        return v

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
    status: Optional[Union[int, str]] = 1


# Request Schema to update cart
class CartUpdate(BaseModel):
    user_id: Optional[int] = None
    products: Optional[Union[str, Any]] = None
    product_id: Optional[int] = None
    variant: Optional[str] = Field(None, max_length=255)
    quantity: Optional[int] = None
    price: Optional[float] = None
    status: Optional[Union[int, str]] = None
