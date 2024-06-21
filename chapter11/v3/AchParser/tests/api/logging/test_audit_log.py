import pytest

from chapter11.v2.AchParser.app.logging.audit_log import AuditLog
from chapter11.v2.AchParser.app.logging.audit_log_record import AuditLogRecord
from chapter11.v2.AchParser.tests.ach_processor.sql_utils import SqlUtils


class TestAuditLog:

    @pytest.fixture(autouse=True)
    def setup_teardown_method(self):
        SqlUtils.truncate_all()
        yield

    def test_insert_record(self):
        log_record = AuditLogRecord(
            ip_address="192.168.1.0/24",
            user_agent="Mozilla/5.0",
            http_request="GET",
            http_response=200,
            url="http://localhost:3000/api/v1/files",
            message="Test audit log insert",
        )
        logger = AuditLog()
        audit_record_id = logger.log_record(log_record)
        retrieved_record = logger.get_log_record(audit_record_id)
        excluded_fields = {"audit_log_id", "created_at"}
        assert SqlUtils.get_row_count_of_1("audit_log") is True, "Expected 1 record"
        assert retrieved_record.dict(exclude=excluded_fields) == log_record.dict(
            exclude=excluded_fields
        ), f"Expected {log_record}, but got {retrieved_record}"
