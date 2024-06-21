from unittest.mock import patch
import pytest
from starlette.testclient import TestClient

from chapter11.v2.AchParser.app.companies.companies_sql import CompaniesSql
from chapter11.v2.AchParser.app.main import app
from testcontainers.compose import DockerCompose
from pathlib import Path


@pytest.fixture(scope="module")
def docker_compose():
    absolute_path = Path("../../../../docker/db").resolve()
    with DockerCompose(absolute_path, build=True, services=["postgres"]) as compose:
        compose.start()
        yield compose
        compose.stop()


class TestCompaniesSql:

    @pytest.fixture()
    def sql(self):
        return CompaniesSql()

    def test_get_companies(self, docker_compose, sql):
        result = sql.get_all_companies()
        assert len(result) == 10

    def test_get_single_company(self, docker_compose, sql):
        result_all = sql.get_all_companies()
        assert len(result_all) == 10
        result_single = sql.get_company_by_id(result_all[0].company_id)
        assert result_single.company_id in [
            company.company_id for company in result_all
        ]
