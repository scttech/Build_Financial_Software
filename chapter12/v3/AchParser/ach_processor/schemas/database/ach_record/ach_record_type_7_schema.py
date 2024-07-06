from typing import Optional

from pydantic import UUID4

from chapter12.v3.AchParser.ach_processor.schemas.database.ach_record.ach_record_base_schema import (
    AchRecordBaseSchema,
)


class AchRecordType7Schema(AchRecordBaseSchema):
    ach_records_type_7_id: Optional[UUID4] = None
    ach_records_type_6_id: UUID4
