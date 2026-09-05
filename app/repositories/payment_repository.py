from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    def get_by_id(db: Session, payment_id: int):
        return db.query(Payment).filter(
            Payment.id == payment_id
        ).first()

    @staticmethod
    def get_by_order_id(db: Session, order_id: int):
        return db.query(Payment).filter(
            Payment.order_id == order_id
        ).order_by(Payment.id.desc()).all()

    @staticmethod
    def get_by_razorpay_order_id(db: Session, razorpay_order_id: str):
        return db.query(Payment).filter(
            Payment.razorpay_order_id == razorpay_order_id
        ).order_by(Payment.id.desc()).all()

    @staticmethod
    def get_by_razorpay_payment_id(db: Session, razorpay_payment_id: str):
        return db.query(Payment).filter(
            Payment.razorpay_payment_id == razorpay_payment_id
        ).first()

    @staticmethod
    def get_all_payments(
        db: Session,
        order_id: int | None = None,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit
        query = db.query(Payment)

        if order_id is not None:
            query = query.filter(Payment.order_id == order_id)

        if status is not None:
            query = query.filter(Payment.status == status)

        if search is not None:
            query = query.filter(
                or_(
                    Payment.razorpay_payment_id.ilike(f"%{search}%"),
                    Payment.razorpay_order_id.ilike(f"%{search}%"),
                    Payment.status.ilike(f"%{search}%")
                )
            )

        total = query.count()
        payments = query.order_by(Payment.id.desc()).offset(skip).limit(limit).all()

        return total, payments

    @staticmethod
    def create(db: Session, payment: Payment):
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def update(db: Session, payment: Payment, update_data: dict):
        for key, value in update_data.items():
            if hasattr(payment, key) and value is not None:
                setattr(payment, key, value)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def delete(db: Session, payment: Payment):
        db.delete(payment)
        db.commit()
        return True
