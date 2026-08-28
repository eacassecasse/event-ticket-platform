from sqlalchemy import String, Text, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    images: Mapped[list["ExternalCatalogItemImage"]] = relationship(
        back_populates="catalog_item",
        cascade="all, delete-orphan",
        order_by="ExternalCatalogItemImage.sort_order",
    )


class ExternalCatalogItemImage(BaseModel, Base):
    """Image belonging to an external catalogue item."""

    __tablename__ = "external_catalog_item_images"

    catalog_item_id: Mapped[str] = mapped_column(
        ForeignKey(
            "external_catalog_items.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    ratio: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    width: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    height: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    fallback: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    sort_order: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    catalog_item: Mapped["ExternalCatalogItem"] = relationship(
        back_populates="images",
    )