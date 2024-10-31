import pytest

from chapter7.AchParserMvp.ach_processor.ach_file_processor import AchFileProcessor
from chapter7.AchParserMvp.ach_processor.database.ach_entry_ppd_details_sql import (
    AchEntryPpdDetailsSql,
)
from chapter7.AchParserMvp.tests.ach_processor.sql_utils import SqlUtils

TABLE_NAME: str = "ach_entry_ppd_details"


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_parse_entry_ppd_details():
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

    ach_batch_header_record_id, ach_entry_ppd_details_record_id = (
        SqlUtils.setup_entry_ppd_details_test(sample_entry_detail_record)
    )
    parser._parse_entry_ppd_detail(
        ach_entry_ppd_details_record_id, sample_entry_detail_record
    )

    sql = AchEntryPpdDetailsSql()
    retrieved_record = sql.get_record(ach_entry_ppd_details_record_id).model_dump()
    del retrieved_record["ach_records_type_6_id"]

    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert (
        retrieved_record == expected_result
    ), f"Expected {expected_result}, but got {retrieved_record}"
