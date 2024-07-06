from uuid import UUID

from psycopg.rows import class_row

from chapter12.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v3.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_716_addenda_schema import (
    AchIat716AddendaSchema,
)


class AchIat716AddendaSql:

    def insert_record(self, ach_iat_addenda: AchIat716AddendaSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
  INSERT INTO ach_iat_addenda_16_details (
        ach_records_type_7_id,
        record_type_code,
        addenda_type_code,
        receiver_city,
        receiver_state,
        receiver_country,
        receiver_postal_code,
        entry_detail_sequence_number
    ) VALUES (
        %(ach_records_type_7_id)s,
        %(record_type_code)s,
        %(addenda_type_code)s,
        %(receiver_city)s,
        %(receiver_state)s,
        %(receiver_country)s,
        %(receiver_postal_code)s,        
        %(entry_detail_sequence_number)s
    )                
            """,
                ach_iat_addenda.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchIat716AddendaSchema:
        with get_db_connection(row_factory=class_row(AchIat716AddendaSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_addenda_16_details WHERE ach_records_type_7_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
