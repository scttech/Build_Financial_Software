from typing import Optional

from pydantic import BaseModel, UUID4


class AchRecordSchema(BaseModel):
    ach_records_id: Optional[UUID4] = None
    ach_files_id: UUID4
    unparsed_record: str
    sequence_number: int
