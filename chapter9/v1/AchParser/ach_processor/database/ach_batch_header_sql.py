from uuid import UUID

from psycopg.rows import class_row

from chapter9.v1.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter9.v1.AchParser.ach_processor.schemas.database.ach_batch_header_schema import (
    AchBatchHeaderSchema,
)


class AchBatchHeaderSql:

    @staticmethod
    def insert_record(ach_batch_header: AchBatchHeaderSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
          INSERT INTO ach_batch_headers (ach_records_type_5_id, record_type_code, service_class_code, company_name,
            company_discretionary_data, company_identification, standard_entry_class_code, company_entry_description,
            company_descriptive_date, effective_entry_date, settlement_date, originator_status_code,
            originating_dfi_identification, batch_number)
            VALUES (%(ach_records_type_5_id)s, %(record_type_code)s, %(service_class_code)s, %(company_name)s,
            %(company_discretionary_data)s, %(company_identification)s, %(standard_entry_class_code)s,
            %(company_entry_description)s, %(company_descriptive_date)s, %(effective_entry_date)s,
            %(settlement_date)s, %(originator_status_code)s, %(originating_dfi_identification)s,
            %(batch_number)s)
            """,
                ach_batch_header.model_dump(),
            )

    @staticmethod
    def get_record(ach_batch_headers_id: UUID) -> AchBatchHeaderSchema:
        with get_db_connection(row_factory=class_row(AchBatchHeaderSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_batch_headers WHERE ach_records_type_5_id = %s
                """,
                [ach_batch_headers_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_batch_headers_id} not found")

        return record
