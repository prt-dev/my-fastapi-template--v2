from typing import Optional
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    variant: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Code-level relationships (No DB foreign key constraints)
    user: Mapped[Optional["Userdata"]] = relationship(
        "Userdata",
        primaryjoin="foreign(Cart.user_id) == Userdata.id",
    )

    product: Mapped[Optional["Product"]] = relationship(
        "Product",
        primaryjoin="foreign(Cart.product_id) == Product.id",
    )
