from decimal import Decimal

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    reservation_id: str
    approve: bool


class PaymentResponse(BaseModel):
    id: str
    reservation_id: str
    amount: Decimal
    status: str
    provider_reference: str | None

    model_config = {
        "from_attributes": True,
    }