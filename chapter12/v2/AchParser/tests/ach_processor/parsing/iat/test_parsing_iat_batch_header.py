import pytest
from chapter12.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter12.v2.AchParser.ach_processor.database.ach.iat.ach_iat_batch_header_sql import (
    AchIatBatchHeaderSql,
)
from chapter12.v2.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestParsingIatBatchHeader:

    TABLE_NAME: str = "ach_iat_batch_headers"

    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        print("\nsetup test\n")
        SqlUtils.truncate_all()
        yield

    def test_parse_iat_batch_header(self):
        # Define a sample batch control record
        sample_batch_header_record = "5220                FF3               US1234567890IATGIFT      USDUSD2406291811061000010000001"

        # Define the expected result of parsing the batch control record
        expected_result = {
            "record_type_code": "5",
            "service_class_code": "220",
            "iat_indicator": "",
            "foreign_exchange_indicator": "FF",
            "foreign_exchange_ref_indicator": "3",
            "foreign_exchange_reference": "",
            "iso_destination_country_code": "US",
            "originator_id": "1234567890",
            "standard_entry_class_code": "IAT",
            "company_entry_description": "GIFT",
            "iso_originating_currency_code": "USD",
            "iso_destination_currency_code": "USD",
            "effective_entry_date": "240629",
            "settlement_date": "181",
            "originator_status_code": "1",
            "originating_dfi_identification": "06100001",
            "batch_number": 1,
        }

        _, ach_batch_header_record_id = SqlUtils.setup_batch_header_test(
            sample_batch_header_record
        )

        parser = AchFileProcessor()
        parser._parse_iat_batch_header(
            ach_batch_header_record_id, sample_batch_header_record
        )

        sql = AchIatBatchHeaderSql()
        retrieved_record = sql.get_record(ach_batch_header_record_id).model_dump(
            exclude={"ach_records_type_5_id"}
        )

        assert SqlUtils.get_row_count_of_1(
            self.TABLE_NAME
        ), f"Expected 1 row in {self.TABLE_NAME}"
        assert (
            retrieved_record == expected_result
        ), f"Expected {expected_result}, but got {retrieved_record}"
