from uuid import UUID

from psycopg.rows import class_row

from ach_processor.database.db_utils import get_db_connection
from ach_processor.schemas.database.ach_file_header_schema import AchFileHeaderSchema


class AchFileHeaderSql:

    def insert_record(self, ach_file_header: AchFileHeaderSchema):
        with get_db_connection() as conn:
            conn.execute(
                """
            INSERT INTO ach_file_headers (ach_records_type_1_id,
                           record_type_code, priority_code, immediate_destination, immediate_origin,
                           file_creation_date, file_creation_time, file_id_modifier, record_size,
                           blocking_factor, format_code, immediate_destination_name,
                           immediate_origin_name, reference_code)
                           VALUES (%(ach_records_type_1_id)s, %(record_type_code)s, %(priority_code)s,
                            %(immediate_destination)s, %(immediate_origin)s, %(file_creation_date)s,
                            %(file_creation_time)s, %(file_id_modifier)s, %(record_size)s, %(blocking_factor)s, 
                            %(format_code)s, %(immediate_destination_name)s, %(immediate_origin_name)s,
                            %(reference_code)s)
                            """,
                ach_file_header.model_dump(),
            )

    def get_record(self, ach_records_id: UUID) -> AchFileHeaderSchema:
        with get_db_connection(row_factory=class_row(AchFileHeaderSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_file_headers WHERE ach_records_type_1_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
