from uuid import UUID

from psycopg.rows import class_row, dict_row

from chapter12.v4.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter12.v4.AchParser.app.companies.company_detail_record import (
    CompanyDetailRecord,
)
from chapter12.v4.AchParser.app.companies.company_overview_record import (
    CompanyOverviewRecord,
)
from chapter12.v4.AchParser.common.address.address import Address
from chapter12.v4.AchParser.common.phone.phone import Phone


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

    def get_company_by_id_application_logic(
        self, company_id: UUID
    ) -> CompanyDetailRecord:
        """Get specific record
        This method relies on the Python code to filter out the duplicated data for addresses and phones.
        """
        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
                SELECT c.company_id, c.ach_company_id, c.name, c.tax_id_type, c.tax_id_number, c.duns, c.logo,
                       c.website, c.industry, 
                       ca.company_address_id, ca.address_type, ca.address_line_1, ca.address_line_2, 
                       ca.address_line_3, ca.address_line_4, ca.city, ca.state, ca.zip_code, ca.zip_code_4, 
                       cp.company_phone_id, cp.phone_type, cp.phone_number, cp.extension
                  FROM companies AS c
            LEFT JOIN company_addresses AS ca USING (company_id)
            LEFT JOIN company_phones AS cp USING (company_id)
            WHERE company_id = %s   
                """,
                [company_id.hex],
            )

        rows = result.fetchall()

        if not rows:
            raise KeyError(f"Record with id {company_id} not found")

        # Group rows by company
        addresses = {}
        phones = {}
        for row in rows:
            # Add address if not already added
            if row["company_address_id"] not in addresses:
                addresses[row["company_address_id"]] = Address(
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
            # Add phone if not already added
            if row["company_phone_id"] not in phones:
                phones[row["company_phone_id"]] = Phone(
                    phone_id=row["company_phone_id"],
                    phone_type=row["phone_type"],
                    phone_number=row["phone_number"],
                    extension=row["extension"],
                )

        company_data = {
            "company_id": rows[0]["company_id"],
            "name": rows[0]["name"],
            "tax_id_type": rows[0]["tax_id_type"],
            "ach_company_id": rows[0]["ach_company_id"],
            "tax_id_number": rows[0]["tax_id_number"],
            "duns": rows[0]["duns"],
            "logo": rows[0]["logo"],
            "website": rows[0]["website"],
            "industry": rows[0]["industry"],
            "addresses": list(addresses.values()),
            "phones": list(phones.values()),
        }

        return CompanyDetailRecord(**company_data)

    def get_company_by_id(self, company_id: UUID) -> CompanyDetailRecord:
        """Get specific record
        This method relies on the SQL code to filter out the duplicated data for addresses and phones.
        """

        with get_db_connection(row_factory=dict_row) as conn:
            result = conn.execute(
                """
            WITH company_info AS (
                SELECT 
                    c.company_id, 
                    c.ach_company_id, 
                    c.name, 
                    c.tax_id_type, 
                    c.tax_id_number, 
                    c.duns, 
                    c.logo,
                    c.website, 
                    c.industry
                FROM 
                    companies AS c
                WHERE 
                    c.company_id = %s
            ),
            addresses AS (
                SELECT 
                    ca.company_id, 
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'company_address_id', ca.company_address_id,
                            'address_type', ca.address_type,
                            'address_line_1', ca.address_line_1,
                            'address_line_2', ca.address_line_2,
                            'address_line_3', ca.address_line_3,
                            'address_line_4', ca.address_line_4,
                            'city', ca.city,
                            'state', ca.state,
                            'zip_code', ca.zip_code,
                            'zip_code_4', ca.zip_code_4
                        )
                    ) AS addresses
                FROM 
                    company_addresses AS ca
                WHERE 
                    ca.company_id = %s
                GROUP BY 
                    ca.company_id
            ),
            phones AS (
                SELECT 
                    cp.company_id, 
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'company_phone_id', cp.company_phone_id,
                            'phone_type', cp.phone_type,
                            'phone_number', cp.phone_number,
                            'extension', cp.extension
                        )
                    ) AS phones
                FROM 
                    company_phones AS cp
                WHERE 
                    cp.company_id = %s
                GROUP BY 
                    cp.company_id
            )
            SELECT 
                ci.company_id, 
                ci.ach_company_id, 
                ci.name, 
                ci.tax_id_type, 
                ci.tax_id_number, 
                ci.duns, 
                ci.logo,
                ci.website, 
                ci.industry, 
                COALESCE(a.addresses, '[]'::json) AS addresses, 
                COALESCE(p.phones, '[]'::json) AS phones
            FROM 
                company_info AS ci
            LEFT JOIN 
                addresses AS a ON ci.company_id = a.company_id
            LEFT JOIN 
                phones AS p ON ci.company_id = p.company_id;
            """,
                [company_id.hex, company_id.hex, company_id.hex],
            )

        row = result.fetchone()

        if not row:
            raise KeyError(f"Record with id {company_id} not found")

        # Convert the JSON fields into Python objects
        addresses = [Address(**address) for address in row["addresses"]]
        phones = [Phone(**phone) for phone in row["phones"]]

        company_data = {
            "company_id": row["company_id"],
            "name": row["name"],
            "tax_id_type": row["tax_id_type"],
            "ach_company_id": row["ach_company_id"],
            "tax_id_number": row["tax_id_number"],
            "duns": row["duns"],
            "logo": row["logo"],
            "website": row["website"],
            "industry": row["industry"],
            "addresses": addresses,
            "phones": phones,
        }

        return CompanyDetailRecord(**company_data)
