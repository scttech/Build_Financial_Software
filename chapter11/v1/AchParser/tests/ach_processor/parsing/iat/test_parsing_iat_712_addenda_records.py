from typing import Literal

import pytest

from chapter11.v1.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v1.AchParser.ach_processor.database.ach.iat.ach_iat_712_addenda_sql import (
    AchIat712AddendaSql,
)
from chapter11.v1.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestParsingIat712AddendaRecords:

    TABLE_NAME: str = "ach_iat_addenda_712_records"

    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        SqlUtils.truncate_all()
        yield

    def test_parse_iat_addenda_712_records(self):
        # Define a sample ACH addenda record
        sample_addenda_record = "712BILBAO*BIZKAIA\                    ES*48001\                                        0000001"

        # Define the expected result of parsing the sample ACH entry detail record
        expected_result = {
            "record_type_code": Literal["7"],
            "addenda_type_code": 12,
            "originator_city": "BILBAO",
            "originator_state": "BIZKAIA",
            "originator_country": "ES",
            "originator_postal_code": "48001",
            "entry_detail_sequence_number": 1,
        }

        _, ach_records_type_7_id = SqlUtils.setup_iat_addenda_test(
            sample_addenda_record
        )

        parser = AchFileProcessor()
        parser._parse_iat_addenda_712(ach_records_type_7_id, sample_addenda_record)

        sql = AchIat712AddendaSql()
        retrieved_record = sql.get_record(ach_records_type_7_id).model_dump(
            exclude={"ach_records_type_7_id"}
        )

        assert SqlUtils.get_row_count_of_1(
            self.TABLE_NAME
        ), f"Expected 1 row in {self.TABLE_NAME}"
        assert (
            retrieved_record == expected_result
        ), f"Expected {expected_result}, but got {retrieved_record}"
