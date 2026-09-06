from typing import Optional
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    client_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=1)

    # Code-level relationships (No DB foreign key constraints)
    client: Mapped[Optional["Client"]] = relationship(
        "Client",
        primaryjoin="foreign(Contact.client_id) == Client.id",
        back_populates="contacts",
    )
