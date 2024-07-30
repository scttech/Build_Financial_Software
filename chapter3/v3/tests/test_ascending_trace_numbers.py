import os

import pytest

from chapter3.v3.ach_processor.AchFileProcessor import AchFileProcessor


@pytest.fixture()
def parser() -> AchFileProcessor:
    parser = AchFileProcessor()
    yield parser


def test_file_with_one_trace_error(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_invalid_trace_numbers_1.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_message: str = "Trace number out of order"

    records, exceptions = parser.parse(file_path)

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_message
    ), f"Expected {expected_exceptions_message}, but got {exceptions[0]}"


def test_file_with_two_trace_errors(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_invalid_trace_numbers_2.ach")

    expected_exceptions_count: int = 2
    expected_exceptions_message: str = "Trace number out of order"

    records, exceptions = parser.parse(file_path)

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_message
    ), f"Expected {expected_exceptions_message}, but got {exceptions[0]}"

    assert (
        exceptions[1] == expected_exceptions_message
    ), f"Expected {expected_exceptions_message}, but got {exceptions[1]}"
