import pytest
from psycopg.rows import dict_row
from chapter6.AchProcessor_V1.tests.SqlUtils import SqlUtils
from chapter6.AchProcessor_V1.ach_processor.AchFileProcessor import AchFileProcessor


TABLE_NAME: str = "ach_addenda_ppd_records"

@pytest.fixture
def setup_teardown_method():
    yield
    SqlUtils.truncate(TABLE_NAME)

def test_parse_addenda_ppd_records(setup_teardown_method):
    # Define a sample ACH batch header record
    sample_addenda_record = "705Test 2                                                                          00020003001"

    # Define the expected result of parsing the sample ACH entry detail record
    expected_result = {
        "record_type_code": "7",
        "addenda_type_code": "05",
        "payment_related_information": "Test 2",
        "addenda_sequence_number": "0002",
        "entry_detail_sequence_number": "0003001",
    }

    parser = AchFileProcessor()

    with SqlUtils.get_db() as conn:
        result = parser._parse_addenda_ppd(conn, sample_addenda_record)

    with SqlUtils.get_db(dict_row) as conn:
        actual_result = conn.execute(f"SELECT * FROM {TABLE_NAME}").fetchone()
        del actual_result["ach_addenda_ppd_records_id"]

    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"
