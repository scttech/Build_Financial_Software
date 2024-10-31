import os
from typing import Generator

import pytest

from chapter11.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v2.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestLoadingPpdFiles:

    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        SqlUtils.truncate_all()
        yield

    @pytest.fixture(autouse=True)
    def parser(self) -> Generator[AchFileProcessor, None, None]:
        yield AchFileProcessor()

    def test_good_unparsed_records_only(self, parser):
        filename = "ppd-mixed.ach"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "data", filename)

        expected_exceptions_result: int = 0
        expected_total_records_result: int = 14

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
        assert record_count_type6 == 10, f"Expected 10, but got {record_count_type6}"
        assert record_count_type7 == 0, f"Expected 0, but got {record_count_type7}"
        assert record_count_type8 == 1, f"Expected 1, but got {record_count_type8}"
        assert record_count_type9 == 1, f"Expected 1, but got {record_count_type9}"
        assert (
            total_record_count == expected_total_records_result
        ), f"Expected {expected_total_records_result}, but got {total_record_count}"

        assert (
            len(exceptions) == expected_exceptions_result
        ), f"Expected {expected_exceptions_result}, but got {len(exceptions)}"

    def test_good_parsed_records(self, parser):
        filename = "ppd-mixed.ach"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "data", filename)

        expected_exceptions_result: int = 0
        expected_total_records_result: int = 14

        ach_file_id = SqlUtils.create_ach_file_record(filename, "123456789")

        parser.parse(ach_file_id, file_path)
        exceptions = SqlUtils.get_exceptions()

        with SqlUtils.get_db() as conn:
            record_count_type1 = conn.execute(
                "SELECT COUNT(*) FROM ach_file_headers"
            ).fetchone()[0]
            record_count_type5 = conn.execute(
                "SELECT COUNT(*) FROM ach_batch_headers"
            ).fetchone()[0]
            record_count_type6 = conn.execute(
                "SELECT COUNT(*) FROM ach_entry_ppd_details"
            ).fetchone()[0]
            record_count_type7 = conn.execute(
                "SELECT COUNT(*) FROM ach_addenda_ppd_records"
            ).fetchone()[0]
            record_count_type8 = conn.execute(
                "SELECT COUNT(*) FROM ach_batch_control_records"
            ).fetchone()[0]
            record_count_type9 = conn.execute(
                "SELECT COUNT(*) FROM ach_file_control_records"
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
        assert record_count_type6 == 10, f"Expected 10, but got {record_count_type6}"
        assert record_count_type7 == 0, f"Expected 0, but got {record_count_type7}"
        assert record_count_type8 == 1, f"Expected 1, but got {record_count_type8}"
        assert record_count_type9 == 1, f"Expected 1, but got {record_count_type9}"
        assert (
            total_record_count == expected_total_records_result
        ), f"Expected {expected_total_records_result}, but got {total_record_count}"

        assert (
            len(exceptions) == expected_exceptions_result
        ), f"Expected {expected_exceptions_result}, but got {len(exceptions)}"
