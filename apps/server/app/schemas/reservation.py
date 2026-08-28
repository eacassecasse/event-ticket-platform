from decimal import Decimal

from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    event_id: str
    quantity: int = Field(gt=0)


class ReservationResponse(BaseModel):
    id: str
    event_id: str
    customer_id: str
    quantity: int
    unit_price: Decimal
    total_amount: Decimal
    status: str

    model_config = {
        "from_attributes": True,
    }