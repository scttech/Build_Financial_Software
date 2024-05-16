import pytest
from pprint import pprint

from chapter10.AchParserV1.ach_processor.database.ach_addenda_ppd_sql import AchAddendaPpdSql
from chapter10.AchParserV1.ach_processor.schemas.database.ach_addenda_ppd_schema import AchAddendaPpdSchema
from chapter10.AchParserV1.tests.ach_processor.sql_utils import SqlUtils


class TestAchAddendaPpdSql:
    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        SqlUtils.truncate_all()
        yield

    def test_insert_record(self):
        sample_addenda_ppd_record = "705Test 2                                                                          00020003001"
        _, ach_records_type_7_id = SqlUtils.setup_addenda_ppd_test(
            sample_addenda_ppd_record
        )

        ach_addenda_ppd_record = AchAddendaPpdSchema(
            ach_records_type_7_id=ach_records_type_7_id,
            record_type_code="7",
            addenda_type_code="05",
            payment_related_information="Test 2",
            addenda_sequence_number="0002",
            entry_detail_sequence_number="0003001",
        )
        sql = AchAddendaPpdSql()
        sql.insert_record(ach_addenda_ppd_record)
        retrieved_record = sql.get_record(ach_records_type_7_id)
        assert (
            SqlUtils.get_row_count_of_1("ach_addenda_ppd_records") is True
        ), "Expected 1 record"
        assert (
            retrieved_record.dict() == ach_addenda_ppd_record.dict()
        ), f"Expected {ach_addenda_ppd_record}, but got {retrieved_record}"
