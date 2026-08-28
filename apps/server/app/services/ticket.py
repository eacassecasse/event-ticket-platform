import secrets

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Payment,
    PaymentStatus,
    Reservation,
    ReservationStatus,
    Ticket,
    TicketStatus,
    User,
)


def generate_ticket_code() -> str:
    """Generate a cryptographically secure ticket identifier."""

    return secrets.token_urlsafe(32)

def create_ticket(
    *,
    db: Session,
    customer: User,
    reservation_id: str,
) -> Ticket:
    """Issue a ticket for a confirmed reservation."""

    reservation = db.scalar(
        select(Reservation).where(
            Reservation.id == reservation_id,
            Reservation.customer_id == customer.id,
        )
    )

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found.",
        )

    if reservation.status != ReservationStatus.CONFIRMED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "A ticket can only be generated "
                "for a confirmed reservation."
            ),
        )

    existing_ticket = db.scalar(
        select(Ticket).where(
            Ticket.reservation_id == reservation.id,
        )
    )

    if existing_ticket is not None:
        return existing_ticket

    payment = db.scalar(
        select(Payment).where(
            Payment.reservation_id == reservation.id,
            Payment.status == PaymentStatus.ACCEPTED,
        )
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No accepted payment exists for this reservation.",
        )

    ticket = Ticket(
        reservation_id=reservation.id,
        event_id=reservation.event_id,
        customer_id=customer.id,
        code=generate_ticket_code(),
        status=TicketStatus.ACTIVE,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket