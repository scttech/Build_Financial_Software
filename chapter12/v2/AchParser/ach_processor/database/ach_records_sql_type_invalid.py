"""AchRecordsSql is a class that handles the sql queries for ach_records"""

from uuid import UUID

from chapter12.v2.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v2.AchParser.ach_processor.schemas.database.ach_record.ach_record_type_invalid_schema import (
    AchRecordTypeInvalidSchema,
)


class AchRecordsSqlTypeInvalid:
    """AchRecordsSql is a class that handles the sql queries for ach_records"""

    def insert_record(self, ach_records: AchRecordTypeInvalidSchema) -> UUID:
        """Insert a record into the database"""
        with get_db_connection() as conn:
            result = conn.execute(
                """
                INSERT INTO ach_records_type_invalid (ach_files_id, unparsed_record, sequence_number) 
                VALUES (%(ach_files_id)s, %(unparsed_record)s, %(sequence_number)s)
                RETURNING ach_records_type_invalid_id
                """,
                ach_records.model_dump(),
            )
        return result.fetchone()[0]

    def get_record(self, ach_records_id: UUID) -> AchRecordTypeInvalidSchema:
        """Get a record by id"""
        with get_db_connection() as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_records_type_invalid WHERE ach_records_type_invalid_id = %s
                """,
                [ach_records_id.hex],
            )

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
