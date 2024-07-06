import pytest
from psycopg.rows import dict_row

from chapter6.AchProcessor.ach_processor.AchFileProcessor import AchFileProcessor
from chapter6.AchProcessor.tests.SqlUtils import SqlUtils


@pytest.fixture
def setup_teardown_method():
    print("\nsetup test\n")
    yield
    print("\nteardown test\n")
    with SqlUtils.get_db() as conn:
        conn.execute("TRUNCATE ach_batch_headers")

# Define a test function to test parsing an ACH batch header record using AchFileProcessor._parse_batch_header()
def test_parse_batch_header():
    # Define a sample ACH batch header record
    sample_batch_header = "5200Company name    DiscretionaryData   Company IDARCComp desc 0216232302160471061000010000001"

    # Define the expected result of parsing the sample ACH batch header record
    expected_result = {
        "record_type_code": "5",
        "service_class_code": "200",
        "company_name": "Company name",
        "company_discretionary_data": "DiscretionaryData",
        "company_identification": "Company ID",
        "standard_entry_class_code": "ARC",
        "company_entry_description": "Comp desc",
        "company_descriptive_date": "021623",
        "effective_entry_date": "230216",
        "settlement_date": "047",
        "originator_status_code": "1",
        "originating_dfi_identification": "0610000",
        "batch_number": "0000001",
    }

    # Create an instance of AchFileProcessor
    parser = AchFileProcessor()

    # Call AchFileProcessor._parse_batch_header() with the sample ACH batch header record
    with SqlUtils.get_db() as conn:
        result = parser._parse_batch_header(conn, sample_batch_header)

    with SqlUtils.get_db(dict_row) as conn:
        actual_result = conn.execute("SELECT * FROM ach_batch_headers").fetchone()
        del actual_result["ach_batch_headers_id"]

    # Assert that the result of parsing the sample ACH batch header record matches the expected result
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"
