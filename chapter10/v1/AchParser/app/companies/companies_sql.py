from psycopg.rows import class_row

from chapter10.v1.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter10.v1.AchParser.app.companies.company_overview_record import (
    CompanyOverviewRecord,
)


class CompaniesSql:

    def get_all_companies(self) -> list[CompanyOverviewRecord]:
        """Get all records"""
        with get_db_connection(row_factory=class_row(CompanyOverviewRecord)) as conn:
            result = conn.execute(
                """
                SELECT company_id, name, industry, logo FROM companies
                """,
                [],
            )

        records = result.fetchall()

        return records
