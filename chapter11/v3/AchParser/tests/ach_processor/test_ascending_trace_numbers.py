import os
from typing import Generator

import pytest

from chapter11.v3.AchParser.ach_processor.ach_exceptions import AchExceptions
from chapter11.v3.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v3.AchParser.tests.ach_processor.sql_utils import SqlUtils


@pytest.fixture()
def parser() -> Generator[AchFileProcessor, None, None]:
    parser = AchFileProcessor()
    yield parser


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_file_with_one_trace_error(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_invalid_trace_numbers_1.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_code: str = AchExceptions.TRACE_NUMBER_OUT_OF_ORDER.value

    ach_files_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")

    parser.parse(ach_files_id, file_path)
    exceptions = SqlUtils.get_exceptions()

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_code
    ), f"Expected {expected_exceptions_code}, but got {exceptions[0]}"


def test_file_with_two_trace_errors(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_invalid_trace_numbers_2.ach")

    expected_exceptions_count: int = 2
    expected_exceptions_code: str = "003"

    ach_files_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")

    parser.parse(ach_files_id, file_path)
    exceptions = SqlUtils.get_exceptions()

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_code
    ), f"Expected {expected_exceptions_code}, but got {exceptions[0]}"

    assert (
        exceptions[1] == expected_exceptions_code
    ), f"Expected {expected_exceptions_code}, but got {exceptions[1]}"
