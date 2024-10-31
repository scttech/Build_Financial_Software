from uuid import UUID

from chapter5.AchProcessor_V2_PreAPICode.ach_processor.database.db_utils import (
    get_db_connection,
)
from chapter5.AchProcessor_V2_PreAPICode.ach_processor.schemas.ach_file_schema import (
    AchFileSchema,
)
from psycopg.rows import class_row


class AchFileSql:
    def insert_record(self, ach_file: AchFileSchema) -> UUID:
        with get_db_connection() as conn:
            result = conn.execute(
                """
                INSERT INTO ach_files(ach_files_id, file_name, file_hash, created_at)
                               VALUES (DEFAULT, %(file_name)s, %(file_hash)s, DEFAULT)
                               RETURNING ach_files_id
                                """,
                ach_file.model_dump(),
            )

        return result.fetchone()[0]

    def get_record(self, ach_file_id: UUID) -> AchFileSchema:
        with get_db_connection(row_factory=class_row(AchFileSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_files WHERE ach_files_id = %s
                """,
                [ach_file_id.hex],
            )

            record = result.fetchone()

            if not record:
                raise KeyError(f"Record with id {ach_file_id} not found")

            return record
