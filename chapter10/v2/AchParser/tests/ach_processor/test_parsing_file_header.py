from typing import Dict

import pytest

from chapter10.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter10.v2.AchParser.ach_processor.database.ach_file_header_sql import (
    AchFileHeaderSql,
)
from chapter10.v2.AchParser.tests.ach_processor.sql_utils import SqlUtils


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_parse_file_header():
    sample_header = "101 990000013 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX"

    expected_result: Dict[str:str] = {
        "record_type_code": "1",
        "priority_code": "01",
        "immediate_destination": "990000013",
        "immediate_origin": "691000134",
        "file_creation_date": "040220",
        "file_creation_time": "0830",
        "file_id_modifier": "A",
        "record_size": "094",
        "blocking_factor": "10",
        "format_code": "1",
        "immediate_destination_name": "DEST NAME",
        "immediate_origin_name": "ORIGIN NAME",
        "reference_code": "XXXXXXXX",
    }

    parser = AchFileProcessor()
    ach_record_id = SqlUtils.setup_file_header_test(sample_header)
    parser._parse_file_header(ach_record_id, sample_header)

    result = AchFileHeaderSql().get_record(ach_record_id).model_dump()
    del result["ach_records_type_1_id"]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
