import hmac
import hashlib
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import RAZORPAY_KEY_SECRET
from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository
from app.repositories.order_repository import OrderRepository
from app.schemas.payment import PaymentIn, RazorpayVerifyIn
from app.services.razorpay_service import RazorpayService


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

        if not payment_data.get("razorpay_order_id") and order.razorpay_order_id:
            payment_data["razorpay_order_id"] = order.razorpay_order_id

        if payment_data.get("razorpay_payment_id"):
            try:
                rzp_payment = RazorpayService.get_payment(payment_data["razorpay_payment_id"])
                if rzp_payment and isinstance(rzp_payment, dict):
                    if not payment_data.get("status"):
                        payment_data["status"] = rzp_payment.get("status", "pending")
                    if rzp_payment.get("status") == "captured":
                        payment_data["signature_verified"] = True
            except Exception as e:
                print(f"Warning: Could not fetch payment from Razorpay: {e}")

        payment = Payment(**payment_data)
        created_payment = PaymentRepository.create(db, payment)

        # If payment is captured or marked paid, update order status
        if created_payment.status in ("captured", "paid"):
            OrderRepository.update(
                db,
                order,
                {
                    "status": "paid",
                    "razorpay_order_id": created_payment.razorpay_order_id or order.razorpay_order_id
                }
            )

        return created_payment

    @staticmethod
    def verifyRazorpayPayment(db: Session, request: RazorpayVerifyIn):
        if not RAZORPAY_KEY_SECRET:
            raise HTTPException(
                status_code=500,
                detail="RAZORPAY_KEY_SECRET is not configured on the server"
            )

        try:
            RazorpayService.verify_payment(
                razorpay_order_id=request.razorpay_order_id,
                razorpay_payment_id=request.razorpay_payment_id,
                razorpay_signature=request.razorpay_signature,
            )
        except Exception:
            body_to_sign = f"{request.razorpay_order_id}|{request.razorpay_payment_id}"
            expected_signature = hmac.new(
                RAZORPAY_KEY_SECRET.encode("utf-8"),
                body_to_sign.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, request.razorpay_signature):
                raise HTTPException(
                    status_code=400,
                    detail="Razorpay payment signature verification failed"
                )

        order = None
        if request.order_id:
            order = OrderRepository.get_by_id(db, request.order_id)
        if not order:
            order = OrderRepository.get_by_razorpay_order_id(db, request.razorpay_order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Associated order not found")

        payment_status = "captured"
        try:
            rzp_payment = RazorpayService.get_payment(request.razorpay_payment_id)
            if rzp_payment and isinstance(rzp_payment, dict):
                payment_status = rzp_payment.get("status", "captured")
        except Exception as e:
            print(f"Warning: Could not fetch payment from Razorpay: {e}")

        payment = PaymentRepository.get_by_razorpay_payment_id(db, request.razorpay_payment_id)
        if payment:
            payment = PaymentRepository.update(
                db,
                payment,
                {
                    "status": payment_status,
                    "signature_verified": True,
                    "razorpay_order_id": request.razorpay_order_id,
                }
            )
        else:
            payment = Payment(
                order_id=order.id,
                razorpay_order_id=request.razorpay_order_id,
                razorpay_payment_id=request.razorpay_payment_id,
                amount=order.amount,
                currency=order.currency,
                status=payment_status,
                signature_verified=True,
            )
            payment = PaymentRepository.create(db, payment)

        OrderRepository.update(
            db,
            order,
            {
                "status": "paid",
                "razorpay_order_id": request.razorpay_order_id
            }
        )

        return payment

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
