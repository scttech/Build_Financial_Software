from psycopg.rows import class_row

from chapter11.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter11.v3.AchParser.common.database.company.company_limits_record import (
    CompanyLimitsRecord,
)


class CompanyLimitsSql:

    def get_company_limits(self, company_id) -> CompanyLimitsRecord:
        with get_db_connection(row_factory=class_row(CompanyLimitsRecord)) as conn:
            result = conn.execute(
                """
                WITH ach_batch_totals AS (
    SELECT
        c.company_id,
        SUM(abcr.total_credit_entry_dollar_amount) AS current_credit_total,
        SUM(abcr.total_debit_entry_dollar_amount) AS current_debit_total
    FROM ach_records_type_5 AS art5
    INNER JOIN ach_records_type_8 AS art8 USING (ach_records_type_5_id)
    INNER JOIN ach_batch_headers AS abh USING (ach_records_type_5_id)
    INNER JOIN ach_batch_control_records AS abcr USING (ach_records_type_8_id)
    INNER JOIN companies AS c ON c.ach_company_id = abh.company_identification AND c.company_id = %s
    GROUP BY c.company_id
)
SELECT cl.company_limit_id,
       cl.daily_debit_limit,
       cl.daily_credit_limit,
       COALESCE(abt.current_credit_total, 0) AS current_credit_total,
       COALESCE(abt.current_debit_total, 0) AS current_debit_total,
       CASE
           WHEN abt.current_credit_total > cl.daily_credit_limit THEN TRUE
           ELSE FALSE
       END AS daily_credit_exceeded,
       CASE
           WHEN abt.current_debit_total > cl.daily_debit_limit THEN TRUE
           ELSE FALSE
       END AS daily_debit_exceeded
FROM company_limits AS cl
LEFT JOIN ach_batch_totals AS abt USING (company_id)
WHERE cl.company_id = %s
                """,
                [company_id, company_id],
            )

        return result.fetchone()

    def file_exceeds_company_limits(self, file_id) -> bool:
        with get_db_connection(row_factory=class_row(CompanyLimitsRecord)) as conn:
            result = conn.execute(
                """
                WITH ach_batch_totals AS (
                    SELECT
                            c.company_id,
                            SUM(abcd.total_credit_entry_dollar_amount) AS current_credit_total,
                            SUM(abcd.total_debit_entry_dollar_amount) AS current_debit_total
                    FROM ach_files AS af
                    INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                    INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                    INNER JOIN ach_records_type_8 AS art8 USING (ach_records_type_5_id)
                    INNER JOIN ach_batch_headers AS abh USING (ach_records_type_5_id)
                    INNER JOIN ach_batch_control_details AS abcd USING (ach_records_type_8_id)
                    INNER JOIN companies AS c ON c.ach_company_id = abh.company_identification
                    WHERE af.ach_files_id = %s
                    GROUP BY c.company_id
                )
                SELECT 1
                FROM ach_files AS af
                INNER JOIN ach_records_type_1 AS art1 USING (ach_files_id)
                INNER JOIN ach_records_type_5 AS art5 USING (ach_records_type_1_id)
                INNER JOIN ach_records_type_8 AS art8 USING (ach_records_type_5_id)
                INNER JOIN ach_batch_headers AS abh USING (ach_records_type_5_id)
                INNER JOIN companies AS c ON c.ach_company_id = abh.company_identification
                INNER JOIN company_limits AS cl USING (company_id)
                LEFT JOIN ach_batch_totals AS abt USING (company_id)
                WHERE af.ach_files_id = %s 
                AND ( abt.current_credit_total > cl.daily_credit_limit
                OR abt.current_debit_total > cl.daily_debit_limit )
                LIMIT 1
                """,
                [file_id, file_id],
            )

        return result.fetchone() is not None
