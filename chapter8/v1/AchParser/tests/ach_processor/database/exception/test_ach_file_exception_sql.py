import pytest

from chapter8.AchParserV1.ach_processor.database.ach_file_sql import AchFileSql
from chapter8.AchParserV1.ach_processor.database.exception.ach_exceptions_sql import (
    AchExceptionsSql,
)
from chapter8.AchParserV1.ach_processor.schemas.database.ach_file_schema import (
    AchFileSchema,
)
from chapter8.AchParserV1.ach_processor.schemas.database.exception.ach_exception_schema import (
    AchExceptionSchema,
)
from chapter8.AchParserV1.tests.ach_processor.sql_utils import SqlUtils


class TestAchFileExceptionSql:
    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        print("\nsetup test\n")
        SqlUtils.truncate_all()
        yield
        SqlUtils.truncate_all()

    def test_insert_record(self):
        ach_file_record = AchFileSchema(file_name="sample.ach", file_hash="1234567890")
        ach_file_sql = AchFileSql()
        ach_file_id = ach_file_sql.insert_record(ach_file_record)
        ach_file_exception_record = AchExceptionSchema(
            ach_files_id=ach_file_id,
            record_number=1,
            exception_code="001",
        )
        ach_file_exception_sql = AchExceptionsSql()
        exception_id = ach_file_exception_sql.insert_record(ach_file_exception_record)
        retrieved_record = ach_file_exception_sql.get_record(exception_id)
        assert (
            SqlUtils.get_row_count_of_1("ach_exceptions") is True
        ), "Expected 1 record"
        assert (
            retrieved_record.ach_files_id == ach_file_id
        ), f"Expected {ach_file_id}, but got {retrieved_record.ach_files_id}"
        assert (
            retrieved_record.exception_code == "001"
        ), f"Expected '001', but got {retrieved_record.record_number}"
