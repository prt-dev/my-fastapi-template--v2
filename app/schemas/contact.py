from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.client import ClientOut


class ContactOut(BaseModel):
    id: Optional[int] = None
    client_id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    subject: Optional[str] = Field(None, max_length=255)
    message: Optional[str] = None
    status: Optional[int] = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    client: Optional[ClientOut] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create/update contact
class ContactIn(ContactOut):
    pass
