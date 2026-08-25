from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel
from app.database.base import Base


class EventStatus(StrEnum):
    """Lifecycle states supported by an event."""

    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"


class Event(BaseModel, Base):
    """Event published on the platform."""

    organizer_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    external_catalog_item_id: Mapped[str] = mapped_column(
        ForeignKey("external_catalog_items.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    capacity: Mapped[int] = mapped_column(
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    status: Mapped[EventStatus] = mapped_column(
        nullable=False,
        default=EventStatus.DRAFT,
    )