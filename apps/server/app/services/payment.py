from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    Payment,
    PaymentStatus,
    Reservation,
    ReservationStatus,
    User,
)


def process_payment(
    *,
    db: Session,
    customer: User,
    reservation_id: str,
    approve: bool,
) -> Payment:

    reservation = db.scalar(
        select(Reservation)
        .where(
            Reservation.id == reservation_id,
            Reservation.customer_id == customer.id,
        )
        .with_for_update()
    )

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found.",
        )

    if reservation.status != ReservationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Reservation has already been processed.",
        )

    payment_status = (
        PaymentStatus.ACCEPTED
        if approve
        else PaymentStatus.REJECTED
    )

    payment = Payment(
        reservation_id=reservation.id,
        amount=reservation.total_amount,
        status=payment_status,
        provider_reference=(
            f"SIM-{uuid4().hex[:12].upper()}"
        ),
        processed_at=datetime.now(timezone.utc),
    )

    reservation.status = (
        ReservationStatus.CONFIRMED
        if approve
        else ReservationStatus.CANCELLED
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment