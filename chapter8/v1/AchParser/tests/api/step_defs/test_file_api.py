import os
from random import randint

import pytest
from pytest_bdd import given, scenarios, parsers, when, then
from starlette.testclient import TestClient

from chapter8.AchParserMvpNoSignOnScreen.ach_processor.ach_file_processor import AchFileProcessor
from chapter8.AchParserMvpNoSignOnScreen.app.main import app
from chapter8.AchParserMvpNoSignOnScreen.tests.ach_processor.sql_utils import SqlUtils

client = TestClient(app)

# Load scenarios
scenarios("../features/ach_files_endpoint.feature")


@pytest.fixture
def ach_file_processor() -> AchFileProcessor:
    return AchFileProcessor()


@pytest.fixture
def api_response():
    return {}


@given("that I have a clean database")
def truncate_database():
    SqlUtils.truncate_all()


@given(parsers.re(r'that I have posted the file "(?P<ach_file>.*)"'))
def parse_the_given_file(ach_file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "../data", ach_file)
    parser = AchFileProcessor()
    ach_files_id = SqlUtils.create_ach_file_record(ach_file, str(randint(1, 99999999)))
    parser.parse(ach_files_id, file_path)


@when("I request a list of files")
def request_files(api_response):
    response = client.get("/api/v1/files")
    assert response.status_code == 200, response.text
    print(response.json())
    api_response["response"] = response.json()


@then(parsers.re('I should have a file that includes the file "(?P<filename>.*)"'))
def step_impl(filename, api_response):
    assert any(
        response["filename"] == filename for response in api_response["response"]
    ), (f"Expected {filename} in" f" {api_response['response']}")


@then(parsers.parse('it should have a total credit amount of "{credit_amount}"'))
def step_impl(credit_amount, api_response):
    response = api_response["response"][0]["credit_total"]
    assert credit_amount == response, f"Expected {credit_amount} in {response}"


@then(parsers.parse('it should have a total debit amount of "{debit_amount}"'))
def step_impl(debit_amount, api_response):
    response = api_response["response"][0]["debit_total"]
    assert debit_amount == response, f"Expected {debit_amount} in {response}"


@then("there should be no exceptions")
def no_exceptions():
    assert 0 == len(SqlUtils.get_exceptions()), "Expected no exceptions"


@then(parsers.parse('I should have a single file named "{filename}"'))
def verify_single_file(filename, api_response):
    assert (
        len(api_response["response"]) == 1
    ), f"Expected 1 file, but got {len(api_response['response'])}"
    response = api_response["response"][0]["filename"]
    assert filename == response, f"Expected {filename} in {response}"
