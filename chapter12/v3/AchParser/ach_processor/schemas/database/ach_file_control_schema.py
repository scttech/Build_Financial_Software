from decimal import Decimal

from pydantic import BaseModel, UUID4


class AchFileControlSchema(BaseModel):
    ach_records_type_9_id: UUID4
    record_type_code: str
    batch_count: str
    block_count: str
    entry_addenda_count: int
    entry_hash: str
    total_debit_entry_dollar_amount: Decimal
    total_credit_entry_dollar_amount: Decimal
    reserved: str

