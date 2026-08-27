from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    role_id: Mapped[int] = mapped_column(Integer, nullable=False)
    permission_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Code-level relationships (No DB-level foreign key constraints)
    role: Mapped["Role"] = relationship(
        "Role",
        primaryjoin="foreign(RolePermission.role_id) == Role.id",
        back_populates="role_permissions",
    )

    permission: Mapped["Permission"] = relationship(
        "Permission",
        primaryjoin="foreign(RolePermission.permission_id) == Permission.id",
        back_populates="role_permissions",
    )
