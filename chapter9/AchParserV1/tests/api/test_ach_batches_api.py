from pathlib import Path
from random import randint
from typing import Callable, Optional

from chapter9.AchParserV1.ach_processor.ach_file_processor import AchFileProcessor
from chapter9.AchParserV1.app.main import app
from starlette.testclient import TestClient
from chapter9.AchParserV1.tests.ach_processor.sql_utils import SqlUtils


class TestAchBatchesApi:
    client: TestClient = TestClient(app)
    ach_files_id: Optional[str] = None

    def setup_method(self, _method: Callable) -> None:
        ach_file = "data/sample.ach"
        absolute_path = Path("api/data/sample.ach").resolve()
        SqlUtils.truncate_all()
        self.ach_files_id = SqlUtils.create_ach_file_record(
            ach_file, str(randint(1, 99999999))
        )
        AchFileProcessor().parse(self.ach_files_id, absolute_path)

    def test_get_batches_api(self):
        print(
            f"\nTesting {self.__class__.__name__} class with {self.ach_files_id} file id"
        )
        response = self.client.get(f"/api/v1/files/{self.ach_files_id}/batches")
        assert response.status_code == 200, response.text
        assert len(response.json()) == 5, "Should have 5 batches"

    def teardown_method(self, method: Callable) -> None:
        print(f"\nTeardown for {method.__name__} test method execution")