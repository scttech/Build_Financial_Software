from typing import Optional

from chapter6.AchProcessor_V2.ach_processor.schemas.ach_record.ach_record_base_schema import AchRecordBaseSchema
from pydantic import UUID4


class AchRecordSchema(AchRecordBaseSchema):
    primary_key: Optional[UUID4] = None
