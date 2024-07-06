from uuid import UUID

from psycopg.rows import class_row

from chapter12.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v3.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_batch_header_schema import (
    AchIatBatchHeaderSchema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_batch_header_schema import (
    AchBatchHeaderSchema,
)


class AchIatBatchHeaderSql:

    @staticmethod
    def insert_record(ach_iat_batch_header: AchIatBatchHeaderSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
   INSERT INTO ach_iat_batch_headers (
        ach_records_type_5_id, 
        record_type_code, 
        service_class_code, 
        iat_indicator,
        foreign_exchange_indicator, 
        foreign_exchange_ref_indicator, 
        foreign_exchange_reference, 
        iso_destination_country_code, 
        originator_id, 
        standard_entry_class_code, 
        company_entry_description, 
        iso_originating_currency_code, 
        iso_destination_currency_code, 
        effective_entry_date, 
        settlement_date, 
        originator_status_code, 
        originating_dfi_identification, 
        batch_number
    ) VALUES (
        %(ach_records_type_5_id)s, 
        %(record_type_code)s, 
        %(service_class_code)s, 
        %(iat_indicator)s,
        %(foreign_exchange_indicator)s, 
        %(foreign_exchange_ref_indicator)s, 
        %(foreign_exchange_reference)s, 
        %(iso_destination_country_code)s, 
        %(originator_id)s, 
        %(standard_entry_class_code)s, 
        %(company_entry_description)s, 
        %(iso_originating_currency_code)s, 
        %(iso_destination_currency_code)s, 
        %(effective_entry_date)s, 
        %(settlement_date)s, 
        %(originator_status_code)s, 
        %(originating_dfi_identification)s, 
        %(batch_number)s
    )
            """,
                ach_iat_batch_header.model_dump(),
            )

    @staticmethod
    def get_record(ach_batch_headers_id: UUID) -> AchIatBatchHeaderSchema:
        with get_db_connection(row_factory=class_row(AchIatBatchHeaderSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_batch_headers WHERE ach_records_type_5_id = %s
                """,
                [ach_batch_headers_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_batch_headers_id} not found")

        return record
