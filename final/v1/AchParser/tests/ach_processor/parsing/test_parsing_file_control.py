from decimal import Decimal
from typing import Dict

import pytest

from final.v1.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from final.v1.AchParser.ach_processor.database.ach_file_control_sql import (
    AchFileControlSql,
)
from final.v1.AchParser.tests.ach_processor.sql_utils import SqlUtils

TABLE_NAME: str = "ach_file_control_records"


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_parse_file_header():
    sample_file_control = "9000010000010000000740198019800000000007825000114611480"

    expected_result: Dict[str:str] = {
        "record_type_code": "9",
        "batch_count": "000010",
        "block_count": "000010",
        "entry_addenda_count": 74,
        "entry_hash": "0198019800",
        "total_debit_entry_dollar_amount": Decimal("78.25"),
        "total_credit_entry_dollar_amount": Decimal("1146114.80"),
        "reserved": "",
    }

    parser = AchFileProcessor()

    ach_file_header_record_id, ach_file_control_record_id = (
        SqlUtils.setup_file_control_test(sample_file_control)
    )
    parser._parse_file_control(ach_file_control_record_id, sample_file_control)

    sql = AchFileControlSql()
    retrieved_record = sql.get_record(ach_file_control_record_id).model_dump()
    del retrieved_record["ach_records_type_9_id"]

    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert (
        retrieved_record == expected_result
    ), f"Expected {expected_result}, but got {retrieved_record}"
