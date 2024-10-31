from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import Field, BaseModel


class AchIat715AddendaSchema(BaseModel):
    ach_records_type_7_id: UUID
    record_type_code: str = Literal["7"]
    addenda_type_code: int = Literal[15]
    receiver_identification_number: str = Field(..., max_length=15)
    receiver_street_address: str = Field(..., max_length=35)
    entry_detail_sequence_number: int = Field(..., ge=0)
