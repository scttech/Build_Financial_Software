from uuid import UUID

from psycopg.rows import class_row

from chapter12.v2.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v2.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_710_addenda_schema import (
    AchIat710AddendaSchema,
)
from chapter12.v2.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_entry_details_schema import (
    AchIatEntryDetailsSchema,
)
from chapter12.v2.AchParser.ach_processor.schemas.database.ach_entry_ppd_details_schema import (
    AchEntryPpdDetailsSchema,
)


class AchIat710AddendaSql:

    def insert_record(self, ach_iat_addenda: AchIat710AddendaSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
  INSERT INTO ach_iat_addenda_710_records (
        ach_records_type_7_id,
        addenda_type_code,
        transaction_type_code,
        foreign_payment_amount,
        foreign_trace_number,
        receiving_name,
        entry_detail_sequence_number
    ) VALUES (
        %(ach_records_type_7_id)s,
        %(addenda_type_code)s,
        %(transaction_type_code)s,
        %(foreign_payment_amount)s,
        %(foreign_trace_number)s,
        %(receiving_name)s,
        %(entry_detail_sequence_number)s
    )                
            """,
                ach_iat_addenda.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchIat710AddendaSchema:
        with get_db_connection(row_factory=class_row(AchIat710AddendaSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_addenda_710_records WHERE ach_records_type_7_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
