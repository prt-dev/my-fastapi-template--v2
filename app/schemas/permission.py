from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    name: str
    description: str | None = None
    module: str = "products"
    status: int = 1


class PermissionIn(PermissionBase):
    pass


class PermissionOut(PermissionBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class RolePermissionOut(BaseModel):
    id: int
    role_id: int
    permission_id: int
    permission: PermissionOut | None = None

    model_config = ConfigDict(from_attributes=True)
