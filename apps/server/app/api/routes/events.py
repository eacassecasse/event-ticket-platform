from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import require_role
from app.database.session import get_db
from app.models import (
    Event,
    EventStatus,
    ExternalCatalogItem,
    User,
    UserRole,
)
from app.schemas.event import EventCreate, EventResponse

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=EventResponse,
    status_code=201,
)
def create_event(
    payload: EventCreate,
    current_user: Annotated[
        User,
        Depends(
            require_role(UserRole.ORGANIZER),
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> Event:

    catalog_item = db.scalar(
        select(ExternalCatalogItem).where(
            ExternalCatalogItem.provider == "ticketmaster",
            ExternalCatalogItem.external_id
            == payload.catalog_external_id,
        )
    )

    if catalog_item is None:
        catalog_item = ExternalCatalogItem(
            provider="ticketmaster",
            external_id=payload.catalog_external_id,
            title=payload.title,
            description=payload.description,
        )

        db.add(catalog_item)
        db.flush()

    event = Event(
        organizer_id=current_user.id,
        external_catalog_item_id=catalog_item.id,
        title=payload.title,
        description=payload.description,
        event_date=payload.event_date,
        location=payload.location,
        capacity=payload.capacity,
        price=payload.price,
        status=EventStatus.PUBLISHED,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event

@router.get(
    "",
    response_model=list[EventResponse],
)
def list_events(
    db: Annotated[Session, Depends(get_db)],
) -> list[Event]:

    return list(
        db.scalars(
            select(Event)
            .where(
                Event.status == EventStatus.PUBLISHED,
            )
            .order_by(Event.event_date)
        )
    )