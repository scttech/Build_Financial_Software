from typing import Optional

from pydantic import UUID4

from chapter7.v1.AchParser.ach_processor.schemas.database.ach_record.ach_record_base_schema import (
    AchRecordBaseSchema,
)


class AchRecordType5Schema(AchRecordBaseSchema):
    ach_records_type_5_id: Optional[UUID4] = None
    ach_records_type_1_id: UUID4
