import pytest
from testcontainers.compose import DockerCompose
from pathlib import Path

from chapter12.v3.AchParser.common.database.company.company_limits_sql import (
    CompanyLimitsSql,
)
from chapter12.v3.AchParser.common.database.search.company_search_sql import (
    CompanySearchSql,
)


@pytest.fixture(scope="module")
def docker_compose():
    absolute_path = Path("../../docker").resolve()
    print(f"absolute_path: {absolute_path}")
    with DockerCompose(absolute_path, build=True, services=["postgres"]) as compose:
        compose.start()
        yield compose
        compose.stop(down=True)


class TestCompanyLimitsSql:

    @pytest.fixture()
    def sql(self):
        return CompanyLimitsSql()

    def test_get_company_limits(self, docker_compose, sql):
        company_id = CompanySearchSql().get_companies("459876543").company_id
        assert company_id is not None
        company_limit = sql.get_company_limits(company_id)
        assert company_limit is not None
        assert company_limit.daily_credit_limit == 750
        assert company_limit.daily_debit_limit == 400
        assert company_limit.current_credit_total == 0
        assert company_limit.current_debit_total == 0
        assert company_limit.daily_credit_exceeded is False
        assert company_limit.daily_debit_exceeded is False
