from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class ProductPermissions:
    """Predefined permission names for product module."""
    CREATE = "products:create"
    READ = "products:read"
    UPDATE = "products:update"
    DELETE = "products:delete"
    LIST = "products:list"


class ClientPermissions:
    """Predefined permission names for client module."""
    CREATE = "clients:create"
    READ = "clients:read"
    UPDATE = "clients:update"
    DELETE = "clients:delete"
    LIST = "clients:list"


class BlogPermissions:
    """Predefined permission names for blog module."""
    CREATE = "blogs:create"
    READ = "blogs:read"
    UPDATE = "blogs:update"
    DELETE = "blogs:delete"
    LIST = "blogs:list"


class CartPermissions:
    """Predefined permission names for cart module."""
    CREATE = "carts:create"
    READ = "carts:read"
    UPDATE = "carts:update"
    DELETE = "carts:delete"
    LIST = "carts:list"


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    module: Mapped[str] = mapped_column(
        String(100),
        default="products",
        nullable=False,
    )
    status: Mapped[int] = mapped_column(Integer, default=1)

    # Code-level relationships (No DB-level foreign key constraints)
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permissions",
        primaryjoin="Permission.id == foreign(RolePermission.permission_id)",
        secondaryjoin="foreign(RolePermission.role_id) == Role.id",
        viewonly=True,
    )

    role_permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        primaryjoin="foreign(RolePermission.permission_id) == Permission.id",
        back_populates="permission",
        cascade="all, delete-orphan",
    )
