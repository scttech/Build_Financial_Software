from pydantic import BaseModel, UUID4


class AchFileControlSchema(BaseModel):
    ach_records_id: UUID4
    ach_file_headers_id: UUID4
    record_type_code: str
    batch_count: str
    block_count: str
    entry_addenda_count: str
    entry_hash: str
    total_debit_entry_dollar_amount: str
    total_credit_entry_dollar_amount: str
    reserved: str

