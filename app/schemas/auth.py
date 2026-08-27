from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import Field


class LoginRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=4, max_length=100)
    email: EmailStr
    password: str