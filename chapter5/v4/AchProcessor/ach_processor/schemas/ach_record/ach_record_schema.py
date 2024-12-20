from typing import Optional

from pydantic import UUID4

from chapter5.AchProcessor_V2.ach_processor.schemas.ach_record.ach_record_base_schema import (
    AchRecordBaseSchema,
)


class AchRecordSchema(AchRecordBaseSchema):
    primary_key: Optional[UUID4] = None
