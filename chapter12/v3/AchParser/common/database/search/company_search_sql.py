import re
from uuid import UUID
from psycopg.rows import dict_row
from chapter12.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v3.AchParser.app.companies.companies_sql import CompaniesSql
from chapter12.v3.AchParser.app.companies.company_detail_record import (
    CompanyDetailRecord,
)


class CompanySearchSql:

    def get_sql_selection_query(self):
        return """
               SELECT c.company_id
                 FROM companies AS c    
        """

    def _get_company_using_id(self, criteria: str) -> UUID:
        with get_db_connection(row_factory=dict_row) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE c.tax_id_number = %s"
            sql += "   OR c.ach_company_id = %s"
            result = conn.execute(sql, [criteria, criteria])
            row = result.fetchone()

            if not row:
                raise KeyError(f"Record with id {criteria} not found")

            return row["company_id"]

    def _get_company_using_name(self, criteria: str) -> UUID:
        with get_db_connection(row_factory=dict_row) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE c.name = %s"
            result = conn.execute(sql, [criteria])
            row = result.fetchone()

            if not row:
                raise KeyError(f"Record with id {criteria} not found")

            return row["company_id"]

    def _get_company_using_company_uuid(self, criteria: str) -> UUID:
        with get_db_connection(row_factory=dict_row) as conn:
            sql = self.get_sql_selection_query()
            sql += "WHERE c.company_id = %s"
            result = conn.execute(sql, [criteria])
            row = result.fetchone()

            if not row:
                raise KeyError(f"Record with id {criteria} not found")

            return row["company_id"]

    def get_companies(self, criteria: str) -> CompanyDetailRecord:
        company_id_pattern = r"^\d+$"
        company_name_pattern = r"^[a-zA-Z1-9\s]+$"
        if re.match(company_id_pattern, criteria):
            company_id = self._get_company_using_id(criteria)
        elif re.match(company_name_pattern, criteria):
            company_id = self._get_company_using_name(criteria)
        else:
            company_id = self._get_company_using_company_uuid(criteria)

        company_sql = CompaniesSql()
        return company_sql.get_company_by_id(company_id)
