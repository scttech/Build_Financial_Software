from typing import Literal
from uuid import UUID

from pydantic import Field, BaseModel


class AchIat713AddendaSchema(BaseModel):
    ach_records_type_7_id: UUID
    record_type_code: str = Literal["7"]
    addenda_type_code: int = Literal[13]
    originating_dfi_name: str = Field(..., max_length=35)
    originating_dfi_identification_qualifier: str = Field(..., max_length=2)
    originating_dfi_identification: str = Field(..., max_length=34)
    originating_dfi_branch_country_code: str = Field(..., max_length=3)
    entry_detail_sequence_number: int = Field(..., ge=0)
