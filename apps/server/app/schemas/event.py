from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    catalog_external_id: str
    title: str
    description: str | None = None
    event_date: datetime
    location: str = Field(min_length=2)
    capacity: int = Field(gt=0)
    price: Decimal = Field(gt=0)


class EventResponse(BaseModel):
    id: str
    title: str
    description: str | None
    event_date: datetime
    location: str
    capacity: int
    price: Decimal
    status: str

    model_config = {
        "from_attributes": True,
    }