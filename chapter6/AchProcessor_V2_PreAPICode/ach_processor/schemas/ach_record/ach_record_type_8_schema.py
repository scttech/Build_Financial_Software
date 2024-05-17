from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

from ach_processor.schemas.ach_record.ach_record_base_schema import AchRecordBaseSchema


class AchRecordType8Schema(AchRecordBaseSchema):
    ach_records_type_8_id: Optional[UUID4] = None
    ach_records_type_5_id: UUID4