"""AchRecordsSql is a class that handles the sql queries for ach_records"""

from uuid import UUID
from psycopg.rows import class_row

from chapter8.AchParserMvp.ach_processor.database.db_utils import get_db_connection
from chapter8.AchParserMvp.ach_processor.schemas.database.ach_record.ach_record_schema import AchRecordSchema


class CombinedAchRecordsSql:
    """AchRecordsSql is a class that handles the sql queries for ach_records"""

    def get_records(self, ach_files_id: UUID) -> list[AchRecordSchema]:
        """Get a record by id"""
        with get_db_connection(row_factory=class_row(AchRecordSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM combined_ach_records WHERE ach_files_id = %s
                """,
                [ach_files_id.hex],
            )

        record = result.fetchall()

        return record

    def get_record(self, ach_files_id: UUID, primary_key: UUID) -> AchRecordSchema:
        """Get a record by id"""
        with get_db_connection() as conn:
            result = conn.execute(
                """
                SELECT * FROM combined_ach_records WHERE ach_files_id = %s AND primary_key = %s
                """,
                [ach_files_id.hex, primary_key.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {primary_key} not found")

        return record
