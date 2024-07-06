from typing import Optional

from pydantic import UUID4

from chapter10.v2.AchParser.ach_processor.schemas.database.ach_record.ach_record_base_schema import (
    AchRecordBaseSchema,
)


class AchRecordType8Schema(AchRecordBaseSchema):
    ach_records_type_8_id: Optional[UUID4] = None
    ach_records_type_5_id: UUID4
