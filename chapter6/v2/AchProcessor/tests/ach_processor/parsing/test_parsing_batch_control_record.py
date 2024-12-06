import pytest

from chapter6.v2.AchProcessor.ach_processor.ach_file_processor import AchFileProcessor
from chapter6.v2.AchProcessor.ach_processor.database.ach_batch_control_sql import (
    AchBatchControlSql,
)
from chapter6.v2.AchProcessor.tests.ach_processor.sql_utils import SqlUtils

TABLE_NAME: str = "ach_batch_control_records"


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_parse_batch_control():
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
    ach_batch_header_record_id, ach_batch_control_record_id = (
        SqlUtils.setup_batch_control_test(sample_batch_control_record)
    )

    parser._parse_batch_control(
        ach_batch_control_record_id, sample_batch_control_record
    )

    sql = AchBatchControlSql()
    retrieved_record = sql.get_record(ach_batch_control_record_id).model_dump()
    del retrieved_record["ach_records_type_8_id"]

    assert SqlUtils.get_row_count_of_1(TABLE_NAME), f"Expected 1 row in {TABLE_NAME}"
    assert (
        retrieved_record == expected_result
    ), f"Expected {expected_result}, but got {retrieved_record}"
