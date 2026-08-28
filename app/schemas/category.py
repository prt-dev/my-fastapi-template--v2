from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CategoryOut(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None
    status: Optional[int] = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create/update category
class CategoryIn(CategoryOut):
    pass
