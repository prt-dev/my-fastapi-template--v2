from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository
from app.repositories.order_repository import OrderRepository
from app.schemas.payment import PaymentIn


class PaymentService:

    @staticmethod
    def getPayments(
        db: Session,
        order_id: int | None = None,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        total, payments = PaymentRepository.get_all_payments(
            db=db,
            order_id=order_id,
            status=status,
            search=search,
            page=page,
            limit=limit
        )

        return {
            "total": total,
            "payments": payments
        }

    @staticmethod
    def getPaymentById(db: Session, payment_id: int):
        payment = PaymentRepository.get_by_id(db, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment

    @staticmethod
    def getPaymentsByOrderId(db: Session, order_id: int):
        return PaymentRepository.get_by_order_id(db, order_id)

    @staticmethod
    def createPayment(db: Session, request: PaymentIn):
        
        payment_data = request.model_dump(exclude_unset=True)

        if not payment_data.get("order_id"):
            raise HTTPException(status_code=400, detail="Order ID is required")

        order = OrderRepository.get_by_id(db, payment_data["order_id"])
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if not payment_data.get("amount") or payment_data["amount"] == 0:
            payment_data["amount"] = order.amount

        if not payment_data.get("currency"):
            payment_data["currency"] = order.currency

        payment = Payment(**payment_data)
        created_payment = PaymentRepository.create(db, payment)

        # If payment is captured or marked paid, update order status
        if created_payment.status in ("captured", "paid"):
            OrderRepository.update(
                db,
                order,
                {"status": "paid"}
            )

        return created_payment

    @staticmethod
    def updatePayment(db: Session, payment_id: int, request: PaymentIn):
        payment = PaymentRepository.get_by_id(db, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        update_data = request.model_dump(exclude_unset=True)
        return PaymentRepository.update(db, payment, update_data)

    @staticmethod
    def deletePayment(db: Session, payment_id: int):
        payment = PaymentRepository.get_by_id(db, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        PaymentRepository.delete(db, payment)
        return {"message": "Payment deleted successfully"}
