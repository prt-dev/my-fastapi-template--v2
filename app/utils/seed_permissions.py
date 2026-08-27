from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.permission import (
    Permission,
    ProductPermissions,
    ClientPermissions,
    BlogPermissions,
    CartPermissions,
)
from app.models.role import Role
from app.models.role_permission import RolePermission

DEFAULT_PRODUCT_PERMISSIONS = [
    {
        "name": ProductPermissions.CREATE,
        "description": "Permission to create a new product",
        "module": "products",
    },
    {
        "name": ProductPermissions.READ,
        "description": "Permission to view product details",
        "module": "products",
    },
    {
        "name": ProductPermissions.UPDATE,
        "description": "Permission to update existing product",
        "module": "products",
    },
    {
        "name": ProductPermissions.DELETE,
        "description": "Permission to delete a product",
        "module": "products",
    },
    {
        "name": ProductPermissions.LIST,
        "description": "Permission to view all products list",
        "module": "products",
    },
]

DEFAULT_CLIENT_PERMISSIONS = [
    {
        "name": ClientPermissions.CREATE,
        "description": "Permission to create a new client",
        "module": "clients",
    },
    {
        "name": ClientPermissions.READ,
        "description": "Permission to view client details",
        "module": "clients",
    },
    {
        "name": ClientPermissions.UPDATE,
        "description": "Permission to update existing client",
        "module": "clients",
    },
    {
        "name": ClientPermissions.DELETE,
        "description": "Permission to delete a client",
        "module": "clients",
    },
    {
        "name": ClientPermissions.LIST,
        "description": "Permission to view all clients list",
        "module": "clients",
    },
]

DEFAULT_BLOG_PERMISSIONS = [
    {
        "name": BlogPermissions.CREATE,
        "description": "Permission to create a new blog",
        "module": "blogs",
    },
    {
        "name": BlogPermissions.READ,
        "description": "Permission to view blog details",
        "module": "blogs",
    },
    {
        "name": BlogPermissions.UPDATE,
        "description": "Permission to update existing blog",
        "module": "blogs",
    },
    {
        "name": BlogPermissions.DELETE,
        "description": "Permission to delete a blog",
        "module": "blogs",
    },
    {
        "name": BlogPermissions.LIST,
        "description": "Permission to view all blogs list",
        "module": "blogs",
    },
]

DEFAULT_CART_PERMISSIONS = [
    {
        "name": CartPermissions.CREATE,
        "description": "Permission to add item to cart",
        "module": "carts",
    },
    {
        "name": CartPermissions.READ,
        "description": "Permission to view cart item details",
        "module": "carts",
    },
    {
        "name": CartPermissions.UPDATE,
        "description": "Permission to update cart item",
        "module": "carts",
    },
    {
        "name": CartPermissions.DELETE,
        "description": "Permission to delete item from cart",
        "module": "carts",
    },
    {
        "name": CartPermissions.LIST,
        "description": "Permission to view all cart items list",
        "module": "carts",
    },
]


def _seed_permissions_list(db: Session, permissions_list: list[dict], module_name: str):
    created_permissions = []
    for perm_data in permissions_list:
        existing = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not existing:
            perm = Permission(
                name=perm_data["name"],
                description=perm_data["description"],
                module=perm_data["module"],
                status=1,
            )
            db.add(perm)
            created_permissions.append(perm)
        else:
            created_permissions.append(existing)

    db.commit()

    # Check or create Admin role (id=1)
    admin_role = db.query(Role).filter(Role.id == 1).first()
    if not admin_role:
        admin_role = Role(id=1, role_name="Admin", status=1)
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # Assign permissions to Admin role if not already assigned
    for perm in created_permissions:
        existing_rp = db.query(RolePermission).filter(
            RolePermission.role_id == admin_role.id,
            RolePermission.permission_id == perm.id,
        ).first()
        if not existing_rp:
            rp = RolePermission(
                role_id=admin_role.id,
                permission_id=perm.id,
            )
            db.add(rp)

    db.commit()
    print(f"{module_name.capitalize()} permissions seeded successfully ({len(permissions_list)} permissions).")


def seed_product_permissions(db: Session | None = None):
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True
    try:
        _seed_permissions_list(db, DEFAULT_PRODUCT_PERMISSIONS, "product")
    finally:
        if should_close:
            db.close()


def seed_client_permissions(db: Session | None = None):
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True
    try:
        _seed_permissions_list(db, DEFAULT_CLIENT_PERMISSIONS, "client")
    finally:
        if should_close:
            db.close()


def seed_blog_permissions(db: Session | None = None):
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True
    try:
        _seed_permissions_list(db, DEFAULT_BLOG_PERMISSIONS, "blog")
    finally:
        if should_close:
            db.close()


def seed_cart_permissions(db: Session | None = None):
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True
    try:
        _seed_permissions_list(db, DEFAULT_CART_PERMISSIONS, "cart")
    finally:
        if should_close:
            db.close()


def seed_all_permissions(db: Session | None = None):
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True
    try:
        _seed_permissions_list(db, DEFAULT_PRODUCT_PERMISSIONS, "product")
        _seed_permissions_list(db, DEFAULT_CLIENT_PERMISSIONS, "client")
        _seed_permissions_list(db, DEFAULT_BLOG_PERMISSIONS, "blog")
        _seed_permissions_list(db, DEFAULT_CART_PERMISSIONS, "cart")
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    seed_all_permissions()

