from uuid import UUID

from psycopg.rows import class_row

from chapter6.AchProcessor_V1.ach_processor.database import DbUtils
from chapter6.AchProcessor_V1.ach_processor.schemas.AchFileSchema import AchFileSchema


class AchFileSql:
    def insert_record(self, ach_file: AchFileSchema) -> UUID:
        with DbUtils.get_db_connection() as conn:
            result = conn.execute(
                """
                INSERT INTO ach_files(ach_files_id, file_name, file_hash, created_at)
                               VALUES (DEFAULT, %(file_name)s, %(file_hash)s, DEFAULT)
                               RETURNING ach_files_id
                                """, ach_file.model_dump())

        return result.fetchone()[0]

    def get_record(self, ach_file_id: UUID) -> AchFileSchema:
        with DbUtils.get_db_connection(row_factory=class_row(AchFileSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_files WHERE ach_files_id = %s
                """, [ach_file_id.hex])

            record = result.fetchone()

            if not record:
                raise KeyError(f"Record with id {ach_file_id} not found")

            return record

