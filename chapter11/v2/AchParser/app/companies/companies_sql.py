from psycopg.rows import class_row, dict_row
from uuid import UUID
from chapter11.v2.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter11.v2.AchParser.app.companies.company_detail_record import (
    CompanyDetailRecord,
)
from chapter11.v2.AchParser.app.companies.company_overview_record import (
    CompanyOverviewRecord,
)
from chapter11.v2.AchParser.common.address.address import Address
from chapter11.v2.AchParser.common.phone.phone import Phone


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

    def get_company_by_id(self, company_id: UUID) -> CompanyDetailRecord:
        """Get specific record"""
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
                SELECT c.company_id, c.name, c.tax_id_type, c.tax_id_number, c.duns, c.logo, c.website, c.industry, 
                       ca.company_address_id, ca.address_type, ca.address_type, ca.address_line_1, ca.address_line_2, 
                       ca.address_line_3, ca.address_line_4, ca.city, ca.state, ca.zip_code, ca.zip_code_4, 
                       cp.company_phone_id, cp.phone_type, cp.phone_number, cp.extension
                  FROM companies AS c
            INNER JOIN company_addresses AS ca USING (company_id)
            INNER JOIN company_phones AS cp USING (company_id)
            WHERE company_id = %s   
                """,
                [company_id.hex],
            )

        rows = result.fetchall()

        if not rows:
            raise KeyError(f"Record with id {company_id} not found")

            # Group rows by company
        addresses = []
        phones = []
        for row in rows:
            addresses.append(
                Address(
                    address_id=row["company_address_id"],
                    address_type=row["address_type"],
                    address_line_1=row["address_line_1"],
                    address_line_2=row["address_line_2"],
                    address_line_3=row["address_line_3"],
                    address_line_4=row["address_line_4"],
                    city=row["city"],
                    state=row["state"],
                    zip_code=row["zip_code"],
                    zip_code_4=row["zip_code_4"],
                )
            )
            phones.append(
                Phone(
                    phone_id=row["company_phone_id"],
                    phone_type=row["phone_type"],
                    phone_number=row["phone_number"],
                    extension=row["extension"],
                )
            )

        company_data = {
            "company_id": rows[0]["company_id"],
            "name": rows[0]["name"],
            "tax_id_type": rows[0]["tax_id_type"],
            "tax_id_number": rows[0]["tax_id_number"],
            "duns": rows[0]["duns"],
            "logo": rows[0]["logo"],
            "website": rows[0]["website"],
            "industry": rows[0]["industry"],
            "addresses": addresses,
            "phones": phones,
        }

        return CompanyDetailRecord(**company_data)
