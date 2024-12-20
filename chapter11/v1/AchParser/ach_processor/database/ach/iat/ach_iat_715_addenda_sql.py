from uuid import UUID

from psycopg.rows import class_row

from chapter11.v1.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_710_addenda_schema import (
    AchIat710AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_711_addenda_schema import (
    AchIat711AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_712_addenda_schema import (
    AchIat712AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_713_addenda_schema import (
    AchIat713AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_714_addenda_schema import (
    AchIat714AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_715_addenda_schema import (
    AchIat715AddendaSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach.iat.ach_iat_entry_details_schema import (
    AchIatEntryDetailsSchema,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.ach_entry_ppd_details_schema import (
    AchEntryPpdDetailsSchema,
)


class AchIat715AddendaSql:

    def insert_record(self, ach_iat_addenda: AchIat715AddendaSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
  INSERT INTO ach_iat_addenda_715_records (
        ach_records_type_7_id,
        addenda_type_code,
        receiver_identification_number,
        receiver_street_address,
        entry_detail_sequence_number
    ) VALUES (
        %(ach_records_type_7_id)s,
        %(addenda_type_code)s,
        %(receiver_identification_number)s,
        %(receiver_street_address)s,
        %(entry_detail_sequence_number)s
    )                
            """,
                ach_iat_addenda.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchIat715AddendaSchema:
        with get_db_connection(row_factory=class_row(AchIat715AddendaSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_iat_addenda_715_records WHERE ach_records_type_7_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
