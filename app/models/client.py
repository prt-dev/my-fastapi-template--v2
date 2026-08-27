from typing import Optional
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    domain: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    logo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    default_meta_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    default_meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=1)

    # Code-level relationships (No DB foreign key constraints)
    blogs: Mapped[list["Blog"]] = relationship(
        "Blog",
        primaryjoin="foreign(Blog.client_id) == Client.id",
        back_populates="client",
        cascade="all, delete-orphan",
    )
