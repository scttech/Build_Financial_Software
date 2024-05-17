"""AchRecordsSql is a class that handles the sql queries for ach_records"""
from uuid import UUID

from chapter7.AchProcessor.ach_processor.database.db_utils import get_db_connection
from chapter7.AchProcessor.ach_processor.schemas.ach_record.ach_record_type_9_schema import AchRecordType9Schema


class AchRecordsSqlType9:
    """AchRecordsSql is a class that handles the sql queries for ach_records"""

    def insert_record(self, ach_records: AchRecordType9Schema) -> UUID:
        """Insert a record into the database"""
        with get_db_connection() as conn:
            result = conn.execute("""
                INSERT INTO ach_records_type_9 (ach_records_type_1_id, unparsed_record, sequence_number) 
                VALUES (%(ach_records_type_1_id)s, %(unparsed_record)s, %(sequence_number)s)
                RETURNING ach_records_type_9_id
                """, ach_records.model_dump())
        return result.fetchone()[0]

    def get_record(self, ach_records_id: UUID) -> AchRecordType9Schema:
        """Get a record by id"""
        with get_db_connection() as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_records_type_9 WHERE ach_records_type_9_id = %s
                """, [ach_records_id.hex])

        record = result.fetchone()

        if not record:
            raise KeyError(f"Record with id {ach_records_id} not found")

        return record
