from fastapi.testclient import TestClient

from chapter4.ApiSample.app.main import app

client = TestClient(app)


def test_read_record():
    response = client.get("/files/1/records/2")
    assert response.status_code == 200
    assert response.json() == {"file_id": "1", "record_id": "2"}
