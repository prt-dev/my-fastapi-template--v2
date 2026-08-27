from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProductOut(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    sku: Optional[str] = Field(None, max_length=100)
    stock_quantity: Optional[int] = Field(0, ge=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = Field(None, max_length=500)
    status: Optional[int] = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create/update product
class ProductIn(ProductOut):
    pass
