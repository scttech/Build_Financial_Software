from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import Field, BaseModel


class AchIat714AddendaSchema(BaseModel):
    ach_records_type_7_id: UUID
    record_type_code: str = Literal["7"]
    addenda_type_code: int = Literal[14]
    receiving_dfi_name: str = Field(..., max_length=35)
    receiving_dfi_identification_qualifier: str = Field(..., max_length=2)
    receiving_dfi_identification: str = Field(..., max_length=34)
    receiving_dfi_branch_country_code: str = Field(..., max_length=3)
    entry_detail_sequence_number: int = Field(..., ge=0)
