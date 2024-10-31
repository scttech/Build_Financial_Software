import re

from psycopg.rows import class_row

from chapter11.v1.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter11.v1.AchParser.ach_processor.schemas.api.transaction_search_response import (
    TransactionSearchResponse,
)


class TransactionSearchSql:

    def get_sql_selection_query(self):
        return """
               SELECT art1.ach_files_id AS file_id, 
                      art5.ach_records_type_5_id AS batch_header_id, 
                      art6.ach_records_type_6_id AS entry_id, 
                      af.file_name AS filename, 
                      aepd.individual_name AS individual_name,
                      aepd.amount AS amount 
                 FROM ach_files af
           INNER JOIN ach_records_type_1 art1 USING ( ach_files_id )
           INNER JOIN ach_records_type_5 art5 USING ( ach_records_type_1_id )
           INNER JOIN ach_records_type_6 art6 USING ( ach_records_type_5_id )
           INNER JOIN ach_entry_ppd_details aepd USING ( ach_records_type_6_id )        
        """

    def _get_transactions_using_individual_name(
        self, criteria: str
    ) -> list[TransactionSearchResponse]:
        with get_db_connection(
            row_factory=class_row(TransactionSearchResponse)
        ) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE aepd.individual_name ILIKE %s"
            result = conn.execute(sql, [criteria])
            return result.fetchall()

    def _get_transactions_using_amount(
        self, criteria: str
    ) -> list[TransactionSearchResponse]:
        with get_db_connection(
            row_factory=class_row(TransactionSearchResponse)
        ) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE aepd.amount = %s"
            result = conn.execute(sql, [criteria])
            return result.fetchall()

    def _get_transactions_using_amount_range(
        self, begin_amount: str, end_amount: str
    ) -> list[TransactionSearchResponse]:
        with get_db_connection(
            row_factory=class_row(TransactionSearchResponse)
        ) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE aepd.amount BETWEEN %s AND %s"
            result = conn.execute(sql, [begin_amount, end_amount])
            return result.fetchall()

    def get_transactions(self, criteria: str) -> list[TransactionSearchResponse]:
        amount_pattern = r"^\d+\.\d{2}$"
        multiple_amounts_pattern = r"(^\d+\.\d{2})\s+(\d+\.\d{2})$"
        if re.match(amount_pattern, criteria):
            return self._get_transactions_using_amount(criteria)
        elif match := re.match(multiple_amounts_pattern, criteria):
            begin_amount, end_amount = match.groups()
            return self._get_transactions_using_amount_range(begin_amount, end_amount)
        else:
            return self._get_transactions_using_individual_name(criteria)
