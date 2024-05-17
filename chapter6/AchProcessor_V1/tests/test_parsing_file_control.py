from typing import Dict

import pytest
from ach_processor.AchFileProcessor import AchFileProcessor
from psycopg.rows import dict_row
from tests.SqlUtils import SqlUtils

TABLE_NAME: str = "ach_file_control_records"

@pytest.fixture
def setup_teardown_method():
    print("\nsetup test\n")
    yield
    print("\nteardown test\n")
    with SqlUtils.get_db() as conn:
        conn.execute(f"TRUNCATE {TABLE_NAME}")

def test_parse_file_header(setup_teardown_method):
    sample_file_control = "9000010000010000000740198019800000000007825000114611480"

    expected_result: Dict[str:str] = {
        "record_type_code": "9",
        "batch_count": "000010",
        "block_count": "000010",
        "entry_addenda_count": "00000074",
        "entry_hash": "0198019800",
        "total_debit_entry_dollar_amount": "000000007825",
        "total_credit_entry_dollar_amount": "000114611480",
        "reserved": ""
    }

    parser = AchFileProcessor()
    with SqlUtils.get_db() as conn:
        result = parser._parse_file_control(conn, sample_file_control)

    with SqlUtils.get_db(dict_row) as conn:
        actual_result = conn.execute(f"SELECT * FROM {TABLE_NAME}").fetchone()
        del actual_result["ach_file_control_records_id"]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"
