from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

from ach_processor.schemas.ach_record.ach_record_base_schema import AchRecordBaseSchema


class AchRecordType1Schema(AchRecordBaseSchema):
    ach_records_type_1_id: Optional[UUID4] = None
    ach_files_id: UUID4
