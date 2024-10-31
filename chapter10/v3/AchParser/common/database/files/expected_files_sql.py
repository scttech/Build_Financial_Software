from psycopg.rows import class_row

from chapter10.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter10.v3.AchParser.common.database.files.expected_files_record import (
    ExpectedFilesRecord,
)


class ExpectedFilesSql:

    def get_expected_files_for_company(self, company_id) -> list[ExpectedFilesRecord]:
        with get_db_connection(row_factory=class_row(ExpectedFilesRecord)) as conn:
            result = conn.execute(
                """
                    WITH future_file_dates AS (
                        SELECT ef.company_expected_file_id,
                               ef.company_id,
                               ef.file_name,
                               CASE ef.schedule
                                   WHEN 'daily' THEN ef.last_file_date + INTERVAL '1 day'
                                   WHEN 'weekly' THEN ef.last_file_date + INTERVAL '1 week'
                                   WHEN 'bi-weekly' THEN ef.last_file_date + INTERVAL '2 weeks'
                                   WHEN 'monthly' THEN ef.last_file_date + INTERVAL '1 month'
                                   WHEN 'quarterly' THEN ef.last_file_date + INTERVAL '3 months'
                                   WHEN 'semi-annually' THEN ef.last_file_date + INTERVAL '6 months'
                                   WHEN 'annually' THEN ef.last_file_date + INTERVAL '1 year'
                                   ELSE ef.last_file_date
                               END AS next_file_date
                               FROM company_expected_files AS ef
                               WHERE ef.company_id = %s
                    )
                    SELECT ef.company_expected_file_id,
                           ef.file_name,
                           ef.schedule,
                           ef.last_file_date,
                           ffd.next_file_date,
                           CASE
                              WHEN af.file_name IS NOT NULL AND af.created_at::date = ef.last_file_date::date THEN TRUE
                              ELSE FALSE
                           END AS file_loaded
                      FROM company_expected_files AS ef
                INNER JOIN future_file_dates AS ffd USING (company_expected_file_id)
                 LEFT JOIN ach_files AS af ON ef.file_name = af.file_name
                     WHERE ef.company_id = %s;
                """,
                [company_id, company_id],
            )

        records = result.fetchall()

        return records

    def update_last_file_date(self, file_name: str):
        with get_db_connection() as conn:
            conn.execute(
                """
                    UPDATE company_expected_files
                       SET last_file_date = NOW(),
                           updated_at = NOW()
                     WHERE file_name = %s;
                """,
                [file_name],
            )
