from datetime import datetime

from pydantic import BaseModel


class TicketResponse(BaseModel):
    id: str
    reservation_id: str
    event_id: str
    customer_id: str
    code: str
    status: str
    issued_at: datetime
    validated_at: datetime | None

    model_config = {
        "from_attributes": True,
    }


class TicketValidationRequest(BaseModel):
    code: str
    event_id: str


class TicketValidationResponse(BaseModel):
    valid: bool
    status: str
    message: str
    ticket_id: int | None = None