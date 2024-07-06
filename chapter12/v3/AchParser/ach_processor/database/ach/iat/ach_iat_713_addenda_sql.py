from uuid import UUID
from psycopg.rows import class_row
from chapter12.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v3.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_713_addenda_schema import (
    AchIat713AddendaSchema,
)


class AchIat713AddendaSql:

    def insert_record(self, ach_iat_addenda: AchIat713AddendaSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
  INSERT INTO ach_iat_addenda_13_details (
        ach_records_type_7_id,
        record_type_code,
        addenda_type_code,
        originating_dfi_name,
        originating_dfi_identification_qualifier,
        originating_dfi_identification,
        originating_dfi_branch_country_code,
        entry_detail_sequence_number
    ) VALUES (
        %(ach_records_type_7_id)s,
        %(record_type_code)s,
        %(addenda_type_code)s,
        %(originating_dfi_name)s,
        %(originating_dfi_identification_qualifier)s,
        %(originating_dfi_identification)s,
        %(originating_dfi_branch_country_code)s,        
        %(entry_detail_sequence_number)s
    )                
            """,
                ach_iat_addenda.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchIat713AddendaSchema:
        with get_db_connection(row_factory=class_row(AchIat713AddendaSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_addenda_13_details WHERE ach_records_type_7_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
