from typing import Optional
from pydantic import UUID4

from ach_processor.schemas.database.ach_record.ach_record_base_schema import (
    AchRecordBaseSchema,
)


class AchRecordType9Schema(AchRecordBaseSchema):
    ach_records_type_9_id: Optional[UUID4] = None
    ach_records_type_1_id: UUID4
