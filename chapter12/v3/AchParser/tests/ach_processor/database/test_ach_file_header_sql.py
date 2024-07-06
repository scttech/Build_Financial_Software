import pytest

from chapter12.v3.AchParser.ach_processor.database.ach_file_header_sql import (
    AchFileHeaderSql,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_file_header_schema import (
    AchFileHeaderSchema,
)
from chapter12.v3.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestAchFileHeaderSql:
    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        print("\nsetup test\n")
        yield
        SqlUtils.truncate_all()

    def test_insert_record(self):
        sample_header = "101 990000013 6910001340402200830A094101DEST NAME              ORIGIN NAME            XXXXXXXX"

        ach_records_type_1_id = SqlUtils.setup_file_header_test(sample_header)
        ach_file_header_record = AchFileHeaderSchema(
            ach_records_type_1_id=ach_records_type_1_id,
            record_type_code="1",
            priority_code="01",
            immediate_destination="990000013",
            immediate_origin="691000134",
            file_creation_date="040220",
            file_creation_time="0830",
            file_id_modifier="A",
            record_size="094",
            blocking_factor="10",
            format_code="1",
            immediate_destination_name="DEST NAME",
            immediate_origin_name="ORIGIN NAME",
            reference_code="XXXXXXXX",
        )
        sql = AchFileHeaderSql()
        sql.insert_record(ach_file_header_record)
        retrieved_record = sql.get_record(ach_records_type_1_id)
        assert (
            SqlUtils.get_row_count_of_1("ach_file_headers") is True
        ), "Expected 1 record"
        assert (
            retrieved_record == ach_file_header_record
        ), f"Expected {ach_file_header_record}, but got {retrieved_record}"
