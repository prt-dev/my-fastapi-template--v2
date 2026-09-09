from typing import Optional
from sqlalchemy import Integer, String, Float, Text
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
    products: Mapped[str] = mapped_column(Text, nullable=False)
    product_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    variant: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True, default="1", server_default="1")

    # Code-level relationships (No DB foreign key constraints)
    user: Mapped[Optional["Userdata"]] = relationship(
        "Userdata",
        primaryjoin="foreign(Cart.user_id) == Userdata.id",
    )

    product: Mapped[Optional["Product"]] = relationship(
        "Product",
        primaryjoin="foreign(Cart.product_id) == Product.id",
    )
