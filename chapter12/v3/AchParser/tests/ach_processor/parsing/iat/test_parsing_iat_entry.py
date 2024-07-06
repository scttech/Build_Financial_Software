from decimal import Decimal

import pytest

from chapter12.v3.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter12.v3.AchParser.ach_processor.database.ach.iat.ach_iat_entry_details_sql import (
    AchIatEntryDetailsSql,
)
from chapter12.v3.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestParsingIatEntry:

    TABLE_NAME: str = "ach_iat_entry_details"

    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        SqlUtils.truncate_all()
        yield

    def test_parse_iat_entry(self):
        sample_entry_record = "6222670841310007             0000000100123                                    1000000100000001"

        # Define the expected result of parsing the batch control record
        expected_result = {
            "record_type_code": "6",
            "transaction_code": 22,
            "receiving_dfi_identification": "26708413",
            "number_of_addenda": 7,
            "amount": Decimal("1.00"),
            "foreign_receivers_account_number": "123",
            "gateway_ofac_screening": False,
            "secondary_ofac_screening": False,
            "addenda_record_indicator": "1",
            "trace_number": 100000001,
        }

        ach_file_id, ach_records_type_5_id, ach_iat_entries_record_id = (
            SqlUtils.setup_entry_iat_details_test(sample_entry_record)
        )

        parser = AchFileProcessor()
        parser._parse_iat_entry_detail(
            ach_file_id=ach_file_id,
            current_batch_header_id=ach_records_type_5_id,
            ach_records_type_6_id=ach_iat_entries_record_id,
            sequence_number=1,
            line=sample_entry_record,
        )

        sql = AchIatEntryDetailsSql()
        retrieved_record = sql.get_record(ach_iat_entries_record_id).model_dump(
            exclude={"ach_records_type_6_id"}
        )

        assert SqlUtils.get_row_count_of_1(
            self.TABLE_NAME
        ), f"Expected 1 row in {self.TABLE_NAME}"
        assert (
            retrieved_record == expected_result
        ), f"Expected {expected_result}, but got {retrieved_record}"
