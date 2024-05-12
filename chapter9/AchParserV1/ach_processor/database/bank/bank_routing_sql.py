
from uuid import UUID
from psycopg.rows import class_row

from ach_processor.database.db_utils import get_db_connection
from ach_processor.schemas.bank.bank_routing_numbers_schema import BankRoutingNumbersSchema
from ach_processor.schemas.database.ach_record.ach_record_schema import AchRecordSchema


class BankRoutingSql:

    def get_records(self, ach_files_id: UUID) -> list[BankRoutingNumbersSchema]:
        with get_db_connection(row_factory=class_row(BankRoutingNumbersSchema)) as conn:
            result = conn.execute(
                """
                SELECT * FROM bank_routing_numbers
                """
            )

        record = result.fetchall()

        return record

    def valid_bank_routing_number(self, bank_routing_number: str) -> bool:
        with get_db_connection() as conn:
            result = conn.execute(
                """
                SELECT * FROM bank_routing_numbers 
                WHERE routing_number = %s
                """,
                [bank_routing_number],
            )

        record = result.fetchone()

        if not record:
            return False

        return True
