from pathlib import Path
from unittest.mock import patch

import pytest
from starlette.testclient import TestClient
from testcontainers.compose import DockerCompose

from chapter12.v2.AchParser.app.main import app


@pytest.fixture(scope="class", autouse=True)
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def docker_compose():
    absolute_path = Path("../../docker").resolve()
    with DockerCompose(absolute_path, build=True, services=["postgres"]) as compose:
        compose.start()
        yield compose
        compose.stop()


class TestCompanyApis:

    @pytest.fixture(autouse=True)
    def mock_client_host(self):
        with patch(
            "fastapi.Request.client",
            new_callable=lambda: type("Client", (), {"host": "127.0.0.1"}),
        ):
            yield

    def test_get_companies(self, client, docker_compose):
        response = client.get("/api/v1/companies")
        assert response.status_code == 200, response.text
        assert len(response.json()) == 10

    def test_get_single_company(self, client, docker_compose):
        overview_response = client.get("/api/v1/companies")
        assert overview_response.status_code == 200, overview_response.text
        company_id = overview_response.json()[0]["company_id"]
        detail_response = client.get(f"/api/v1/companies/{company_id}")
        assert detail_response.status_code == 200, detail_response.text
        assert detail_response.json()["company_id"] == company_id
