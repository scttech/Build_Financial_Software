import pytest

from chapter6.v2.AchProcessor.ach_processor.database.ach_batch_control_sql import (
    AchBatchControlSql,
)
from chapter6.v2.AchProcessor.ach_processor.schemas.ach_batch_control_schema import (
    AchBatchControlSchema,
)
from chapter6.v2.AchProcessor.tests.ach_processor.sql_utils import SqlUtils


class TestAchBatchHeaderSql:
    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        SqlUtils.truncate_all()
        yield

    def test_insert_record(self):

        sample_batch_control_record = "82000000080016501650000000000301000000000302CompID                             061000010000003"
        ach_records_type_5_id, ach_records_type_8_id = (
            SqlUtils.setup_batch_control_test(sample_batch_control_record)
        )

        ach_batch_control_record = AchBatchControlSchema(
            ach_records_type_8_id=ach_records_type_8_id,
            record_type_code="8",
            service_class_code="200",
            entry_addenda_count="000008",
            entry_hash="0016501650",
            total_debit_entry_dollar_amount="000000000301",
            total_credit_entry_dollar_amount="000000000302",
            company_identification="CompID",
            message_authentication_code="",
            reserved="",
            originating_dfi_identification="06100001",
            batch_number="0000003",
        )

        sql = AchBatchControlSql()
        sql.insert_record(ach_batch_control_record)
        retrieved_record = sql.get_record(ach_records_type_8_id)
        assert (
            SqlUtils.get_row_count_of_1("ach_batch_control_records") is True
        ), "Expected 1 record"
        assert (
            retrieved_record == ach_batch_control_record
        ), f"Expected {ach_batch_control_record}, but got {retrieved_record}"
