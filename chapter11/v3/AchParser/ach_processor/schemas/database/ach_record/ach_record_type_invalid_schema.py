from typing import Optional

from pydantic import UUID4

from chapter11.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_base_schema import (
    AchRecordBaseSchema,
)


class AchRecordTypeInvalidSchema(AchRecordBaseSchema):
    ach_records_type_invalid_id: Optional[UUID4] = None
    ach_files_id: UUID4
    unparsed_record: str
    sequence_number: int
