from typing import Optional

from chapter6.AchProcessor_V2_PreAPICode.ach_processor.schemas.ach_record.ach_record_base_schema import AchRecordBaseSchema
from pydantic import UUID4


class AchRecordType9Schema(AchRecordBaseSchema):
    ach_records_type_9_id: Optional[UUID4] = None
    ach_records_type_1_id: UUID4