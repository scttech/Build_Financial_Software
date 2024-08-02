from pydantic import BaseModel, UUID4


class AchAddendaPpdSchema(BaseModel):
    ach_records_id: UUID4
    ach_entry_ppd_details_id: UUID4
    record_type_code: str
    addenda_type_code: str
    payment_related_information: str
    addenda_sequence_number: str
    entry_detail_sequence_number: str