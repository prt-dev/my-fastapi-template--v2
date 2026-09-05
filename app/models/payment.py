from typing import Optional
from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    razorpay_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    razorpay_payment_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="INR")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    signature_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Code-level relationships (No DB foreign key constraints)
    order: Mapped[Optional["Order"]] = relationship(
        "Order",
        primaryjoin="foreign(Payment.order_id) == Order.id",
    )
