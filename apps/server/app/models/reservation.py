from decimal import Decimal
from enum import StrEnum

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.base_model import BaseModel


class ReservationStatus(StrEnum):
    """Reservation lifecycle states."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Reservation(BaseModel, Base):
    """Customer reservation for an event."""

    event_id: Mapped[str] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
        index=True,
    )

    customer_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    status: Mapped[ReservationStatus] = mapped_column(
        nullable=False,
        default=ReservationStatus.PENDING,
        index=True,
    )