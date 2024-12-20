from pathlib import Path

import pytest
from testcontainers.compose import DockerCompose

from chapter11.v2.AchParser.common.database.files.expected_files_sql import (
    ExpectedFilesSql,
)
from chapter11.v2.AchParser.common.database.search.company_search_sql import (
    CompanySearchSql,
)


@pytest.fixture(scope="module")
def docker_compose():
    absolute_path = Path("../../docker").resolve()
    print(f"absolute_path: {absolute_path}")
    with DockerCompose(absolute_path, build=True, services=["postgres"]) as compose:
        compose.start()
        yield compose
        compose.stop()


class TestExpectedFilesSql:

    @pytest.fixture()
    def sql(self):
        return ExpectedFilesSql()

    def test_get_expected_files_for_company(self, docker_compose, sql):
        company_id = CompanySearchSql().get_companies("459876543").company_id
        assert company_id is not None
        results = sql.get_expected_files_for_company(company_id)
        assert len(results) == 2
        assert any(
            record.file_name == "elemental_resources.ach" for record in results
        ), "file_name: elemental_resources.ach not found in the array"
        assert any(
            record.file_name == "elemental_resources_daily_billpay.ach"
            for record in results
        ), "file_name: elemental_resources_daily_billpay.ach not found in the array"
