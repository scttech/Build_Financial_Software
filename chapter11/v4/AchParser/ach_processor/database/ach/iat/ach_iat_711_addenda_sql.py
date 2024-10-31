from uuid import UUID

from psycopg.rows import class_row

from chapter11.v4.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter11.v4.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_711_addenda_schema import (
    AchIat711AddendaSchema,
)


class AchIat711AddendaSql:

    def insert_record(self, ach_iat_addenda: AchIat711AddendaSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
  INSERT INTO ach_iat_addenda_11_details (
        ach_records_type_7_id,
        record_type_code,
        addenda_type_code,
        originator_name,
        originator_street_address,
        entry_detail_sequence_number
    ) VALUES (
        %(ach_records_type_7_id)s,
        %(record_type_code)s,
        %(addenda_type_code)s,
        %(originator_name)s,
        %(originator_street_address)s,
        %(entry_detail_sequence_number)s
    )                
            """,
                ach_iat_addenda.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchIat711AddendaSchema:
        with get_db_connection(row_factory=class_row(AchIat711AddendaSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_addenda_11_details WHERE ach_records_type_7_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
