import pytest

from chapter12.v3.AchParser.ach_processor.database.ach_batch_header_sql import (
    AchBatchHeaderSql,
)
from chapter12.v3.AchParser.ach_processor.schemas.database.ach_batch_header_schema import (
    AchBatchHeaderSchema,
)
from chapter12.v3.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestAchBatchHeaderSql:
    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        print("\nsetup test\n")
        SqlUtils.truncate_all()
        yield
        SqlUtils.truncate_all()

    def test_insert_record(self):

        sample_batch_header = "5200Company name    DiscretionaryData   1234567890ARCComp desc 0216232302160471061000010000001"
        ach_records_type_1_id, ach_records_type_5_id = SqlUtils.setup_batch_header_test(
            sample_batch_header
        )

        ach_batch_header_record = AchBatchHeaderSchema(
            ach_records_type_5_id=ach_records_type_5_id,
            record_type_code="5",
            service_class_code="200",
            company_name="Company name",
            company_discretionary_data="DiscretionaryData",
            company_identification="1234567890",
            standard_entry_class_code="ARC",
            company_entry_description="Comp desc",
            company_descriptive_date="021623",
            effective_entry_date="230216",
            settlement_date="047",
            originator_status_code="1",
            originating_dfi_identification="0610000",
            batch_number="0000001",
        )
        sql = AchBatchHeaderSql()
        sql.insert_record(ach_batch_header_record)
        retrieved_record = sql.get_record(ach_records_type_5_id)
        assert (
            SqlUtils.get_row_count_of_1("ach_batch_headers") is True
        ), "Expected 1 record"
        assert (
            retrieved_record.dict() == ach_batch_header_record.dict()
        ), f"Expected {ach_batch_header_record}, but got {retrieved_record}"
