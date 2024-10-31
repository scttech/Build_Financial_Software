from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field, UUID4


class BatchSearchResponse(BaseModel):
    file_id: UUID4 = Field(
        ..., description="Unique identifier for the ACH file.", title="File ID"
    )
    batch_header_id: UUID4 = Field(
        ...,
        description="Unique identifier for the ACH Batch Header.",
        title="Batch Header ID",
    )
    filename: str = Field(
        ..., description="The name of the ACH file.", title="Filename", max_length=255
    )
    company_name: str = Field(
        ...,
        description="The name of the individual or company for the entry.",
        title="Individual Name",
        max_length=255,
    )
    total_credit_entry_dollar_amount: Annotated[
        Decimal,
        Field(
            ...,
            description="The total credit entry dollar amount for the batch.",
            title="Total Credit Entry Dollar Amount",
            max_digits=10,
            decimal_places=2,
        ),
    ]
    total_debit_entry_dollar_amount: Annotated[
        Decimal,
        Field(
            ...,
            description="The debit entry dollar amount for the batch.",
            title="Total Debit Entry Dollar Amount",
            max_digits=10,
            decimal_places=2,
        ),
    ]
    entry_addenda_count: Annotated[
        Decimal,
        Field(
            ...,
            description="The number of entry/addenda records in the batch .",
            title="Entry and Addenda Count",
            max_digits=10,
        ),
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "123e4567-e89b-12d3-a456-426614174000",
                "batch_header_id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "test.ach",
                "company_name": "Petro Power LLC",
                "total_credit_entry_dollar_amount": 100.00,
                "total_debit_entry_dollar_amount": 0.00,
                "entry_addenda_count": 1,
            }
        }
