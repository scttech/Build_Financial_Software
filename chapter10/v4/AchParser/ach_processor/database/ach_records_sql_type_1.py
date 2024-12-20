"""AchRecordsSql is a class that handles the sql queries for ach_records"""

from uuid import UUID

from chapter10.v4.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter10.v4.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_1_schema import (
    AchRecordType1Schema,
)


class AchRecordsSqlType1:
    """AchRecordsSql is a class that handles the sql queries for ach_records"""

    def insert_record(self, ach_records: AchRecordType1Schema) -> UUID:
        """Insert a record into theach_records_sql_type_1.py database"""
        with get_db_connection() as conn:
            result = conn.execute(
                """
                INSERT INTO ach_records_type_1 (ach_files_id, unparsed_record, sequence_number) 
                VALUES (%(ach_files_id)s, %(unparsed_record)s, %(sequence_number)s)
                RETURNING ach_records_type_1_id
                """,
                ach_records.model_dump(),
            )
        return result.fetchone()[0]

    def get_record(self, ach_records_id: UUID) -> AchRecordType1Schema:
        """Get a record by id"""
        with get_db_connection() as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_records_type_1 WHERE ach_records_type_1_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
