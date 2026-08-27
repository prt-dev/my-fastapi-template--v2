from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ClientOut(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=255)
    website_name: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=500)
    domain: Optional[str] = Field(None, max_length=255)
    logo: Optional[str] = Field(None, max_length=500)
    default_meta_title: Optional[str] = Field(None, max_length=255)
    default_meta_description: Optional[str] = None
    status: Optional[int] = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create/update client
class ClientIn(ClientOut):
    pass
