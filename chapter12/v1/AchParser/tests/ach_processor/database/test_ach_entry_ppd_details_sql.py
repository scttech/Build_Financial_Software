import pytest

from chapter12.v1.AchParser.ach_processor.database.ach_entry_ppd_details_sql import (
    AchEntryPpdDetailsSql,
)
from chapter12.v1.AchParser.ach_processor.schemas.database.ach_entry_ppd_details_schema import (
    AchEntryPpdDetailsSchema,
)
from chapter12.v1.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestAchEntryPpdDetailsSql:
    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        print("\nsetup test\n")
        yield
        SqlUtils.truncate_all()

    def test_insert_record(self):
        sample_ach_entry_ppd_details_record = "6272670841345                0000000301               0003xxxxxxxxxxxxxxxx  LC1061000010003001"
        ach_records_type_5_id, ach_records_type_6_id = (
            SqlUtils.setup_entry_ppd_details_test(sample_ach_entry_ppd_details_record)
        )

        ach_entry_ppd_details_record = AchEntryPpdDetailsSchema(
            ach_records_type_6_id=ach_records_type_6_id,
            record_type_code="6",
            transaction_code="27",
            receiving_dfi_identification="26708413",
            check_digit="4",
            dfi_account_number="5",
            amount="0000000301",
            individual_identification_number="",
            individual_name="0003xxxxxxxxxxxxxxxx",
            discretionary_data="LC",
            addenda_record_indicator="1",
            trace_number="061000010003001",
        )
        sql = AchEntryPpdDetailsSql()
        sql.insert_record(ach_entry_ppd_details_record)
        retrieved_record = sql.get_record(ach_records_type_6_id)
        assert (
            SqlUtils.get_row_count_of_1("ach_entry_ppd_details") is True
        ), "Expected 1 record"
        assert (
            retrieved_record == ach_entry_ppd_details_record
        ), f"Expected {ach_entry_ppd_details_record}, but got {retrieved_record}"
