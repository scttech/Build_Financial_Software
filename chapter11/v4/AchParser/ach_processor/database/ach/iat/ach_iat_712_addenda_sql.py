from uuid import UUID

from psycopg.rows import class_row

from chapter11.v4.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter11.v4.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_712_addenda_schema import (
    AchIat712AddendaSchema,
)


class AchIat712AddendaSql:

    def insert_record(self, ach_iat_addenda: AchIat712AddendaSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
  INSERT INTO ach_iat_addenda_12_details (
        ach_records_type_7_id,
        record_type_code,
        addenda_type_code,
        originator_city,
        originator_state,
        originator_country,
        originator_postal_code,
        entry_detail_sequence_number
    ) VALUES (
        %(ach_records_type_7_id)s,
        %(record_type_code)s,
        %(addenda_type_code)s,
        %(originator_city)s,
        %(originator_state)s,
        %(originator_country)s,
        %(originator_postal_code)s,        
        %(entry_detail_sequence_number)s
    )                
            """,
                ach_iat_addenda.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchIat712AddendaSchema:
        with get_db_connection(row_factory=class_row(AchIat712AddendaSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_addenda_12_details WHERE ach_records_type_7_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
