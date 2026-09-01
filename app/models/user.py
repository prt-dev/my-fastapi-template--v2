from typing import Optional

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from app.core.database import Base


class Userdata(Base):
    __tablename__ = "userdata"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    firstname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    lastname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    password: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[int] = mapped_column(Integer, default=1)
    additional_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Code-level relationship (No DB foreign key constraint)
    role: Mapped[Optional["Role"]] = relationship(
        "Role",
        primaryjoin="foreign(Userdata.role_id) == Role.id",
        back_populates="users",
    )
