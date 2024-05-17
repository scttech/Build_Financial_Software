import pytest
from pytest_bdd import scenarios, when, then, parsers
from chapter6.AchProcessor.tests.SqlUtils import SqlUtils
from chapter6.AchProcessor.ach_processor.AchFileProcessor import AchFileProcessor

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
    with SqlUtils.get_db() as conn:
        parsed_record = ach_file_processor._parse_batch_header(conn, batch_header_record)
    record.update(parsed_record)


@then(parsers.parse("the record type should be {type_5}"))
def then_record_type_code_should_be(record, type_5):
    assert (
        record["record_type_code"] == type_5
    ), f"Expected {type_5}, but got {record['record_type_code']}"
