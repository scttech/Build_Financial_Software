from decimal import Decimal

from pydantic import BaseModel, UUID4


class AchEntryPpdDetailsSchema(BaseModel):
    ach_records_type_6_id: UUID4
    record_type_code: str
    transaction_code: int
    receiving_dfi_identification: str
    check_digit: str
    dfi_account_number: str
    amount: Decimal
    individual_identification_number: str
    individual_name: str
    discretionary_data: str
    addenda_record_indicator: str
    trace_number: str
