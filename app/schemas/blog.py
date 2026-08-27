from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BlogOut(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    author_id: Optional[int] = None

    title: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    excerpt: Optional[str] = None
    content: Optional[str] = None

    featured_image: Optional[str] = Field(None, max_length=500)

    status: Optional[int] = 1
    published_at: Optional[datetime] = None

    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = None
    canonical_url: Optional[str] = Field(None, max_length=500)
    og_title: Optional[str] = Field(None, max_length=255)
    og_description: Optional[str] = None
    og_image: Optional[str] = Field(None, max_length=500)

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create/update blog
class BlogIn(BlogOut):
    pass
