from pydantic import BaseModel, UUID4


class AchBatchHeaderSchema(BaseModel):
    ach_records_type_5_id: UUID4
    record_type_code: str
    service_class_code: str
    company_name: str
    company_discretionary_data: str
    company_identification: str
    standard_entry_class_code: str
    company_entry_description: str
    company_descriptive_date: str
    effective_entry_date: str
    settlement_date: str
    originator_status_code: str
    originating_dfi_identification: str
    batch_number: str
