import pytest
from pytest_bdd import scenarios, when, then, parsers

from chapter11.v1.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v1.AchParser.ach_processor.database.ach_batch_header_sql import (
    AchBatchHeaderSql,
)
from chapter11.v1.AchParser.tests.ach_processor.sql_utils import SqlUtils

# Load scenarios
scenarios("../features/batch_header.feature")


@pytest.fixture
def ach_file_processor():
    return AchFileProcessor()


@pytest.fixture
def record():
    return {}


@pytest.fixture
def setup_teardown_method():
    yield
    SqlUtils.truncate_all()


@when(parsers.re(r'we parse the batch header "(?P<batch_header_record>.*)"'))
def when_the_record_is_parsed(
    ach_file_processor,
    batch_header_record,
    record,
):
    ach_file_header_record_id, ach_batch_header_record_id = (
        SqlUtils.setup_batch_header_test(batch_header_record)
    )
    ach_file_processor._parse_batch_header(
        ach_batch_header_record_id, batch_header_record
    )
    sql = AchBatchHeaderSql()
    retrieved_record = sql.get_record(ach_batch_header_record_id).model_dump()
    record.update(retrieved_record)


@then(parsers.parse("the record type should be {type_5}"))
def then_record_type_code_should_be(record, type_5, setup_teardown_method):
    assert (
        record["record_type_code"] == type_5
    ), f"Expected {type_5}, but got {record['record_type_code']}"
