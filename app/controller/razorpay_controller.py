from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.order import OrderIn
from app.schemas.payment import PaymentIn, RazorpayVerifyIn
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService
from app.services.razorpay_service import RazorpayService
from app.repositories.order_repository import OrderRepository


class RazorpayController:

    @staticmethod
    def create_razorpay_order(
        db: Session,
        request: OrderIn,
        current_user_id: int | None = None,
    ):
        # 1. Reuse createOrder function to create order only
        order = OrderService.createOrder(db, request, current_user_id=current_user_id)

        # 2. Call RazorpayOrder in that
        return RazorpayService.RazorpayOrder(db=db, order=order)

    @staticmethod
    def create_razorpay_order_by_order_id(
        db: Session,
        order_id: int,
    ):
        order = OrderService.getOrderById(db, order_id)
        return RazorpayService.RazorpayOrder(db=db, order=order)

    RazorpayOrder = create_razorpay_order

    @staticmethod
    def verify_razorpay_payment(
        db: Session,
        request: RazorpayVerifyIn,
    ):
        # 1. Verify Razorpay payment signature
        RazorpayService.verify_signature(
            razorpay_order_id=request.razorpay_order_id,
            razorpay_payment_id=request.razorpay_payment_id,
            razorpay_signature=request.razorpay_signature,
        )

        # 2. Locate associated order using Order module functions
        order = None
        if request.order_id:
            try:
                order = OrderService.getOrderById(db, request.order_id)
            except HTTPException:
                order = None

        if not order:
            order = OrderRepository.get_by_razorpay_order_id(db, request.razorpay_order_id)

        if not order:
            raise HTTPException(status_code=404, detail="Associated order not found")

        # 3. Check payment status from Razorpay API
        payment_status = "captured"
        try:
            rzp_payment = RazorpayService.get_payment(request.razorpay_payment_id)
            if rzp_payment and isinstance(rzp_payment, dict):
                payment_status = rzp_payment.get("status", "captured")
        except Exception as e:
            print(f"Warning: Could not fetch payment from Razorpay: {e}")

        # 4. Create or update payment using Payment module functions
        existing_payments = PaymentService.getPaymentsByOrderId(db, order.id)
        payment = None
        for p in existing_payments:
            if getattr(p, "razorpay_payment_id", None) == request.razorpay_payment_id:
                payment = p
                break

        if payment:
            payment = PaymentService.updatePayment(
                db,
                payment.id,
                PaymentIn(
                    status=payment_status,
                    signature_verified=True,
                    razorpay_order_id=request.razorpay_order_id,
                    razorpay_payment_id=request.razorpay_payment_id,
                )
            )
        else:
            payment_in = PaymentIn(
                order_id=order.id,
                amount=order.amount,
                currency=order.currency,
                status=payment_status,
                signature_verified=True,
                razorpay_order_id=request.razorpay_order_id,
                razorpay_payment_id=request.razorpay_payment_id,
            )
            payment = PaymentService.createPayment(db, payment_in)

        # 5. Ensure order has razorpay_order_id and status is paid
        OrderRepository.update(
            db,
            order,
            {
                "status": "paid",
                "razorpay_order_id": request.razorpay_order_id
            }
        )

        return payment

    verify_payment = verify_razorpay_payment
