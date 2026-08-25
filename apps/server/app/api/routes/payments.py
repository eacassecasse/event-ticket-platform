from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_role
from app.database.session import get_db
from app.models import User, UserRole
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
)
from app.services.payment import process_payment


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=201,
)
def pay(
    payload: PaymentCreate,
    current_user: Annotated[
        User,
        Depends(
            require_role(UserRole.CUSTOMER),
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> PaymentResponse:

    payment = process_payment(
        db=db,
        customer=current_user,
        reservation_id=payload.reservation_id,
        approve=payload.approve,
    )

    return payment