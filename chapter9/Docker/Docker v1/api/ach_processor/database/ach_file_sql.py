from typing import Optional
from uuid import UUID

from psycopg.rows import dict_row, class_row

from ach_processor.database.db_utils import get_db_connection
from ach_processor.schemas.api.ach_batches_response import AchBatchesResponse
from ach_processor.schemas.api.ach_files_response import AchFilesResponse
from ach_processor.schemas.database.ach_file_schema import AchFileSchema


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

    def get_records(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[AchFileSchema]:
        with get_db_connection(row_factory=class_row(AchFileSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_files
                LIMIT %s 
                OFFSET %s
                """,
                [limit, offset],
            )

            return result.fetchall()

    def get_files_response(
        self, limit: Optional[int] = 100, offset: Optional[int] = 0
    ) -> list[AchFilesResponse]:
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
                SELECT af.ach_files_id AS id,
                       af.file_name AS filename,
                       af.created_at AS date, 
                       afcr.total_debit_entry_dollar_amount AS debit_total, 
                       afcr.total_credit_entry_dollar_amount AS credit_total 
                FROM ach_files AS af
                INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                INNER JOIN ach_records_type_9 AS art9 USING (ach_records_type_1_id)
                INNER JOIN ach_file_control_records AS afcr USING (ach_records_type_9_id)
                ORDER BY af.created_at DESC
                LIMIT %s
                OFFSET %s                
                """,
                [limit, offset],
            )

            return result.fetchall()

    def get_batches(self, ach_file_id: UUID) -> list[AchBatchesResponse]:
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
                    SELECT abh.company_name AS company_name, 
                           art5.ach_records_type_5_id AS id, 
                           abh.batch_number, 
                           abcr.total_debit_entry_dollar_amount AS debit_total,
                           abcr.total_credit_entry_dollar_amount AS credit_total, 
                           abcr.entry_addenda_count 
                      FROM ach_files AS af
                INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                INNER JOIN ach_records_type_8 AS art8 USING (ach_records_type_5_id)
                INNER JOIN ach_batch_headers AS abh USING (ach_records_type_5_id)
                INNER JOIN ach_batch_control_records AS abcr USING (ach_records_type_8_id)
                     WHERE af.ach_files_id = %s
                  ORDER BY abh.company_name
                """,
                [ach_file_id.hex],
            )

            return result.fetchall()

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
