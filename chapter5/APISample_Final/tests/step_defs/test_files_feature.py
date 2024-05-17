import pytest
from pytest_bdd import scenarios, when, then, parsers
from fastapi.testclient import TestClient
from chapter5.APISample_Final.app.main import app

client = TestClient(app)

# Load scenarios
scenarios("../features/files.feature")

@pytest.fixture
def api_response():
    # Store response from API
    return {}

@when(parsers.parse('I make a {http_request_type} request to the endpoint {endpoint}'))
def when_http_request_to_endpoint(
    api_response,
    http_request_type,
    endpoint
):
    if http_request_type == "GET":
        response = client.get(endpoint)
    elif http_request_type == "POST":
        response = client.post(endpoint, json={"file": "File_4"})
    else:
        raise NotImplementedError
    api_response["data"] = response


@then(parsers.parse("the status code should be {status_code:d}"))
def then_the_status_code_is(api_response, status_code):
    assert (
        api_response["data"].status_code == status_code
    ), f"Expected {status_code}, but got {when_http_request_to_endpoint.status_code}"