from decimal import Decimal

import pytest

from chapter11.v4.AchParser.ach_processor.database.ach_file_control_sql import (
    AchFileControlSql,
)
from chapter11.v4.AchParser.ach_processor.schemas.database.ach_file_control_schema import (
    AchFileControlSchema,
)
from chapter11.v4.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestAchFileControlSql:
    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        print("\nsetup test\n")
        yield
        SqlUtils.truncate_all()

    def test_insert_record(self):

        sample_file_control_record = (
            "9000010000010000000740198019800000000007825000114611480"
        )
        ach_records_type_1_id, ach_records_type_9_id = SqlUtils.setup_file_control_test(
            sample_file_control_record
        )

        ach_file_control_record = AchFileControlSchema(
            ach_records_type_9_id=ach_records_type_9_id,
            record_type_code="9",
            batch_count="000010",
            block_count="000010",
            entry_addenda_count="00000074",
            entry_hash="0198019800",
            total_debit_entry_dollar_amount=Decimal("78.25"),
            total_credit_entry_dollar_amount=Decimal("1146114.80"),
            reserved="",
        )

        sql = AchFileControlSql()
        sql.insert_record(ach_file_control_record)
        retrieved_record = sql.get_record(ach_records_type_9_id)
        assert (
            SqlUtils.get_row_count_of_1("ach_file_control_records") is True
        ), "Expected 1 record"
        assert (
            retrieved_record == ach_file_control_record
        ), f"Expected {ach_file_control_record}, but got {retrieved_record}"
