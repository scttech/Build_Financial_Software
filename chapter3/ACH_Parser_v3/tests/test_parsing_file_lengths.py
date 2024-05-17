import os

import pytest

from chapter3.ACH_Parser_v3.AchFileProcessor import AchFileProcessor


@pytest.fixture()
def parser() -> AchFileProcessor:
    parser = AchFileProcessor()
    yield parser


def test_good_file(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample.ach")

    expected_exceptions_result: int = 0
    expected_records_result: int = 41

    records, exceptions = parser.parse(file_path)

    assert (
        len(records) == expected_records_result
    ), f"Expected {expected_records_result}, but got {len(records)}"

    assert (
        len(exceptions) == expected_exceptions_result
    ), f"Expected {expected_exceptions_result}, but got {len(exceptions)}"


def test_file_with_invalid_length(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_short_lines_1.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_message: str = "Invalid line length"

    records, exceptions = parser.parse(file_path)

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_message
    ), f"Expected {expected_exceptions_message}, but got {exceptions[0]}"
