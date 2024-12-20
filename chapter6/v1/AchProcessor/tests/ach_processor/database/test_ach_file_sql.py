import pytest

from chapter6.v1.AchProcessor.ach_processor.database.ach_file_sql import AchFileSql
from chapter6.v1.AchProcessor.ach_processor.schemas.ach_file_schema import AchFileSchema
from chapter6.v1.AchProcessor.tests.ach_processor.sql_utils import SqlUtils


class TestAchFileSql:
    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        print("\nsetup test\n")
        yield
        SqlUtils.truncate_all()

    def test_insert_record(self):
        ach_file_record = AchFileSchema(file_name="sample.ach", file_hash="1234567890")
        sql = AchFileSql()
        ach_file_id = sql.insert_record(ach_file_record)
        retrieved_record = sql.get_record(ach_file_id)
        assert SqlUtils.get_row_count_of_1("ach_files") is True, "Expected 1 record"
        assert (
            retrieved_record.file_name == ach_file_record.file_name
        ), f"Expected {ach_file_record.file_name}, but got {retrieved_record.file_name}"
