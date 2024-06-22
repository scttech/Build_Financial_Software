from uuid import UUID

from psycopg.rows import class_row

from chapter11.v4.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter11.v4.AchParser.ach_processor.schemas.database.ach_batch_control_schema import (
    AchBatchControlSchema,
)


class AchBatchControlSql:

    def insert_record(self, ach_batch_header: AchBatchControlSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
           INSERT INTO ach_batch_control_records (ach_records_type_8_id, record_type_code,
            service_class_code, entry_addenda_count, entry_hash, total_debit_entry_dollar_amount,
            total_credit_entry_dollar_amount, company_identification, message_authentication_code,
            reserved, originating_dfi_identification, batch_number)
        VALUES (%(ach_records_type_8_id)s, %(record_type_code)s, %(service_class_code)s, %(entry_addenda_count)s,
            %(entry_hash)s, %(total_debit_entry_dollar_amount)s, %(total_credit_entry_dollar_amount)s,
            %(company_identification)s, %(message_authentication_code)s, %(reserved)s,
            %(originating_dfi_identification)s, %(batch_number)s)
            """,
                ach_batch_header.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchBatchControlSchema:
        with get_db_connection(row_factory=class_row(AchBatchControlSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_batch_control_records WHERE ach_records_type_8_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
