import os
from random import randint

import pytest
from pytest_bdd import given, scenarios, parsers, when, then
from starlette.testclient import TestClient

from chapter9.v1.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter9.v1.AchParser.app.main import app
from chapter9.v1.AchParser.tests.ach_processor.sql_utils import SqlUtils

client = TestClient(app)

# Load scenarios
scenarios("../features/ach_entries_endpoint.feature")


@pytest.fixture
def ach_file_processor() -> AchFileProcessor:
    return AchFileProcessor()


@pytest.fixture
def api_response():
    return {}


@given("that I have a clean database")
def truncate_database():
    SqlUtils.truncate_all()


@given(parsers.parse('that I have posted the file "{ach_file}"'))
def parse_the_given_file(ach_file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "../data", ach_file)
    parser = AchFileProcessor()
    ach_files_id = SqlUtils.create_ach_file_record(ach_file, str(randint(1, 99999999)))
    parser.parse(ach_files_id, file_path)


@when("I request entries for a file and batch")
def request_unparsed_record(api_response):
    response = client.get("/api/v1/files/")
    assert response.status_code == 200, response.text
    file_id = response.json()[0]["id"]
    response = client.get(f"/api/v1/files/{file_id}/batches")
    assert response.status_code == 200, response.text
    batch_id = response.json()[0]["id"]
    response = client.get(f"/api/v1/files/{file_id}/batches/{batch_id}/entries")
    assert response.status_code == 200, response.text
    api_response["response"] = response.json()


@then(
    parsers.parse(
        'I should have a response that includes all applications of "{application}"'
    )
)
def response_that_includes_file(application, api_response):
    assert all(
        response["application"] == application for response in api_response["response"]
    ), (f"Expected {application} in" f" {api_response['response']}")
