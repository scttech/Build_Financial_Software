from uuid import UUID

from psycopg.rows import class_row

from chapter12.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v3.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_714_addenda_schema import (
    AchIat714AddendaSchema,
)


class AchIat714AddendaSql:

    def insert_record(self, ach_iat_addenda: AchIat714AddendaSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
  INSERT INTO ach_iat_addenda_14_details (
        ach_records_type_7_id,
        record_type_code,
        addenda_type_code,
        receiving_dfi_name,
        receiving_dfi_identification_qualifier,
        receiving_dfi_identification,
        receiving_dfi_branch_country_code,
        entry_detail_sequence_number
    ) VALUES (
        %(ach_records_type_7_id)s,
        %(record_type_code)s,
        %(addenda_type_code)s,
        %(receiving_dfi_name)s,
        %(receiving_dfi_identification_qualifier)s,
        %(receiving_dfi_identification)s,
        %(receiving_dfi_branch_country_code)s,        
        %(entry_detail_sequence_number)s
    )                
            """,
                ach_iat_addenda.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchIat714AddendaSchema:
        with get_db_connection(row_factory=class_row(AchIat714AddendaSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_addenda_14_details WHERE ach_records_type_7_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
