from decimal import Decimal

from pydantic import BaseModel, UUID4


class AchBatchControlSchema(BaseModel):
    ach_records_type_8_id: UUID4
    record_type_code: str
    service_class_code: int
    entry_addenda_count: int
    entry_hash: int
    total_debit_entry_dollar_amount: Decimal
    total_credit_entry_dollar_amount: Decimal
    company_identification: str
    message_authentication_code: str
    reserved: str
    originating_dfi_identification: str
    batch_number: int
