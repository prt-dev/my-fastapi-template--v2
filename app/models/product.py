from typing import Optional
from sqlalchemy import Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    sku: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    variant: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=1)
    
    category: Mapped[Optional["Category"]] = relationship(
        "Category",
        primaryjoin="foreign(Product.category_id) == Category.id",
    )

