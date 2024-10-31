from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, UUID4


class TransactionSearchResponse(BaseModel):
    file_id: UUID4 = Field(
        ..., description="Unique identifier for the ACH file.", title="File ID"
    )
    batch_header_id: UUID4 = Field(
        ...,
        description="Unique identifier for the ACH Batch Header.",
        title="Batch Header ID",
    )
    entry_id: UUID4 = Field(
        ...,
        description="Unique identifier for the ACH Entry Detail.",
        title="Entry Detail ID",
    )
    filename: str = Field(
        ..., description="The name of the ACH file.", title="Filename", max_length=255
    )
    individual_name: str = Field(
        ...,
        description="The name of the individual or company for the entry.",
        title="Individual Name",
        max_length=22,
    )
    amount: Annotated[
        Decimal,
        Field(
            ...,
            description="The amount of the entry.",
            title="Amount",
            max_digits=10,
            decimal_places=2,
        ),
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "123e4567-e89b-12d3-a456-426614174000",
                "record_type_5_id": "123e4567-e89b-12d3-a456-426614174001",
                "record_type_6_id": "123e4567-e89b-12d3-a456-426614174002",
                "filename": "test.ach",
                "individual_name": "John Doe",
                "amount": "100.00",
            }
        }
