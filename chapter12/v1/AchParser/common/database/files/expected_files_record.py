from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, UUID4

from chapter12.v1.AchParser.common.schedule.schedule_type import ScheduleType


class ExpectedFilesRecord(BaseModel):
    company_expected_file_id: Optional[UUID4] = Field(
        None,
        title="Expected File ID",
        description="Unique identifier for the expected file.",
    )
    file_name: str = Field(
        None,
        title="File Name",
        description="Name of the file.",
        max_length=255,
    )
    schedule: ScheduleType = Field(
        None,
        title="Schedule",
        description="Schedule for the file.",
    )
    file_loaded: bool = Field(
        False,
        title="File Loaded",
        description="Flag indicating if the file has been loaded per its schedule.",
    )
    next_file_date: Optional[datetime] = Field(
        None,
        title="Next File Date",
        description="Next date the file is expected to be processed.",
    )
    last_file_date: Optional[datetime] = Field(
        None,
        title="Last File Date",
        description="Last date the file was processed.",
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="Date and time the record was created.",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Updated At",
        description="Date and time the record was updated.",
    )
