"""
Simple test to check if the database is up and running when using testcontainers
"""

from pathlib import Path

import pytest
from testcontainers.compose import DockerCompose

from final.v1.AchParser.tests.ach_processor.sql_utils import SqlUtils


@pytest.fixture(scope="module")
def docker_compose():
    absolute_path = Path("../../docker").resolve()
    print(f"absolute_path: {absolute_path}")
    with DockerCompose(absolute_path) as compose:
        yield compose


def test_postgresql(docker_compose):
    with SqlUtils().get_db() as conn:
        result = conn.execute("SELECT COUNT(*) FROM companies")
        record = result.fetchone()[0]
        assert record == 10
