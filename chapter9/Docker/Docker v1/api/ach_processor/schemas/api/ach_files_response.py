from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, UUID4, Field, condecimal
from typing_extensions import Annotated


class AchFilesResponse(BaseModel):
    id: UUID4 = Field(..., description="Unique identifier for the ACH file", title="ID")
    date: datetime = Field(
        ..., description="The date and time the ACH file was uploaded.", title="Date"
    )
    filename: str = Field(
        ...,
        title="Filename",
        description="The name of the file the ACH file was loaded from.",
        max_length=255,
    )
    credit_total: Annotated[
        Decimal,
        Field(
            ...,
            description="The total amount of credit transactions in the ACH file.",
            ge=0,
            title="Credit Total",
            max_digits=12,
            decimal_places=2,
        ),
    ]
    debit_total: Annotated[
        Decimal,
        Field(
            ...,
            description="The total amount of debit transactions in the ACH file.",
            ge=0,
            title="Debit Total",
            max_digits=12,
            decimal_places=2,
        ),
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "date": "2024-01-01T12:00:00",
                "filename": "ACH_20240101_123.ach",
                "credit_total": "1000.80",
                "debit_total": "5000.23",
            }
        }
