from sqlalchemy.orm import Session
from app.services.payment_service import PaymentService
from app.schemas.payment import PaymentIn, RazorpayVerifyIn


class PaymentController:

    @staticmethod
    def get_all_payments(
        db: Session,
        order_id: int | None = None,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return PaymentService.getPayments(
            db=db,
            order_id=order_id,
            status=status,
            search=search,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_payment_by_id(db: Session, payment_id: int):
        return PaymentService.getPaymentById(db, payment_id)

    @staticmethod
    def get_payments_by_order_id(db: Session, order_id: int):
        return PaymentService.getPaymentsByOrderId(db, order_id)

    @staticmethod
    def create_payment(db: Session, request: PaymentIn):
        return PaymentService.createPayment(db, request)

    @staticmethod
    def verify_razorpay_payment(db: Session, request: RazorpayVerifyIn):
        return PaymentService.verifyRazorpayPayment(db, request)

    @staticmethod
    def update_payment(db: Session, payment_id: int, request: PaymentIn):
        return PaymentService.updatePayment(db, payment_id, request)

    @staticmethod
    def delete_payment(db: Session, payment_id: int):
        return PaymentService.deletePayment(db, payment_id)
