import os

import pytest

from AchFileProcessor import AchFileProcessor


@pytest.fixture()
def parser() -> AchFileProcessor:
    parser = AchFileProcessor()
    yield parser


def test_missing_addenda_records(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_missing_addenda.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_message: str = "Unexpected record type"

    records, exceptions = parser.parse(file_path)

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_message
    ), f"Expected {expected_exceptions_message}, but got {exceptions[0]}"


def test_extra_addenda_records(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_extra_addenda.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_message: str = "Unexpected record type"

    records, exceptions = parser.parse(file_path)

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_message
    ), f"Expected {expected_exceptions_message}, but got {exceptions[0]}"
