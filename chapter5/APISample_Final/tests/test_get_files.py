from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_files():
    response = client.get("/api/v1/files")
    assert response.status_code == 200
    assert response.json() == [{"file": "File_1"}, {"file": "File_2"}]
