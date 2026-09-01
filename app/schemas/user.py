from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserOut(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Field(None, max_length=100)
    firstname: Optional[str] = Field(None, max_length=100)
    lastname: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=10)
    username: Optional[str] = Field(None, min_length=4, max_length=100)
    role_id: Optional[int] = None
    status: Optional[int] = 1

    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )


# Request Schema to create/update user
class UserIn(UserOut):
    password: Optional[str] = Field(None, min_length=6, max_length=72)






