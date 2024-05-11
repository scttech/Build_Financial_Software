from pydantic import BaseModel, UUID4


class AchBatchControlSchema(BaseModel):
    ach_records_id: UUID4
    ach_batch_headers_id: UUID4
    record_type_code: str
    service_class_code: str
    entry_addenda_count: str
    entry_hash: str
    total_debit_entry_dollar_amount: str
    total_credit_entry_dollar_amount: str
    company_identification: str
    message_authentication_code: str
    reserved: str
    originating_dfi_identification: str
    batch_number: str

