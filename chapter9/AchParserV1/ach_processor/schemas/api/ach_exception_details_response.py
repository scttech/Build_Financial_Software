from datetime import datetime
from typing import Optional

from pydantic import BaseModel, UUID4, Field


class AchExceptionDetailsResponse(BaseModel):
    id: UUID4 = Field(default=..., description="Unique identifier for the ACH exception", title="ID")
    created_at: datetime = Field(default=..., description="The date and time the file was uploaded", title="Uploaded At")
    exception_code: str = Field(default=..., description="The code for the exception", title="Exception Code")
    description: str = Field(default=..., description="Description of the exception", title="Description")
    unparsed_record: str = Field(default=..., description="The unparsed record that caused the exception", title="Unparsed Record")

