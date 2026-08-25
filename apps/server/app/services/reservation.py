from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    Event,
    EventStatus,
    Reservation,
    ReservationStatus,
    User,
)


def create_reservation(
    *,
    db: Session,
    customer: User,
    event_id: str,
    quantity: int,
) -> Reservation:
    """
    Create a reservation while protecting event capacity
    against concurrent purchases.
    """

    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero.",
        )

    # Lock the event row for the duration of this transaction.
    event = db.scalar(
        select(Event)
        .where(Event.id == event_id)
        .with_for_update()
    )

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found.",
        )

    if event.status != EventStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is not available for reservation.",
        )

    confirmed_quantity = db.scalar(
        select(
            func.coalesce(
                func.sum(Reservation.quantity),
                0,
            )
        )
        .where(
            Reservation.event_id == event.id,
            Reservation.status == ReservationStatus.CONFIRMED,
        )
    )

    confirmed_quantity = int(confirmed_quantity or 0)

    available_quantity = event.capacity - confirmed_quantity

    if quantity > available_quantity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Only {available_quantity} ticket(s) "
                "are available."
            ),
        )

    unit_price = Decimal(event.price)
    total_amount = unit_price * quantity

    reservation = Reservation(
        event_id=event.id,
        customer_id=customer.id,
        quantity=quantity,
        unit_price=unit_price,
        total_amount=total_amount,
        status=ReservationStatus.PENDING,
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation