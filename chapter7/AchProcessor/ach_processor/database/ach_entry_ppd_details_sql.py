from uuid import UUID

from psycopg.rows import class_row

from chapter7.AchProcessor.ach_processor.database.db_utils import get_db_connection
from chapter7.AchProcessor.ach_processor.schemas.ach_entry_ppd_details_schema import AchEntryPpdDetailsSchema


class AchEntryPpdDetailsSql:

    def insert_record(self, ach_entry_ppd_details: AchEntryPpdDetailsSchema) -> UUID:
        with get_db_connection() as conn:
            conn.execute("""
            INSERT INTO ach_entry_ppd_details (ach_records_type_6_id,record_type_code, transaction_code,
            receiving_dfi_identification, check_digit, dfi_account_number, amount,
            individual_identification_number, individual_name, discretionary_data,
            addenda_record_indicator, trace_number) 
            VALUES (%(ach_records_type_6_id)s, %(record_type_code)s, %(transaction_code)s, %(receiving_dfi_identification)s,
            %(check_digit)s, %(dfi_account_number)s, %(amount)s, %(individual_identification_number)s,
            %(individual_name)s, %(discretionary_data)s, %(addenda_record_indicator)s, %(trace_number)s)
            """, ach_entry_ppd_details.model_dump())

    def get_record(self, ach_records_id: UUID) -> AchEntryPpdDetailsSchema:
        with get_db_connection(row_factory = class_row(AchEntryPpdDetailsSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_entry_ppd_details WHERE ach_records_type_6_id = %s
                """, [ach_records_id.hex])

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record

