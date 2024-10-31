import os

import pytest

from chapter5.AchProcessor.ach_processor.AchFileProcessor import AchFileProcessor
from chapter5.AchProcessor.tests.SqlUtils import SqlUtils


@pytest.fixture()
def parser() -> AchFileProcessor:
    parser = AchFileProcessor()
    yield parser


@pytest.fixture()
def setup_teardown_method():
    yield
    SqlUtils.truncate_all()


def test_good_file(setup_teardown_method, parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample.ach")

    expected_exceptions_result: int = 0
    expected_records_result: int = 41

    records = parser.parse(file_path)
    exceptions = SqlUtils.get_exceptions()

    assert (
        len(records) == expected_records_result
    ), f"Expected {expected_records_result}, but got {len(records)}"

    assert (
        len(exceptions) == expected_exceptions_result
    ), f"Expected {expected_exceptions_result}, but got {len(exceptions)}"


def test_file_with_invalid_length(setup_teardown_method, parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_short_lines_1.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_message: str = "Invalid line length"

    records = parser.parse(file_path)
    exceptions = SqlUtils.get_exceptions()

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_message
    ), f"Expected {expected_exceptions_message}, but got {exceptions[0]}"
