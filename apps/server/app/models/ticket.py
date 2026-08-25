#!/usr/bin/python3

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel
from app.database.base import Base


class TicketStatus(StrEnum):
    """Ticket lifecycle states."""

    ACTIVE = "active"
    USED = "used"
    CANCELLED = "cancelled"


class Ticket(BaseModel, Base):
    """Issued event ticket."""

    reservation_id: Mapped[str] = mapped_column(
        ForeignKey("reservations.id"),
        nullable=False,
        index=True,
    )

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

    code: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )

    status: Mapped[TicketStatus] = mapped_column(
        nullable=False,
        default=TicketStatus.ACTIVE,
        index=True,
    )

    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    validated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )