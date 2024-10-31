from typing import Annotated

from pydantic import BaseModel, UUID4, StringConstraints, field_validator

from chapter11.v1.AchParser.ach_processor.database.bank.bank_routing_sql import (
    BankRoutingSql,
)


class AchFileHeaderSchema(BaseModel):
    ach_records_type_1_id: UUID4
    record_type_code: str
    priority_code: str
    immediate_destination: str
    immediate_origin: str
    file_creation_date: str
    file_creation_time: str
    file_id_modifier: Annotated[
        str, StringConstraints(pattern=r"^[A-Z]$", min_length=1, max_length=1)
    ]
    record_size: str
    blocking_factor: str
    format_code: str
    immediate_destination_name: str
    immediate_origin_name: str
    reference_code: str

    @field_validator("immediate_destination")
    @classmethod
    def validate_immediate_destination(cls, v):
        try:
            if BankRoutingSql().valid_bank_routing_number(v):
                return v
            else:
                raise ValueError("immediate_destination is not a valid routing number")
        except Exception:
            raise ValueError("Unable to validate immediate_destination")
