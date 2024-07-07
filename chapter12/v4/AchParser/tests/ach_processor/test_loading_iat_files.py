import os
from typing import Generator

import pytest
from psycopg.rows import dict_row

from chapter12.v4.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter12.v4.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestLoadingIatFiles:

    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        SqlUtils.truncate_all()
        yield

    @pytest.fixture(autouse=True)
    def parser(self) -> Generator[AchFileProcessor, None, None]:
        yield AchFileProcessor()

    def test_unparsed_records_only(self, parser):
        filename = "iat.ach"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "data", "iat", filename)

        expected_exceptions_result: int = 0
        expected_total_records_result: int = 12

        ach_file_id = SqlUtils.create_ach_file_record(filename, "123456789")

        parser.parse(ach_file_id, file_path)
        exceptions = SqlUtils.get_exceptions()

        with SqlUtils.get_db() as conn:
            record_count_type1 = conn.execute(
                "SELECT COUNT(*) FROM ach_records_type_1"
            ).fetchone()[0]
            record_count_type5 = conn.execute(
                "SELECT COUNT(*) FROM ach_records_type_5"
            ).fetchone()[0]
            record_count_type6 = conn.execute(
                "SELECT COUNT(*) FROM ach_records_type_6"
            ).fetchone()[0]
            record_count_type7 = conn.execute(
                "SELECT COUNT(*) FROM ach_records_type_7"
            ).fetchone()[0]
            record_count_type8 = conn.execute(
                "SELECT COUNT(*) FROM ach_records_type_8"
            ).fetchone()[0]
            record_count_type9 = conn.execute(
                "SELECT COUNT(*) FROM ach_records_type_9"
            ).fetchone()[0]

        total_record_count = (
            record_count_type1
            + record_count_type5
            + record_count_type6
            + record_count_type7
            + record_count_type8
            + record_count_type9
        )

        assert record_count_type1 == 1, f"Expected 1, but got {record_count_type1}"
        assert record_count_type5 == 1, f"Expected 1, but got {record_count_type5}"
        assert record_count_type6 == 1, f"Expected 10, but got {record_count_type6}"
        assert record_count_type7 == 7, f"Expected 0, but got {record_count_type7}"
        assert record_count_type8 == 1, f"Expected 1, but got {record_count_type8}"
        assert record_count_type9 == 1, f"Expected 1, but got {record_count_type9}"
        assert (
            total_record_count == expected_total_records_result
        ), f"Expected {expected_total_records_result}, but got {total_record_count}"

        assert (
            len(exceptions) == expected_exceptions_result
        ), f"Expected {expected_exceptions_result}, but got {len(exceptions)}"

    def test_parsed_records_only(self, parser):
        filename = "iat.ach"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "data", "iat", filename)

        expected_results = {
            "exception_count": 0,
            "total_record_count": 12,
            "record_count_type1": 1,
            "record_count_type5": 1,
            "record_count_type6": 1,
            "record_count_type710": 1,
            "record_count_type711": 1,
            "record_count_type712": 1,
            "record_count_type713": 1,
            "record_count_type714": 1,
            "record_count_type715": 1,
            "record_count_type716": 1,
            "record_count_type8": 1,
            "record_count_type9": 1,
        }

        ach_file_id = SqlUtils.create_ach_file_record(filename, "123456789")

        parser.parse(ach_file_id, file_path)
        exceptions = SqlUtils.get_exceptions()

        with SqlUtils.get_db(row_factory=dict_row) as conn:
            record_counts = conn.execute(
                """
                SELECT
                        record_count_type1,
                        record_count_type5,
                        record_count_type6,
                        record_count_type710,
                        record_count_type711,
                        record_count_type712,
                        record_count_type713,
                        record_count_type714,
                        record_count_type715,
                        record_count_type716,
                        record_count_type8,
                        record_count_type9,
                        record_count_type1 + record_count_type5 + record_count_type6 + record_count_type710 +
                        record_count_type711 + record_count_type712 + record_count_type713 + record_count_type714 +
                        record_count_type715 + record_count_type716 + record_count_type8 + record_count_type9 AS total_record_count
                FROM (
                    SELECT 
                        (SELECT COUNT(*) FROM ach_file_headers) AS record_count_type1,
                        (SELECT COUNT(*) FROM ach_iat_batch_headers) AS record_count_type5,
                        (SELECT COUNT(*) FROM ach_iat_entry_details) AS record_count_type6,
                        (SELECT COUNT(*) FROM ach_iat_addenda_10_details) AS record_count_type710,
                        (SELECT COUNT(*) FROM ach_iat_addenda_11_details) AS record_count_type711,
                        (SELECT COUNT(*) FROM ach_iat_addenda_12_details) AS record_count_type712,
                        (SELECT COUNT(*) FROM ach_iat_addenda_13_details) AS record_count_type713,
                        (SELECT COUNT(*) FROM ach_iat_addenda_14_details) AS record_count_type714,
                        (SELECT COUNT(*) FROM ach_iat_addenda_15_details) AS record_count_type715,
                        (SELECT COUNT(*) FROM ach_iat_addenda_16_details) AS record_count_type716,
                        (SELECT COUNT(*) FROM ach_batch_control_details) AS record_count_type8,
                        (SELECT COUNT(*) FROM ach_file_control_details) AS record_count_type9
                ) AS record_counts
                """
            ).fetchone()
            record_counts["exception_count"] = len(exceptions)

        assert record_counts == expected_results
