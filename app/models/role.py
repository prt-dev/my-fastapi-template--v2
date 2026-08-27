from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    role_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=1)

    # Code-level relationships (No DB-level foreign key constraints)
    users: Mapped[list["Userdata"]] = relationship(
        "Userdata",
        primaryjoin="foreign(Userdata.role_id) == Role.id",
        back_populates="role",
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        primaryjoin="foreign(RolePermission.role_id) == Role.id",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary="role_permissions",
        primaryjoin="Role.id == foreign(RolePermission.role_id)",
        secondaryjoin="foreign(RolePermission.permission_id) == Permission.id",
        viewonly=True,
    )