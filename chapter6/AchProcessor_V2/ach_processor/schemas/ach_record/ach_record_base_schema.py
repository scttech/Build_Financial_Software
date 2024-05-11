from abc import ABC
from pydantic import BaseModel

class AchRecordBaseSchema(ABC, BaseModel):
    unparsed_record: str
    sequence_number: int
