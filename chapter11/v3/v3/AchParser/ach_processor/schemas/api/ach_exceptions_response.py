from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, Field


class AchExceptionsResponse(BaseModel):
    id: UUID4 = Field(default=..., description="Unique identifier for the ACH exception", title="ID")
    file_id: UUID4 = Field(default='', description="Unique identifier for the ACH file", title="File ID")
    file_name: str = Field(default='', description="Name of the ACH file", title="Filename")
    created_at: datetime = Field(default=..., description="The date and time the file was uploaded", title="Uploaded At")
    batch_id: Optional[UUID4] = Field(default=None, description="Unique identifier for the ACH batch", title="Batch ID")
    entry_id: Optional[UUID4] = Field(default=None, description="Unique identifier for the ACH entry", title="Entry ID")
    record_number: int = Field(default=..., description="The record number of the exception", title="Record Number")
    exception_code: str = Field(default=..., description="The code for the exception", title="Exception Code")
    description: str = Field(default=..., description="Description of the exception", title="Description")
