from typing import Optional
from pydantic import UUID4

from chapter9.AchParserV1.ach_processor.schemas.database.ach_record.ach_record_base_schema import (
    AchRecordBaseSchema,
)


class AchRecordSchema(AchRecordBaseSchema):
    primary_key: Optional[UUID4] = None
