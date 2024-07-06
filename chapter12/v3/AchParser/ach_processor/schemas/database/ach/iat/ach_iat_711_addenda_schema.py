from typing import Literal
from uuid import UUID

from pydantic import Field, BaseModel


class AchIat711AddendaSchema(BaseModel):
    ach_records_type_7_id: UUID
    record_type_code: str = Literal["7"]
    addenda_type_code: int = Literal[11]
    originator_name: str = Field(..., max_length=35)
    originator_street_address: str = Field(..., max_length=35)
    entry_detail_sequence_number: int = Field(..., ge=0)
