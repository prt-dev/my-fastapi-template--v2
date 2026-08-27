from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartIn


class CartService:

    @staticmethod
    def getCarts(
        db: Session,
        user_id: int | None = None,
        product_id: int | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        total, carts = CartRepository.get_all_cart_items(
            db=db,
            user_id=user_id,
            product_id=product_id,
            search=search,
            page=page,
            limit=limit
        )

        return {
            "total": total,
            "carts": carts
        }

    @staticmethod
    def getCartById(db: Session, cart_id: int):
        cart = CartRepository.get_by_id(db, cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart item not found")
        return cart

    @staticmethod
    def getUserCart(db: Session, user_id: int):
        items = CartRepository.get_user_cart(db, user_id)
        total_items = sum(item.quantity for item in items)
        subtotal = round(sum(item.price * item.quantity for item in items), 2)
        return {
            "total_items": total_items,
            "subtotal": subtotal,
            "items": items
        }

    @staticmethod
    def createCart(db: Session, request: CartIn, current_user_id: int | None = None):
        cart_data = request.model_dump(exclude_unset=True)

        if not cart_data.get("user_id") and current_user_id:
            cart_data["user_id"] = current_user_id

        if not cart_data.get("user_id"):
            raise HTTPException(status_code=400, detail="User ID is required")

        if not cart_data.get("product_id"):
            raise HTTPException(status_code=400, detail="Product ID is required")

        product = ProductRepository.get_by_id(db, cart_data["product_id"])
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Set default price from product if price not specified or 0
        if cart_data.get("price") is None or cart_data.get("price") == 0:
            cart_data["price"] = product.price

        # Check if item with identical product and variant already exists in cart for this user
        existing_item = CartRepository.get_by_user_product_variant(
            db=db,
            user_id=cart_data["user_id"],
            product_id=cart_data["product_id"],
            variant=cart_data.get("variant")
        )

        if existing_item:
            # Increment quantity
            new_quantity = existing_item.quantity + cart_data.get("quantity", 1)
            update_data = {"quantity": new_quantity}
            if cart_data.get("price") is not None and cart_data.get("price") > 0:
                update_data["price"] = cart_data["price"]
            return CartRepository.update(db, existing_item, update_data)

        cart = Cart(**cart_data)
        return CartRepository.create(db, cart)

    @staticmethod
    def updateCart(db: Session, cart_id: int, request: CartIn, current_user_id: int | None = None):
        cart = CartRepository.get_by_id(db, cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart item not found")

        if current_user_id and cart.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this cart item")

        update_data = request.model_dump(exclude_unset=True)
        return CartRepository.update(db, cart, update_data)

    @staticmethod
    def deleteCart(db: Session, cart_id: int, current_user_id: int | None = None):
        cart = CartRepository.get_by_id(db, cart_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart item not found")

        if current_user_id and cart.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this cart item")

        CartRepository.delete(db, cart)
        return {"message": "Cart item deleted successfully"}

    @staticmethod
    def clearCart(db: Session, user_id: int):
        CartRepository.clear_user_cart(db, user_id)
        return {"message": "Cart cleared successfully"}
