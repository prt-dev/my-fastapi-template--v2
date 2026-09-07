from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.order import Order


class OrderRepository:

    @staticmethod
    def get_by_id(db: Session, order_id: int):
        return db.query(Order).filter(
            Order.id == order_id
        ).first()

    @staticmethod
    def get_by_order_number(db: Session, order_number: str):
        return db.query(Order).filter(
            Order.order_number == order_number
        ).first()

    @staticmethod
    def get_by_razorpay_order_id(db: Session, razorpay_order_id: str):
        return db.query(Order).filter(
            Order.razorpay_order_id == razorpay_order_id
        ).first()

    @staticmethod
    def get_user_orders(db: Session, user_id: int):
        return db.query(Order).filter(
            Order.user_id == user_id
        ).order_by(Order.id.desc()).all()

    @staticmethod
    def get_all_orders(
        db: Session,
        user_id: int | None = None,
        cart_id: int | None = None,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit
        query = db.query(Order)

        if user_id is not None:
            query = query.filter(Order.user_id == user_id)

        if cart_id is not None:
            query = query.filter(Order.cart_id == cart_id)

        if status is not None:
            query = query.filter(Order.status == status)

        if search is not None:
            query = query.filter(
                or_(
                    Order.order_number.ilike(f"%{search}%"),
                    Order.products.ilike(f"%{search}%"),
                    Order.razorpay_order_id.ilike(f"%{search}%"),
                    Order.status.ilike(f"%{search}%")
                )
            )

        total = query.count()
        orders = query.order_by(Order.id.desc()).offset(skip).limit(limit).all()

        return total, orders

    @staticmethod
    def get_user_id(
        db: Session,
        phone: str | None = None,
        email: str | None = None,
        username: str | None = None
    ) -> int | None:
        from app.repositories.user_repository import UserRepository

        user = None
        if phone:
            user = UserRepository.get_by_phone(db, phone)
        elif email:
            user = UserRepository.get_by_email(db, email)
        elif username:
            user = UserRepository.get_by_username(db, username)

        return user.id if user else None

    @staticmethod
    def create(db: Session, order: Order):
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update(db: Session, order: Order, update_data: dict):
        for key, value in update_data.items():
            if hasattr(order, key) and value is not None:
                setattr(order, key, value)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def delete(db: Session, order: Order):
        db.delete(order)
        db.commit()
        return True
