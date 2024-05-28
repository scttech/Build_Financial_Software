import os
from typing import Generator

import pytest

from chapter10.v2.AchParser.ach_processor.ach_exceptions import AchExceptions
from chapter10.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter10.v2.AchParser.tests.ach_processor.sql_utils import SqlUtils


@pytest.fixture()
def parser() -> Generator[AchFileProcessor, None, None]:
    parser = AchFileProcessor()
    yield parser


@pytest.fixture(autouse=True)
def setup_teardown_method():
    SqlUtils.truncate_all()
    yield


def test_incorrect_file_id_modifier(parser):
    try:
        process_file_and_verify_exception(
            ach_filename="invalid_file_id.ach",
            expected_exceptions_count=2,
            expected_exceptions_code=AchExceptions.INVALID_FILE_ID_MODIFIER.value,
            parser=parser,
        )
    except Exception as e:
        print(e)


def test_incorrect_immediate_destination(parser):
    process_file_and_verify_exception(
        "invalid_immediate_destination.ach",
        1,
        AchExceptions.INVALID_IMMEDIATE_DESTINATION.value,
        parser,
    )


def process_file_and_verify_exception(
    ach_filename: str,
    expected_exceptions_count: int,
    expected_exceptions_code: str,
    parser: AchFileProcessor,
):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "bad_files", ach_filename)

    ach_files_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")

    parser.parse(ach_files_id, file_path)
    exceptions = SqlUtils.get_exceptions()

    assert (
        len(exceptions) == expected_exceptions_count
    ), f"Expected {expected_exceptions_count}, but got {len(exceptions)}"

    assert (
        exceptions[0] == expected_exceptions_code
    ), f"Expected {expected_exceptions_code}, but got {exceptions[0]}"
