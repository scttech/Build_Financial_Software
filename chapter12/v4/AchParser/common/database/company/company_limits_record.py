from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, UUID4, Field


class CompanyLimitsRecord(BaseModel):
    company_limit_id: Optional[UUID4] = Field(
        None,
        title="Company Limit ID",
        description="Unique identifier for the company limits.",
    )
    daily_debit_limit: Optional[Decimal] = Field(
        None,
        title="Daily Debit Limit",
        description="The maximum amount of money that can be debited from the company's account in a single day.",
    )
    daily_credit_limit: Optional[Decimal] = Field(
        None,
        title="Daily Credit Limit",
        description="The maximum amount of money that can be credited to the company's account in a single day.",
    )
    current_debit_total: Optional[Decimal] = Field(
        None,
        title="Current Debit Total",
        description="The total amount of money that has been debited from the company's account today.",
    )
    current_credit_total: Optional[Decimal] = Field(
        None,
        title="Current Credit Total",
        description="The total amount of money that has been credited to the company's account today.",
    )
    daily_debit_exceeded: Optional[bool] = Field(
        None,
        title="Debit Exceeded",
        description="Indicates whether the daily debit limit has been exceeded.",
    )
    daily_credit_exceeded: Optional[bool] = Field(
        None,
        title="Credit Exceeded",
        description="Indicates whether the daily credit limit has been exceeded.",
    )
