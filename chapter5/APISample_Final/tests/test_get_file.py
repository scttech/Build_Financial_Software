from fastapi.testclient import TestClient

from chapter5.APISample_Final.app.main import app

client = TestClient(app)


def test_read_file():
    response = client.get("/api/v1/files/1")
    assert response.status_code == 200
    assert response.json() == {"file_id": "1"}


def test_read_file_lower_case():
    response = client.get("/api/v1/files/lower_case_file_id")
    assert response.status_code == 200
    assert response.json() == {"file_id": "lower_case_file_id"}


def test_read_file_validation_error():
    response = client.get("/api/v1/files/this_IS_invalid")
    assert response.status_code == 400
    assert (
        response.json()["detail"][0]["msg"]
        == "String should match pattern '^[a-z0-9_]+$'"
    )
