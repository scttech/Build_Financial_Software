import os
import psycopg
import pytest
from tests.SqlUtils import SqlUtils

from ach_processor.AchFileProcessor import AchFileProcessor


@pytest.fixture
def setup_teardown_method():
    print("\nsetup test\n")
    yield
    print("\nteardown test\n")
    SqlUtils.truncate_all()


def test_record_count(setup_teardown_method):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "data", "sample.ach")
    expected_result = 41
    parser = AchFileProcessor()
    records = parser.parse(ach_files_id, file_path)
    with SqlUtils.get_db() as conn:
        record_count = conn.execute("SELECT COUNT(*) FROM ach_files").fetchone()[0]
    assert (
        record_count == expected_result
    ), f"Expected {expected_result}, but got {record_count}"
