from sqlalchemy.orm import Session
from app.services.cart_service import CartService
from app.schemas.cart import CartIn


class CartController:

    @staticmethod
    def get_all_cart_items(
        db: Session,
        user_id: int | None = None,
        product_id: int | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return CartService.getCarts(
            db=db,
            user_id=user_id,
            product_id=product_id,
            search=search,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_cart_by_id(db: Session, cart_id: int):
        return CartService.getCartById(db, cart_id)

    @staticmethod
    def get_user_cart(db: Session, user_id: int):
        return CartService.getUserCart(db, user_id)

    @staticmethod
    def create_cart_item(db: Session, request: CartIn, current_user_id: int | None = None):
        return CartService.createCart(db, request, current_user_id=current_user_id)

    @staticmethod
    def create_multiple_cart_items(
        db: Session,
        request: list[CartIn],
        current_user_id: int | None = None
    ):
        return CartService.createMultipleCarts(db, request, current_user_id=current_user_id)

    @staticmethod
    def update_cart_item(db: Session, cart_id: int, request: CartIn, current_user_id: int | None = None):
        return CartService.updateCart(db, cart_id, request, current_user_id=current_user_id)

    @staticmethod
    def delete_cart_item(db: Session, cart_id: int, current_user_id: int | None = None):
        return CartService.deleteCart(db, cart_id, current_user_id=current_user_id)

    @staticmethod
    def clear_user_cart(db: Session, user_id: int):
        return CartService.clearCart(db, user_id)
