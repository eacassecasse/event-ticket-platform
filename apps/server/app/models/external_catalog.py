#!/usr/bin/python3

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.base_model import BaseModel

class ExternalCatalogItem(BaseModel, Base):
    """Reference to an item obtained from an external catalogue provider."""

    __tablename__ = "external_catalog_items"

    __table_args__ = (
        UniqueConstraint(
            "provider",
            "external_id",
            name="uq_external_catalog_provider_external_id",
        ),
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    image_url: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )