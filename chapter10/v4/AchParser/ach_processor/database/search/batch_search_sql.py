import re

from psycopg.rows import class_row

from chapter10.v4.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter10.v4.AchParser.ach_processor.schemas.api.batch_search_response import (
    BatchSearchResponse,
)


class BatchSearchSql:

    def get_sql_selection_query(self):
        return """
               SELECT art1.ach_files_id AS file_id,
                      art5.ach_records_type_5_id AS batch_header_id,
                      af.file_name AS filename,
                      COALESCE(c.name, abh.company_name, '') AS company_name,
                      abh.company_identification AS company_identification,
                      abcr.total_credit_entry_dollar_amount AS total_credit_entry_dollar_amount,
                      abcr.total_debit_entry_dollar_amount AS total_debit_entry_dollar_amount,
                      abcr.entry_addenda_count AS entry_addenda_count
                 FROM ach_files af
           INNER JOIN ach_records_type_1 art1 USING ( ach_files_id )
           INNER JOIN ach_records_type_5 art5 USING ( ach_records_type_1_id )
           INNER JOIN ach_records_type_8 art8 USING ( ach_records_type_5_id )
           INNER JOIN ach_batch_headers abh USING ( ach_records_type_5_id )
           INNER JOIN ach_batch_control_records abcr USING ( ach_records_type_8_id )    
            LEFT JOIN companies c ON abh.company_identification = c.ach_company_id    
        """

    def _get_batches_using_company_name(
        self, criteria: str
    ) -> list[BatchSearchResponse]:
        with get_db_connection(row_factory=class_row(BatchSearchResponse)) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE abh.company_name ILIKE %s"
            result = conn.execute(sql, [criteria])
            return result.fetchall()

    def _get_batches_using_company_id(self, criteria: str) -> list[BatchSearchResponse]:
        with get_db_connection(row_factory=class_row(BatchSearchResponse)) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE c.ach_company_id = %s"
            result = conn.execute(sql, [criteria])
            return result.fetchall()

    def _get_batches_using_company_uuid(
        self, criteria: str
    ) -> list[BatchSearchResponse]:
        with get_db_connection(row_factory=class_row(BatchSearchResponse)) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE c.company_id = %s"
            result = conn.execute(sql, [criteria])
            rows = result.fetchall()

            if not rows:
                raise KeyError(f"Record with id {criteria} not found")

            return rows

    def _get_batches_using_amount(self, criteria: str) -> list[BatchSearchResponse]:
        with get_db_connection(row_factory=class_row(BatchSearchResponse)) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE abcr.total_credit_entry_dollar_amount = %s"
            sql += "   OR abcr.total_debit_entry_dollar_amount = %s"
            result = conn.execute(sql, [criteria, criteria])
            return result.fetchall()

    def _get_batches_using_amount_range(
        self, begin_amount: str, end_amount: str
    ) -> list[BatchSearchResponse]:
        with get_db_connection(row_factory=class_row(BatchSearchResponse)) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE aepd.amount BETWEEN %s AND %s"
            sql += "WHERE abcr.total_credit_entry_dollar_amount BETWEEN %s AND %s"
            sql += "   OR abcr.total_debit_entry_dollar_amount BETWEEN %s AND %s"
            result = conn.execute(
                sql, [begin_amount, end_amount, begin_amount, end_amount]
            )
            return result.fetchall()

    def get_batches(self, criteria: str) -> list[BatchSearchResponse]:
        amount_pattern = r"^\d+\.\d{2}$"
        multiple_amounts_pattern = r"(^\d+\.\d{2})\s+(\d+\.\d{2})$"
        company_id_pattern = r"^\d+$"
        company_name_pattern = r"^[a-zA-Z1-9\s]+$"
        if re.match(amount_pattern, criteria):
            return self._get_batches_using_amount(criteria)
        elif match := re.match(multiple_amounts_pattern, criteria):
            begin_amount, end_amount = match.groups()
            return self._get_batches_using_amount_range(begin_amount, end_amount)
        elif re.match(company_id_pattern, criteria):
            return self._get_batches_using_company_id(criteria)
        elif re.match(company_name_pattern, criteria):
            return self._get_batches_using_company_name(criteria)
        else:
            return self._get_batches_using_company_uuid(criteria)
