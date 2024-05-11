from fastapi.testclient import TestClient
from tests.SqlUtils import SqlUtils
import pytest
from app.main import app

client = TestClient(app)

@pytest.fixture
def setup_teardown_method():
    yield
    SqlUtils.truncate_all()

def test_read_files():
    response = client.get("/api/v1/files")
    assert response.status_code == 200
    assert response.json() == [{"file": "File_1"}, {"file": "File_2"}]

def test_upload_file(setup_teardown_method):
    with open("data/sample.ach", "rb") as test_file:
        response = client.post("/api/v1/files", files={"file": test_file})
    assert response.status_code == 201
    assert SqlUtils.get_row_count_of_1('ach_files')
