from typing import Optional, List
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="INR")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    razorpay_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    # Code-level relationships (No DB foreign key constraints)
    user: Mapped[Optional["Userdata"]] = relationship(
        "Userdata",
        primaryjoin="foreign(Order.user_id) == Userdata.id",
    )

    payments: Mapped[List["Payment"]] = relationship(
        "Payment",
        primaryjoin="foreign(Payment.order_id) == Order.id",
    )
