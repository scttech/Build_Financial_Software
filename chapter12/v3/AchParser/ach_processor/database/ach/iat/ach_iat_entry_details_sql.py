from uuid import UUID

from psycopg.rows import class_row

from chapter12.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v3.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_entry_details_schema import (
    AchIatEntryDetailsSchema,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_entry_ppd_details_schema import (
    AchEntryPpdDetailsSchema,
)


class AchIatEntryDetailsSql:

    def insert_record(self, ach_iat_entry_details: AchIatEntryDetailsSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
     INSERT INTO ach_iat_entry_details (
        ach_records_type_6_id, 
        record_type_code, 
        transaction_code, 
        receiving_dfi_identification,
        number_of_addenda, 
        amount, 
        foreign_receivers_account_number, 
        gateway_ofac_screening, 
        secondary_ofac_screening, 
        addenda_record_indicator, 
        trace_number
    ) VALUES (
        %(ach_records_type_6_id)s, 
        %(record_type_code)s, 
        %(transaction_code)s, 
        %(receiving_dfi_identification)s,
        %(number_of_addenda)s, 
        %(amount)s, 
        %(foreign_receivers_account_number)s, 
        %(gateway_ofac_screening)s, 
        %(secondary_ofac_screening)s, 
        %(addenda_record_indicator)s, 
        %(trace_number)s
    )
            """,
                ach_iat_entry_details.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchIatEntryDetailsSchema:
        with get_db_connection(row_factory=class_row(AchIatEntryDetailsSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_entry_details WHERE ach_records_type_6_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
