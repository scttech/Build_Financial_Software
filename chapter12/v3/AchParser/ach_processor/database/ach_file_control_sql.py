from uuid import UUID

from psycopg.rows import class_row

from chapter12.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_file_control_schema import (
    AchFileControlSchema,
)


class AchFileControlSql:

    def insert_record(self, ach_file_control: AchFileControlSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
            INSERT INTO ach_file_control_details (ach_records_type_9_id, record_type_code, batch_count, 
            block_count, entry_addenda_count, entry_hash, total_debit_entry_dollar_amount,
            total_credit_entry_dollar_amount, reserved)
            VALUES (%(ach_records_type_9_id)s, %(record_type_code)s, %(batch_count)s, %(block_count)s,
            %(entry_addenda_count)s, %(entry_hash)s, %(total_debit_entry_dollar_amount)s,
            %(total_credit_entry_dollar_amount)s, %(reserved)s)
            """,
                ach_file_control.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchFileControlSchema:
        with get_db_connection(row_factory=class_row(AchFileControlSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_file_control_details WHERE ach_records_type_9_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
