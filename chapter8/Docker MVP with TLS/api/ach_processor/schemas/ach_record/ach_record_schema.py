from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

from ach_processor.schemas.ach_record.ach_record_base_schema import AchRecordBaseSchema


class AchRecordSchema(AchRecordBaseSchema):
    primary_key: Optional[UUID4] = None
