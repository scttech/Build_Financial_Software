import pytest

from chapter7.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter7.v2.AchParser.ach_processor.database.ach_addenda_ppd_sql import (
    AchAddendaPpdSql,
)
from chapter7.AchParserMvp.tests.ach_processor.sql_utils import SqlUtils

TABLE_NAME: str = "ach_addenda_ppd_records"


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_parse_addenda_ppd_records():
    # Define a sample ACH addenda record
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

    ach_records_type_6_id, ach_records_type_7_id = SqlUtils.setup_addenda_ppd_test(
        sample_addenda_record
    )

    parser._parse_addenda_ppd(ach_records_type_7_id, sample_addenda_record)

    sql = AchAddendaPpdSql()
    retrieved_record = sql.get_record(ach_records_type_7_id).model_dump()
    del retrieved_record["ach_records_type_7_id"]

    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert (
        retrieved_record == expected_result
    ), f"Expected {expected_result}, but got {retrieved_record}"
