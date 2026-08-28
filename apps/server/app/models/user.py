from enum import StrEnum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.base_model import BaseModel


class UserRole(StrEnum):
    """Roles supported by the Event Platform."""

    ORGANIZER = "organizer"
    CUSTOMER = "customer"
    GATE = "gate"


class User(BaseModel, Base):
    """Application user."""

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
        nullable=False,
    )
    