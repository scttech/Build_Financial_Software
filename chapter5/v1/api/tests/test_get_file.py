from fastapi.testclient import TestClient

from chapter5.ApiSample.app.main import app

client = TestClient(app)


def test_read_file():
    response = client.get("/files/1")
    assert response.status_code == 200
    assert response.json() == {"file_id": "1"}
