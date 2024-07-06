import os
import pytest

from chapter12.v3.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter12.v3.AchParser.tests.ach_processor.sql_utils import SqlUtils


@pytest.fixture(autouse=True)
def setup_teardown_method():
    print("\nsetup test\n")
    SqlUtils.truncate_all()
    yield
    print("\nteardown test\n")


def test_record_count():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "../data", "sample.ach")
    expected_result = 29
    parser = AchFileProcessor()
    ach_files_id = SqlUtils.create_ach_file_record("sample.ach", "123456789")
    parser.parse(ach_files_id, file_path)
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
        record_count == expected_result
    ), f"Expected {expected_result}, but got {record_count}"
