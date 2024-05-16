from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, UUID4, Field


class AchBatchesResponse(BaseModel):
    id: UUID4 = Field(
        ..., description="Unique identifier for the ACH batch", title="ID"
    )
    company_name: str = Field(
        ..., description="The name of the company.", title="Company Name", max_length=16
    )
    batch_number: int = Field(
        ...,
        title="Batch Number",
        description="The number associated with the batch.",
        ge=0,
        le=9999999,
    )
    credit_total: Annotated[
        Decimal,
        Field(
            description="The total amount of credit transactions in the ACH batch.",
            title="Credit Total",
            max_digits=12,
            decimal_places=2,
        ),
    ]
    debit_total: Annotated[
        Decimal,
        Field(
            description="The total amount of debit transactions in the ACH batch.",
            title="Debit Total",
            max_digits=12,
            decimal_places=2,
        ),
    ]
    company_id: str = Field(
        ...,
        description="The company identification number.",
        title="Company Identification",
        max_length=10,
    )
    entry_addenda_count: int = Field(
        ...,
        description="The number of addenda records in the ACH batch.",
        title="Entry Addenda Count",
        ge=0,
        le=999999,
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "company_name": "Company Name",
                "company_id": "1234567890",
                "batch_number": 1,
                "credit_total": "100.00",
                "debit_total": "100.00",
                "entry_addenda_count": 2,
            }
        }
