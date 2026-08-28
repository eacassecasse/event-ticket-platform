from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_role
from app.database.session import get_db
from app.models import User, UserRole
from app.schemas.reservation import (
    ReservationCreate,
    ReservationResponse,
)
from app.services.reservation import create_reservation

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"],
)


@router.post(
    "",
    response_model=ReservationResponse,
    status_code=201,
)
def reserve(
    payload: ReservationCreate,
    current_user: Annotated[
        User,
        Depends(
            require_role(UserRole.CUSTOMER),
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> ReservationResponse:

    reservation = create_reservation(
        db=db,
        customer=current_user,
        event_id=payload.event_id,
        quantity=payload.quantity,
    )

    return reservation