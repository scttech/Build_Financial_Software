from decimal import Decimal
from uuid import UUID

import pytest
from chapter11.v3.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v3.AchParser.ach_processor.database.ach_entry_ppd_details_sql import (
    AchEntryPpdDetailsSql,
)
from chapter11.v3.AchParser.tests.ach_processor.sql_utils import SqlUtils

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
        "transaction_code": 27,
        "receiving_dfi_identification": "26708413",
        "check_digit": "4",
        "dfi_account_number": "5",
        "amount": Decimal("3.01"),
        "individual_identification_number": "",
        "individual_name": "0003xxxxxxxxxxxxxxxx",
        "discretionary_data": "LC",
        "addenda_record_indicator": "1",
        "trace_number": "061000010003001",
    }

    parser = AchFileProcessor()

    _, ach_entry_ppd_details_record_id = SqlUtils.setup_entry_ppd_details_test(
        sample_entry_detail_record
    )

    parser._parse_entry_ppd_detail(
        ach_file_id=UUID("27de3869-2f37-42cd-9dfa-993cc6f00241"),
        current_batch_header_id=UUID("af8b2d25-1eea-4a02-a5a5-9cf60d9ecb82"),
        ach_records_type_6_id=ach_entry_ppd_details_record_id,
        sequence_number=1,
        line=sample_entry_detail_record,
    )

    sql = AchEntryPpdDetailsSql()
    retrieved_record = sql.get_record(ach_entry_ppd_details_record_id).model_dump()
    del retrieved_record["ach_records_type_6_id"]

    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert (
        retrieved_record == expected_result
    ), f"Expected {expected_result}, but got {retrieved_record}"
