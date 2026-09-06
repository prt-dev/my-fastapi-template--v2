from app.schemas.auth import LoginRequest
from app.schemas.product import ProductIn, ProductOut
from app.schemas.client import ClientIn, ClientOut
from app.schemas.blog import BlogIn, BlogOut
from app.schemas.cart import CartIn, CartOut
from app.schemas.contact import ContactIn, ContactOut
from app.schemas.user import UserIn, UserOut
from app.schemas.permission import PermissionIn, PermissionOut, RolePermissionOut

LoginIn = LoginRequest

__all__ = [
    "LoginRequest",
    "LoginIn",
    "ProductIn",
    "ProductOut",
    "ClientIn",
    "ClientOut",
    "BlogIn",
    "BlogOut",
    "CartIn",
    "CartOut",
    "ContactIn",
    "ContactOut",
    "UserIn",
    "UserOut",
    "PermissionIn",
    "PermissionOut",
    "RolePermissionOut",
]

