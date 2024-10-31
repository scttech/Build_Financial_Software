import os
from typing import Generator

import pytest

from chapter11.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v2.AchParser.tests.ach_processor.sql_utils import SqlUtils


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

        expected_exceptions_result: int = 0
        expected_total_records_result: int = 12

        ach_file_id = SqlUtils.create_ach_file_record(filename, "123456789")

        parser.parse(ach_file_id, file_path)
        exceptions = SqlUtils.get_exceptions()

        with SqlUtils.get_db() as conn:
            record_count_type1 = conn.execute(
                "SELECT COUNT(*) FROM ach_file_headers"
            ).fetchone()[0]
            record_count_type5 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_batch_headers"
            ).fetchone()[0]
            record_count_type6 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_entry_details"
            ).fetchone()[0]
            record_count_type710 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_addenda_710_records"
            ).fetchone()[0]
            record_count_type711 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_addenda_711_records"
            ).fetchone()[0]
            record_count_type712 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_addenda_712_records"
            ).fetchone()[0]
            record_count_type713 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_addenda_713_records"
            ).fetchone()[0]
            record_count_type714 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_addenda_714_records"
            ).fetchone()[0]
            record_count_type715 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_addenda_715_records"
            ).fetchone()[0]
            record_count_type716 = conn.execute(
                "SELECT COUNT(*) FROM ach_iat_addenda_716_records"
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
            + record_count_type710
            + record_count_type711
            + record_count_type712
            + record_count_type713
            + record_count_type714
            + record_count_type715
            + record_count_type716
            + record_count_type8
            + record_count_type9
        )

        assert record_count_type1 == 1, f"Expected 1, but got {record_count_type1}"
        assert record_count_type5 == 1, f"Expected 1, but got {record_count_type5}"
        assert record_count_type6 == 1, f"Expected 10, but got {record_count_type6}"
        assert record_count_type710 == 1, f"Expected 0, but got {record_count_type710}"
        assert record_count_type711 == 1, f"Expected 0, but got {record_count_type711}"
        assert record_count_type712 == 1, f"Expected 0, but got {record_count_type712}"
        assert record_count_type713 == 1, f"Expected 0, but got {record_count_type713}"
        assert record_count_type714 == 1, f"Expected 0, but got {record_count_type714}"
        assert record_count_type715 == 1, f"Expected 0, but got {record_count_type715}"
        assert record_count_type716 == 1, f"Expected 0, but got {record_count_type716}"
        assert record_count_type8 == 1, f"Expected 1, but got {record_count_type8}"
        assert record_count_type9 == 1, f"Expected 1, but got {record_count_type9}"
        assert (
            total_record_count == expected_total_records_result
        ), f"Expected {expected_total_records_result}, but got {total_record_count}"

        assert (
            len(exceptions) == expected_exceptions_result
        ), f"Expected {expected_exceptions_result}, but got {len(exceptions)}"
