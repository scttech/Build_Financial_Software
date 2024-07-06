from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4


class AchFileSchema(BaseModel):
    ach_files_id: Optional[UUID4] = None
    file_name: str
    file_hash: str
    created_at: Optional[datetime] = None
