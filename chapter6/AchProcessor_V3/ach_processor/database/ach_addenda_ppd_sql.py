from uuid import UUID

from psycopg.rows import class_row

from chapter6.AchProcessor_V3.ach_processor.database.db_utils import get_db_connection
from chapter6.AchProcessor_V3.ach_processor.schemas.ach_addenda_ppd_schema import AchAddendaPpdSchema


class AchAddendaPpdSql:

    def insert_record(self, ach_addenda_ppd: AchAddendaPpdSchema) -> UUID:
        with get_db_connection() as conn:
            conn.execute("""
            INSERT INTO ach_addenda_ppd_records (ach_records_id, ach_entry_ppd_details_id, record_type_code, addenda_type_code,
            payment_related_information, addenda_sequence_number, entry_detail_sequence_number)
            VALUES (%(ach_records_id)s, %(ach_entry_ppd_details_id)s, %(record_type_code)s, %(addenda_type_code)s, %(payment_related_information)s,
            %(addenda_sequence_number)s, %(entry_detail_sequence_number)s)
            """, ach_addenda_ppd.model_dump())

    def get_record(self, ach_records_id: UUID) -> AchAddendaPpdSchema:
        with get_db_connection(row_factory=class_row(AchAddendaPpdSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_addenda_ppd_records WHERE ach_records_id = %s
                """, [ach_records_id.hex])

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record

