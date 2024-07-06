from typing import Dict

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
        conn.execute("TRUNCATE ach_file_headers")

def test_parse_file_header(setup_teardown_method):
    sample_header = "101 267084131 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX"

    expected_result: Dict[str:str] = {
        "record_type_code": "1",
        "priority_code": "01",
        "immediate_destination": "267084131",
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
    with SqlUtils.get_db() as conn:
        result = parser._parse_file_header(conn, sample_header)

    with SqlUtils.get_db(dict_row) as conn:
        actual_result = conn.execute("SELECT * FROM ach_file_headers").fetchone()
        del actual_result["ach_file_headers_id"]

    assert result == expected_result, f"Expected {expected_result}, but got {result}"
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"
