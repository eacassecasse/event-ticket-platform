#!/usr/bin/python3

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models import (
    Event,
    EventStatus,
    ExternalCatalogItem,
    User,
    UserRole,
)
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

DEFAULT_PASSWORD = "Password123!"


def seed() -> None:
    db = SessionLocal()

    try:
        organizer = db.scalar(
            select(User).where(
                User.email == "organizer@elitedev.com.br",
            )
        )

        if organizer is None:
            organizer = User(
                name="Demo Organizer",
                email="organizer@elitedev.com.br",
                password_hash=password_hash.hash(DEFAULT_PASSWORD),
                role=UserRole.ORGANIZER,
            )
            db.add(organizer)

        customer_1 = db.scalar(
            select(User).where(
                User.email == "customer1@elitedev.com.br",
            )
        )

        if customer_1 is None:
            customer_1 = User(
                name="Demo Customer One",
                email="customer1@elitedev.com.br",
                password_hash=password_hash.hash(DEFAULT_PASSWORD),
                role=UserRole.CUSTOMER,
            )
            db.add(customer_1)

        customer_2 = db.scalar(
            select(User).where(
                User.email == "customer2@elitedev.com.br",
            )
        )

        if customer_2 is None:
            customer_2 = User(
                name="Demo Customer Two",
                email="customer2@elitedev.com.br",
                password_hash=password_hash.hash(DEFAULT_PASSWORD),
                role=UserRole.CUSTOMER,
            )
            db.add(customer_2)

        gate_user = db.scalar(
            select(User).where(
                User.email == "gate@elitedev.com.br",
            )
        )

        if gate_user is None:
            gate_user = User(
                name="Demo Gate Operator",
                email="gate@elitedev.com.br",
                password_hash=password_hash.hash(DEFAULT_PASSWORD),
                role=UserRole.GATE,
            )
            db.add(gate_user)

        db.flush()

        catalog_item = db.scalar(
            select(ExternalCatalogItem).where(
                ExternalCatalogItem.provider == "demo",
                ExternalCatalogItem.external_id == "demo-event-001",
            )
        )

        if catalog_item is None:
            catalog_item = ExternalCatalogItem(
                provider="demo",
                external_id="demo-event-001",
                title="Elite Dev Live Experience",
                description=(
                    "Demo event used to evaluate the Event Platform."
                ),
                image_url=None,
            )
            db.add(catalog_item)

        db.flush()

        event = db.scalar(
            select(Event).where(
                Event.external_catalog_item_id == catalog_item.id,
            )
        )

        if event is None:
            event = Event(
                organizer_id=organizer.id,
                external_catalog_item_id=catalog_item.id,
                title="Elite Dev Live Experience",
                description=(
                    "A seeded event for evaluation of the platform."
                ),
                event_date=datetime(
                    2026,
                    9,
                    15,
                    20,
                    0,
                    tzinfo=timezone.utc,
                ),
                location="Lisbon Convention Center",
                capacity=100,
                price=Decimal("500.00"),
                status=EventStatus.PUBLISHED,
            )
            db.add(event)

        db.commit()

        print("Seed completed successfully.")
        print()
        print("Demo accounts:")
        print("  Organizer: organizer@elitedev.com.br")
        print("  Customer 1: customer1@elitedev.com.br")
        print("  Customer 2: customer2@elitedev.com.br")
        print("  Gate: gate@elitedev.com.br")
        print(f"  Password: {DEFAULT_PASSWORD}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()