from fastapi.testclient import TestClient
from chapter5.APISample_Final.app.main import app

client = TestClient(app)

def test_read_record():
    response = client.get("/api/v1/files/1/records/2")
    assert response.status_code == 200
    assert response.json() == {"file_id": "1", "record_id": "2"}

