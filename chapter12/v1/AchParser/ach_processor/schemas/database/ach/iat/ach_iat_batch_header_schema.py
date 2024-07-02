from datetime import datetime

from pydantic import BaseModel, UUID4, Field


class AchIatBatchHeaderSchema(BaseModel):
    ach_records_type_5_id: UUID4 = Field(
        ...,
        description="The id of the ach_records_type_5 record that this record is associated with",
    )
    record_type_code: str = Field(
        ..., description="The code that identifies the type of record", max_length=1
    )
    service_class_code: str = Field(
        ..., description="Identifies the type of service class code", max_length=3
    )
    iat_indicator: str = Field(
        ..., description="Identifies the IAT indicator", max_length=16
    )
    foreign_exchange_indicator: str = Field(
        ..., description="Identifies the foreign exchange indicator", max_length=2
    )
    foreign_exchange_ref_indicator: str = Field(
        ...,
        description="Identifies the foreign exchange reference indicator",
        max_length=1,
    )
    foreign_exchange_reference: str = Field(
        ..., description="Identifies the foreign exchange reference", max_length=15
    )
    iso_destination_country_code: str = Field(
        ..., description="Identifies the ISO destination country code", max_length=2
    )
    originator_id: str = Field(
        ..., description="Identifies the originator id", max_length=10
    )
    standard_entry_class_code: str = Field(
        ..., description="Identifies the standard entry class code", max_length=3
    )
    company_entry_description: str = Field(
        ..., description="Identifies the company entry description", max_length=10
    )
    iso_originating_currency_code: str = Field(
        ..., description="Identifies the ISO originating currency code", max_length=3
    )
    iso_destination_currency_code: str = Field(
        ..., description="Identifies the ISO destination currency code", max_length=3
    )
    effective_entry_date: str = Field(
        ..., description="Identifies the effective entry date", max_length=6
    )
    settlement_date: str = Field(
        ..., description="Identifies the settlement date", max_length=3
    )
    originator_status_code: str = Field(
        ..., description="Identifies the originator status code", max_length=1
    )
    originating_dfi_identification: str = Field(
        ..., description="Identifies the originating DFI identification", max_length=8
    )
    batch_number: int = Field(..., description="Identifies the batch number", ge=0)
