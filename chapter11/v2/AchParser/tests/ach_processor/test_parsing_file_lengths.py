import os
from typing import Generator

import pytest

from chapter11.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v2.AchParser.tests.ach_processor.sql_utils import SqlUtils


@pytest.fixture()
def parser() -> Generator[AchFileProcessor, None, None]:
    yield AchFileProcessor()


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_good_file(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample.ach")

    expected_exceptions_result: int = 0
    expected_records_result: int = 41

    ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")

    parser.parse(ach_file_id, file_path)
    exceptions = SqlUtils.get_exceptions()

    with SqlUtils.get_db() as conn:
        record_count = conn.execute(
            "SELECT COUNT(*) FROM ach_records_type_1"
        ).fetchone()[0]
        record_count += conn.execute(
            "SELECT COUNT(*) FROM ach_records_type_5"
        ).fetchone()[0]
        record_count += conn.execute(
            "SELECT COUNT(*) FROM ach_records_type_6"
        ).fetchone()[0]
        record_count += conn.execute(
            "SELECT COUNT(*) FROM ach_records_type_7"
        ).fetchone()[0]
        record_count += conn.execute(
            "SELECT COUNT(*) FROM ach_records_type_8"
        ).fetchone()[0]
        record_count += conn.execute(
            "SELECT COUNT(*) FROM ach_records_type_9"
        ).fetchone()[0]

    assert (
        record_count == expected_records_result
    ), f"Expected {expected_records_result}, but got {record_count}"

    assert (
        len(exceptions) == expected_exceptions_result
    ), f"Expected {expected_exceptions_result}, but got {len(exceptions)}"


def test_file_with_invalid_length(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_short_lines_1.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_code: str = "001"

    ach_file_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")

    parser.parse(ach_file_id, file_path)
    exceptions = SqlUtils.get_exceptions()

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_code
    ), f"Expected {expected_exceptions_code}, but got {exceptions[0]}"
