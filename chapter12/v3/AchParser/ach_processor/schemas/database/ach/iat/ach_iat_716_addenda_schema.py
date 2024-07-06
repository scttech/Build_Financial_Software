from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import Field, BaseModel


class AchIat716AddendaSchema(BaseModel):
    ach_records_type_7_id: UUID
    record_type_code: str = Literal["7"]
    addenda_type_code: int = Literal[16]
    receiver_city: str = Field(..., max_length=35)
    receiver_state: str = Field(..., max_length=35)
    receiver_country: str = Field(..., max_length=35)
    receiver_postal_code: str = Field(..., max_length=35)
    entry_detail_sequence_number: int = Field(..., ge=0)
