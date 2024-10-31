from psycopg.rows import class_row, dict_row

from chapter10.v3.AchParser.ach_processor.database.db_utils import get_db_connection
from chapter10.v3.AchParser.app.logging.audit_log_record import AuditLogRecord


class AuditLog:
    @staticmethod
    def log_record(log_record: AuditLogRecord):
        with get_db_connection(row_factory=dict_row) as conn:
            log_record_dict = log_record.dict()
            log_record_dict["url"] = str(log_record_dict["url"])
            result = conn.execute(
                """
           INSERT INTO audit_log (user_id, ip_address, user_agent, http_request, http_response, url, message)
           VALUES (%(user_id)s, 
                %(ip_address)s, 
                %(user_agent)s, 
                %(http_request)s, 
                %(http_response)s, 
                %(url)s, 
                %(message)s
                )
           RETURNING audit_log_id
            """,
                log_record_dict,
            )

        return result.fetchone()["audit_log_id"]

    @staticmethod
    def get_log_record(audit_log_id: str) -> AuditLogRecord:
        with get_db_connection(row_factory=class_row(AuditLogRecord)) as conn:
            result = conn.execute(
                """
                SELECT *
                FROM audit_log
                WHERE audit_log_id = %(audit_log_id)s
                """,
                {"audit_log_id": audit_log_id},
            )

        return result.fetchone()

    @staticmethod
    def get_all_log_records() -> list[AuditLogRecord]:
        with get_db_connection(row_factory=class_row(AuditLogRecord)) as conn:
            result = conn.execute(
                """
                SELECT *
                FROM audit_log
                """
            )

        return result.fetchall()
