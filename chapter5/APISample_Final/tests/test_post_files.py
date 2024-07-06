from fastapi.testclient import TestClient

from chapter5.APISample_Final.app.main import app

client = TestClient(app)


def test_post_files():
    response = client.post("/api/v1/files", json={"file": "File_3"})
    assert response.status_code == 201
    assert response.json() == {"file": "File_3"}
