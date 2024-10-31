from pydantic import BaseModel, UUID4


class AchFileHeaderSchema(BaseModel):
    ach_records_type_1_id: UUID4
    record_type_code: str
    priority_code: str
    immediate_destination: str
    immediate_origin: str
    file_creation_date: str
    file_creation_time: str
    file_id_modifier: str
    record_size: str
    blocking_factor: str
    format_code: str
    immediate_destination_name: str
    immediate_origin_name: str
    reference_code: str
