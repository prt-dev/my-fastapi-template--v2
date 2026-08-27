from sqlalchemy.orm import Session

from app.models.cart import Cart


class CartRepository:

    @staticmethod
    def get_by_id(db: Session, cart_id: int):
        return db.query(Cart).filter(
            Cart.id == cart_id
        ).first()

    @staticmethod
    def get_by_user_product_variant(
        db: Session,
        user_id: int,
        product_id: int,
        variant: str | None = None
    ):
        query = db.query(Cart).filter(
            Cart.user_id == user_id,
            Cart.product_id == product_id
        )
        if variant is not None:
            query = query.filter(Cart.variant == variant)
        else:
            query = query.filter(Cart.variant.is_(None))
        return query.first()

    @staticmethod
    def get_all_cart_items(
        db: Session,
        user_id: int | None = None,
        product_id: int | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit
        query = db.query(Cart)

        if user_id is not None:
            query = query.filter(Cart.user_id == user_id)

        if product_id is not None:
            query = query.filter(Cart.product_id == product_id)

        if search is not None:
            query = query.filter(
                Cart.variant.ilike(f"%{search}%")
            )

        total = query.count()
        cart_items = query.offset(skip).limit(limit).all()

        return total, cart_items

    @staticmethod
    def get_user_cart(db: Session, user_id: int):
        return db.query(Cart).filter(
            Cart.user_id == user_id
        ).all()

    @staticmethod
    def create(db: Session, cart: Cart):
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def update(db: Session, cart: Cart, update_data: dict):
        for key, value in update_data.items():
            if hasattr(cart, key) and value is not None:
                setattr(cart, key, value)
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def delete(db: Session, cart: Cart):
        db.delete(cart)
        db.commit()
        return True

    @staticmethod
    def clear_user_cart(db: Session, user_id: int):
        db.query(Cart).filter(Cart.user_id == user_id).delete()
        db.commit()
        return True
