from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import Field, BaseModel


class AchIat710AddendaSchema(BaseModel):
    ach_records_type_7_id: UUID
    record_type_code: str = Literal["7"]
    addenda_type_code: int = Literal[10]
    transaction_type_code: str = Field(..., min_length=1, max_length=3)
    foreign_payment_amount: Decimal = Field(..., ge=0)
    foreign_trace_number: str = Field(max_length=22, default="")
    receiving_name: str = Field(max_length=35, default="")
    entry_detail_sequence_number: int = Field(..., ge=0)
