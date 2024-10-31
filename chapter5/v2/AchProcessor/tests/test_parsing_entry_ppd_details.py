import pytest
from psycopg.rows import dict_row

from chapter5.AchProcessor_V1.ach_processor.AchFileProcessor import AchFileProcessor
from chapter5.AchProcessor_V1.tests.SqlUtils import SqlUtils

TABLE_NAME: str = "ach_entry_ppd_details"


@pytest.fixture
def setup_teardown_method():
    print("\nsetup test\n")
    yield
    print("\nteardown test\n")
    SqlUtils.truncate(TABLE_NAME)


def test_parse_entry_ppd_details(setup_teardown_method):
    # Define a sample ACH batch header record
    sample_entry_detail_record = "6272670841345                0000000301               0003xxxxxxxxxxxxxxxx  LC1061000010003001"

    # Define the expected result of parsing the sample ACH entry detail record
    expected_result = {
        "record_type_code": "6",
        "transaction_code": "27",
        "receiving_dfi_identification": "26708413",
        "check_digit": "4",
        "dfi_account_number": "5",
        "amount": "0000000301",
        "individual_identification_number": "",
        "individual_name": "0003xxxxxxxxxxxxxxxx",
        "discretionary_data": "LC",
        "addenda_record_indicator": "1",
        "trace_number": "061000010003001",
    }

    parser = AchFileProcessor()

    with SqlUtils.get_db() as conn:
        result = parser._parse_entry_ppd_detail(conn, sample_entry_detail_record)

    with SqlUtils.get_db(dict_row) as conn:
        actual_result = conn.execute(f"SELECT * FROM {TABLE_NAME}").fetchone()
        del actual_result["ach_entry_ppd_details_id"]

    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    assert (
        actual_result == expected_result
    ), f"Expected {expected_result}, but got {actual_result}"
