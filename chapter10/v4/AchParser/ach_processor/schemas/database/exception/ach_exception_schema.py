from typing import Optional

from pydantic import BaseModel, Field, UUID4


class AchExceptionSchema(BaseModel):
    ach_exceptions_id: Optional[UUID4] = Field(default=None,
                                                    description="Unique identifier for the ACH file exception",
                                                    title="ach_file_exceptions_id"
                                                    )
    ach_files_id: UUID4 = Field(
        default=..., description="Unique identifier for the ACH file", title="File ID"
    )
    ach_batch_id: Optional[UUID4] = Field(default=None, description="Unique identifier for the ACH record type 5", title="Batch ID")
    ach_entry_id: Optional[UUID4] = Field(default=None, description="Unique identifier for the ACH record type 6", title="Entry ID")
    record_number: int = Field(
        default=..., description="The record number in the ACH file", title="record_number"
    )
    exception_code: str = Field(
        default=..., description="The code associated with the exception", title="exception_code", max_length=3
    )
