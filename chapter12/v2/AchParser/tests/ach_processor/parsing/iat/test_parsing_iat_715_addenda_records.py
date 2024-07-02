from decimal import Decimal
from typing import Literal

from chapter12.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
import pytest

from chapter12.v2.AchParser.ach_processor.database.ach.iat.ach_iat_710_addenda_sql import (
    AchIat710AddendaSql,
)
from chapter12.v2.AchParser.ach_processor.database.ach.iat.ach_iat_711_addenda_sql import (
    AchIat711AddendaSql,
)
from chapter12.v2.AchParser.ach_processor.database.ach.iat.ach_iat_712_addenda_sql import (
    AchIat712AddendaSql,
)
from chapter12.v2.AchParser.ach_processor.database.ach.iat.ach_iat_713_addenda_sql import (
    AchIat713AddendaSql,
)
from chapter12.v2.AchParser.ach_processor.database.ach.iat.ach_iat_714_addenda_sql import (
    AchIat714AddendaSql,
)
from chapter12.v2.AchParser.ach_processor.database.ach.iat.ach_iat_715_addenda_sql import (
    AchIat715AddendaSql,
)
from chapter12.v2.AchParser.ach_processor.database.ach_addenda_ppd_sql import (
    AchAddendaPpdSql,
)
from chapter12.v2.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestParsingIat715AddendaRecords:

    TABLE_NAME: str = "ach_iat_addenda_715_records"

    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        SqlUtils.truncate_all()
        yield

    def test_parse_iat_addenda_715_records(self):
        # Define a sample ACH addenda record
        sample_addenda_record = "715               9999 NORTH BROADWAY                                                  0000001"

        # Define the expected result of parsing the sample ACH entry detail record
        expected_result = {
            "record_type_code": Literal["7"],
            "addenda_type_code": 15,
            "receiver_identification_number": "",
            "receiver_street_address": "9999 NORTH BROADWAY",
            "entry_detail_sequence_number": 1,
        }

        _, ach_records_type_7_id = SqlUtils.setup_iat_addenda_test(
            sample_addenda_record
        )

        parser = AchFileProcessor()
        parser._parse_iat_addenda_715(ach_records_type_7_id, sample_addenda_record)

        sql = AchIat715AddendaSql()
        retrieved_record = sql.get_record(ach_records_type_7_id).model_dump(
            exclude={"ach_records_type_7_id"}
        )

        assert SqlUtils.get_row_count_of_1(
            self.TABLE_NAME
        ), f"Expected 1 row in {self.TABLE_NAME}"
        assert (
            retrieved_record == expected_result
        ), f"Expected {expected_result}, but got {retrieved_record}"
