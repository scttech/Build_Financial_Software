from uuid import UUID

from psycopg.rows import class_row

from chapter11.v1.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter11.v1.AchParser.ach_processor.schemas.api.ach_exception_details_response import (
    AchExceptionDetailsResponse,
)
from chapter11.v1.AchParser.ach_processor.schemas.api.ach_exceptions_response import (
    AchExceptionsResponse,
)
from chapter11.v1.AchParser.ach_processor.schemas.database.exception.ach_exception_schema import (
    AchExceptionSchema,
)


class AchExceptionsSql:
    @staticmethod
    def insert_record(ach_file_exception: AchExceptionSchema) -> UUID:
        with get_db_connection() as conn:
            result = conn.execute(
                """
           INSERT INTO ach_exceptions (ach_files_id, record_number, exception_code)
           VALUES (%(ach_files_id)s, %(record_number)s, %(exception_code)s)
           RETURNING ach_exceptions_id
            """,
                ach_file_exception.model_dump(),
            )

        return result.fetchone()[0]

    @staticmethod
    def get_record(ach_exception_id: UUID) -> AchExceptionSchema:
        with get_db_connection(row_factory=class_row(AchExceptionSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM ach_exceptions
                WHERE ach_exceptions_id = %s
                """,
                [ach_exception_id],
            )

            return result.fetchone()

    @staticmethod
    def get_exceptions_response(
        ach_files_id: UUID = None,
    ) -> list[AchExceptionsResponse]:
        query_parameters = []
        sql = """
                    SELECT
                        afe.ach_exceptions_id AS id,
                        afe.ach_files_id AS file_id,
                        af.file_name AS file_name,
                        af.created_at AS created_at,
                        afe.ach_records_type_5_id AS batch_id,
                        afe.ach_records_type_6_id AS entry_id,
                        afe.record_number AS record_number,
                        afe.exception_code AS exception_code,
                        aec.exception_description AS description
                    FROM ach_exceptions AS afe
                    INNER JOIN ach_exception_codes AS aec USING (exception_code)
                    INNER JOIN ach_files AS af USING (ach_files_id)                    
        """
        if ach_files_id is not None:
            sql += " WHERE afe.ach_files_id = %s"
            query_parameters.append(ach_files_id)

        with get_db_connection(row_factory=class_row(AchExceptionsResponse)) as conn:
            result = conn.execute(sql, query_parameters)
            return result.fetchall()

    @staticmethod
    def get_exception_detail_response(
        file_id, exception_id
    ) -> AchExceptionDetailsResponse:
        with get_db_connection(
            row_factory=class_row(AchExceptionDetailsResponse)
        ) as conn:
            result = conn.execute(
                """
                SELECT
                    ae.ach_exceptions_id AS id,
                    af.created_at AS created_at,
                    ae.exception_code AS exception_code,
                    aec.exception_description AS description,
                    acr.unparsed_record AS unparsed_record
                FROM ach_exceptions AS ae
                INNER JOIN ach_exception_codes AS aec USING (exception_code)
                INNER JOIN ach_files AS af USING (ach_files_id)
                INNER JOIN ach_combined_records AS acr ON ae.ach_files_id = acr.ach_files_id 
                           AND ae.record_number = acr.sequence_number
                WHERE ae.ach_files_id = %s 
                  AND ae.ach_exceptions_id = %s               
        """,
                [file_id, exception_id],
            )
        return result.fetchone()
