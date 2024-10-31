from pathlib import Path
from random import randint
from typing import Callable, Optional
from unittest.mock import patch

import pytest
from starlette.testclient import TestClient

from chapter11.v4.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v4.AchParser.app.main import app
from chapter11.v4.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestOfacApi:
    client: TestClient = TestClient(app)
    ach_files_id: Optional[str] = None

    # Get the directory of our file
    current_file_dir = Path(__file__).resolve().parent

    @pytest.fixture(autouse=True)
    def mock_client_host(self):
        with patch(
            "fastapi.Request.client",
            new_callable=lambda: type("Client", (), {"host": "127.0.0.1"}),
        ):
            yield

    def get_absolute_path(self, relative_path):
        return self.current_file_dir / relative_path

    def setup_method(self, _method: Callable) -> None:
        ach_file = "ofac_elemental_resources.ach"
        absolute_path = self.get_absolute_path(
            Path("../data/ofac_elemental_resources.ach")
        )
        SqlUtils.truncate_all()
        self.ach_files_id = SqlUtils.create_ach_file_record(
            ach_file, str(randint(1, 99999999))
        )
        AchFileProcessor().parse(self.ach_files_id, absolute_path)

    def test_get_ofac_api_for_ppd_batches(self):
        print(
            f"\nTesting {self.__class__.__name__} class with {self.ach_files_id} file id"
        )
        response = self.client.get("/api/v1/files/ofac")
        assert response.status_code == 200, response.text
        assert len(response.json()) == 3, "Should have 3 matches"

    def teardown_method(self, method: Callable) -> None:
        print(f"\nTeardown for {method.__name__} test method execution")
