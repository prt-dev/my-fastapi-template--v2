from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserOut(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    firstname: Optional[str] = Field(None, max_length=100)
    lastname: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=4, max_length=100)
    role_id: Optional[int] = None
    status: Optional[int] = 1
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# Request Schema to create user
class UserIn(UserOut):
    password: Optional[str] = Field(None, min_length=6, max_length=72)




