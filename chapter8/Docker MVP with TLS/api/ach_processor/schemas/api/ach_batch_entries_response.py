from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, UUID4, Field


class AchBatchEntriesResponse(BaseModel):
    id: UUID4 = Field(
        ..., description="Unique identifier for the ACH entry record", title="ID"
    )
    transaction_code: int = Field(
        ..., description="The transaction code for the entry.", title="Transaction Code"
    )
    amount: Annotated[
        Decimal,
        Field(
            description="The amount of the entry.",
            title="Amount",
            max_digits=10,
            decimal_places=2,
        ),
    ]
    account_number_last_4: str = Field(
        ...,
        description="The masked account number for the entry.",
        title="Account Number",
        max_length=17,
    )
    individual_name: str = Field(
        ...,
        description="The name of the individual or company for the entry.",
        title="Individual Name",
        max_length=22,
    )
    addenda_count: int = Field(
        ...,
        description="The number of addenda records for the entry.",
        title="Addenda Count",
    )
    transaction_description: str = Field(
        ...,
        description="The description of the transaction code.",
        title="Transaction Description",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "transaction_code": 22,
                "transaction_description": "Credit",
                "individual_name": "John Doe",
                "amount": "100.00",
                "account_number_last_4": "1234",
                "addenda_count": 2,
            }
        }
