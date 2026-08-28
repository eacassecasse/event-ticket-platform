from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.base_model import BaseModel


class PaymentStatus(StrEnum):
    """Payment processing states."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Payment(BaseModel, Base):
    """Simulated payment associated with a reservation."""

    reservation_id: Mapped[str] = mapped_column(
        ForeignKey("reservations.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    status: Mapped[PaymentStatus] = mapped_column(
        nullable=False,
        default=PaymentStatus.PENDING,
        index=True,
    )

    provider_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )