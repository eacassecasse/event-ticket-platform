from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import require_role
from app.database.session import get_db
from app.models import (
    Ticket,
    TicketStatus,
    User,
    UserRole,
)
from app.schemas.ticket import (
    TicketResponse,
    TicketValidationRequest,
    TicketValidationResponse,
)
from app.services.ticket import create_ticket

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=201,
)
def issue_ticket(
    reservation_id: str,
    current_user: Annotated[
        User,
        Depends(
            require_role(UserRole.CUSTOMER),
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> Ticket:

    return create_ticket(
        db=db,
        customer=current_user,
        reservation_id=reservation_id,
    )


@router.get(
    "/me",
    response_model=list[TicketResponse],
)
def list_my_tickets(
    current_user: Annotated[
        User,
        Depends(
            require_role(UserRole.CUSTOMER),
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> list[Ticket]:

    return list(
        db.scalars(
            select(Ticket)
            .where(
                Ticket.customer_id == current_user.id,
            )
            .order_by(Ticket.issued_at.desc())
        )
    )

@router.post(
    "/validate",
    response_model=TicketValidationResponse,
)
def validate_ticket(
    payload: TicketValidationRequest,
    current_user: Annotated[
        User,
        Depends(
            require_role(UserRole.GATE),
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> TicketValidationResponse:

    ticket = db.scalar(
        select(Ticket)
        .where(Ticket.code == payload.code)
        .with_for_update()
    )

    if ticket is None:
        return TicketValidationResponse(
            valid=False,
            status="invalid",
            message="Ticket not found.",
        )

    if ticket.event_id != payload.event_id:
        return TicketValidationResponse(
            valid=False,
            status="wrong_event",
            message="Ticket belongs to another event.",
            ticket_id=ticket.id,
        )

    if ticket.status == TicketStatus.USED:
        return TicketValidationResponse(
            valid=False,
            status="used",
            message="Ticket has already been used.",
            ticket_id=ticket.id,
        )

    if ticket.status == TicketStatus.CANCELLED:
        return TicketValidationResponse(
            valid=False,
            status="invalid",
            message="Ticket has been cancelled.",
            ticket_id=ticket.id,
        )

    ticket.status = TicketStatus.USED
    ticket.validated_at = datetime.now(timezone.utc)

    db.commit()

    return TicketValidationResponse(
        valid=True,
        status="valid",
        message="Ticket validated successfully.",
        ticket_id=ticket.id,
    )

@router.get(
    "/share/{code}",
    response_model=TicketResponse,
)
def get_shared_ticket(
    code: str,
    db: Annotated[Session, Depends(get_db)],
) -> Ticket:

    ticket = db.scalar(
        select(Ticket).where(
            Ticket.code == code,
        )
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found.",
        )

    return ticket