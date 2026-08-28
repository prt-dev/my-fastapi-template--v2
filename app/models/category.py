from typing import Optional
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    status: Mapped[int] = mapped_column(Integer, default=1)

    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        primaryjoin="foreign(Category.parent_id) == Category.id",
        remote_side=[id],
    )

    products: Mapped[list["Product"]] = relationship(
        "Product",
        primaryjoin="foreign(Product.category_id) == Category.id",
        viewonly=True,
    )
