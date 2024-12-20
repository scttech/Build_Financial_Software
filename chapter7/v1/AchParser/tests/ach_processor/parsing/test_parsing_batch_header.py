import pytest

from chapter7.v1.AchParser.ach_processor.ach_file_processor import (
    AchFileProcessor,
)
from chapter7.v1.AchParser.ach_processor.database.ach_batch_header_sql import (
    AchBatchHeaderSql,
)
from chapter7.AchParserMvpNoSignOnScreen.tests.ach_processor.sql_utils import SqlUtils

TABLE_NAME: str = "ach_batch_headers"


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


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

    ach_file_header_record_id, ach_batch_header_record_id = (
        SqlUtils.setup_batch_header_test(sample_batch_header)
    )
    parser._parse_batch_header(ach_batch_header_record_id, sample_batch_header)

    # Call AchFileProcessor._parse_batch_header() with the sample ACH batch header record
    # we must remove any id fields from the result because they are generated by the database and we
    # will not know them in advance
    sql = AchBatchHeaderSql()
    retrieved_record = sql.get_record(ach_batch_header_record_id).model_dump()
    del retrieved_record["ach_records_type_5_id"]

    # Assert that the result of parsing the sample ACH batch header record matches the expected result
    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert (
        retrieved_record == expected_result
    ), f"Expected {expected_result}, but got {retrieved_record}"
