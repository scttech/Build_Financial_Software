from chapter5.ApiSample.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_files():
    response = client.get("/files")
    assert response.status_code == 200
    assert response.json() == [{"file": "File_1"}, {"file": "File_2"}]
