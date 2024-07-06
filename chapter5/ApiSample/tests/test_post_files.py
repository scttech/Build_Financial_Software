from fastapi.testclient import TestClient

from chapter5.ApiSample.app.main import app

client = TestClient(app)


def test_post_files():
    response = client.post("/files", json={"file": "File_3"})
    assert response.status_code == 201
    assert response.json() == {"file": "File_3"}
