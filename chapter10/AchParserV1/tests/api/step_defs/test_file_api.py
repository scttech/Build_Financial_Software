import os
from random import randint

import pytest
from pytest_bdd import given, scenarios, parsers, when, then
from starlette.testclient import TestClient

from ach_processor.ach_file_processor import AchFileProcessor
from app.main import app
from tests.ach_processor.sql_utils import SqlUtils

client = TestClient(app)

# Load scenarios
scenarios("../features/ach_files_endpoint.feature")
scenarios("../features/ach_files_exception_endpoint.feature")


@pytest.fixture
def ach_file_processor() -> AchFileProcessor:
    return AchFileProcessor()


@pytest.fixture
def api_response():
    return {}


@given("that I have a clean database")
def truncate_database():
    SqlUtils.truncate_all()


@given(parsers.parse('that I have posted the file \"{ach_file}\"'))
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


@when(parsers.parse('I request a list of exceptions for the file \"{filename}\"'))
def get_list_of_exceptions_for_file(api_response, filename):
    response = client.get("/api/v1/files/")
    assert response.status_code == 200, response.text
    file_id = response.json()[0]["id"]
    response = client.get(f"/api/v1/files/{file_id}/exceptions")
    assert response.status_code == 200, response.text
    api_response["response"] = response.json()


@when('I request the unparsed record for the exception code "004"')
def request_unparsed_record(api_response):
    response = client.get("/api/v1/files/")
    assert response.status_code == 200, response.text
    file_id = response.json()[0]["id"]
    response = client.get(f"/api/v1/files/{file_id}/exceptions")
    assert response.status_code == 200, response.text
    exception_id = response.json()[0]["id"]
    response = client.get(f"/api/v1/files/{file_id}/exceptions/{exception_id}")
    assert response.status_code == 200, response.text
    api_response["response"] = response.json()


@when("I request a list of exceptions for all files")
def request_a_list_of_exceptions_for_all_files(api_response):
    response = client.get(f"/api/v1/files/exceptions")
    assert response.status_code == 200, response.text
    api_response["response"] = response.json()


@then(parsers.parse('I should have a response that includes the file \"{filename}\"'))
def response_that_includes_file(filename, api_response):
    assert any(
        response["filename"] == filename for response in api_response["response"]
    ), f"Expected {filename} in" f" {api_response['response']}"


@then(parsers.parse('it should have a total credit amount of "{credit_amount}"'))
def should_have_a_total_credit_amount(credit_amount, api_response):
    response = api_response["response"][0]["credit_total"]
    assert credit_amount == response, f"Expected {credit_amount} in {response}"


@then(parsers.parse('it should have a total debit amount of "{debit_amount}"'))
def should_have_a_total_debit_amount(debit_amount, api_response):
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


@then(parsers.parse('I should receive an error of \"{error_code}\" and a message of \"{error_message}\"'))
def check_error_code_exists_on_response(error_code, error_message, api_response):
    print(api_response["response"])
    assert any(
        error_code == response["exception_code"] for response in api_response["response"]
    ), f"Expected {error_code} in" f" {api_response['response']}"
    assert any(
        error_message == response["description"] for response in api_response["response"]
    ), f"Expected {error_message} in" f" {api_response['response']}"


@then(parsers.parse('I should receive an unparsed record of \"{expected_unparsed_record}\"'))
def receive_an_unparsed_record(api_response, expected_unparsed_record):
    print(api_response["response"])
    actual_unparsed_record = api_response["response"]["unparsed_record"]
    assert expected_unparsed_record == actual_unparsed_record, \
        f"Expected {expected_unparsed_record} in {api_response['response']}"


@then(parsers.parse("the has_exceptions field should be {expected_value}"))
def has_exceptions_validation(api_response, expected_value):
    expected_bool_value = expected_value.lower() == "true"
    actual_exceptions_flag = api_response["response"][0]["has_exceptions"]
    assert expected_bool_value == actual_exceptions_flag, \
        f"Expected {expected_value} in {api_response['response']}"
