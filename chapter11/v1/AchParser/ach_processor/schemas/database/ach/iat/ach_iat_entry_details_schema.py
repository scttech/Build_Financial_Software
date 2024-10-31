from decimal import Decimal
from pydantic import BaseModel, UUID4, Field


class AchIatEntryDetailsSchema(BaseModel):
    ach_records_type_6_id: UUID4
    record_type_code: str = Field(..., max_length=1)
    transaction_code: int = Field(...)
    receiving_dfi_identification: str = Field(..., max_length=9)
    number_of_addenda: int = Field(..., ge=0, le=9999)
    amount: Decimal = Field(..., ge=0)
    foreign_receivers_account_number: str = Field(..., max_length=35)
    gateway_ofac_screening: bool = Field(default=False)
    secondary_ofac_screening: bool = Field(default=False)
    addenda_record_indicator: str = Field(default="1", max_length=1)
    trace_number: int = Field(..., ge=0)
