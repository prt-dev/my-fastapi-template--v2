from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    client_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    author_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)

    featured_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    status: Mapped[int] = mapped_column(Integer, default=1)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    meta_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    canonical_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    og_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    og_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    og_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Code-level relationships (No DB foreign key constraints)
    client: Mapped[Optional["Client"]] = relationship(
        "Client",
        primaryjoin="foreign(Blog.client_id) == Client.id",
        back_populates="blogs",
    )

    author: Mapped[Optional["Userdata"]] = relationship(
        "Userdata",
        primaryjoin="foreign(Blog.author_id) == Userdata.id",
    )
