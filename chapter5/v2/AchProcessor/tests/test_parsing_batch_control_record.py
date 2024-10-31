import pytest
from psycopg.rows import dict_row

from chapter5.AchProcessor_V1.ach_processor.AchFileProcessor import AchFileProcessor
from chapter5.AchProcessor_V1.tests.SqlUtils import SqlUtils

TABLE_NAME: str = "ach_batch_control_records"


@pytest.fixture
def setup_teardown_method():
    print("\nsetup test\n")
    yield
    print("\nteardown test\n")
    SqlUtils.truncate(TABLE_NAME)


def test_parse_batch_control(setup_teardown_method):
    # Define a sample batch control record
    sample_batch_control_record = "82000000080016501650000000000301000000000302CompID                             061000010000003"

    # Define the expected result of parsing the batch control record
    expected_result = {
        "record_type_code": "8",
        "service_class_code": "200",
        "entry_addenda_count": "000008",
        "entry_hash": "0016501650",
        "total_debit_entry_dollar_amount": "000000000301",
        "total_credit_entry_dollar_amount": "000000000302",
        "company_identification": "CompID",
        "message_authentication_code": "",
        "reserved": "",
        "originating_dfi_identification": "06100001",
        "batch_number": "0000003",
    }

    parser = AchFileProcessor()

    with SqlUtils.get_db() as conn:
        result = parser._parse_batch_control(conn, sample_batch_control_record)

    with SqlUtils.get_db(dict_row) as conn:
        actual_result = conn.execute(f"SELECT * FROM {TABLE_NAME}").fetchone()
        del actual_result["ach_batch_control_records_id"]

    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    assert (
        actual_result == expected_result
    ), f"Expected {expected_result}, but got {actual_result}"
