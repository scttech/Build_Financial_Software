import os
from typing import Generator

import pytest

from chapter10.v1.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter10.v1.AchParser.tests.ach_processor.sql_utils import SqlUtils


@pytest.fixture()
def parser() -> Generator[AchFileProcessor, None, None]:
    parser = AchFileProcessor()
    yield parser


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_missing_addenda_records(parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_missing_addenda.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_code: str = "002"

    ach_files_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")

    parser.parse(ach_files_id, file_path)
    exceptions = SqlUtils.get_exceptions()

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_code
    ), f"Expected {expected_exceptions_code}, but got {exceptions[0]}"


def test_extra_addenda_records(setup_teardown_method, parser):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample_extra_addenda.ach")

    expected_exceptions_count: int = 1
    expected_exceptions_code: str = "002"

    ach_files_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")

    parser.parse(ach_files_id, file_path)
    exceptions = SqlUtils.get_exceptions()

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_code
    ), f"Expected {expected_exceptions_code}, but got {exceptions[0]}"
