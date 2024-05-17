from abc import ABC
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4

class AchRecordBaseSchema(ABC, BaseModel):
    unparsed_record: str
    sequence_number: int