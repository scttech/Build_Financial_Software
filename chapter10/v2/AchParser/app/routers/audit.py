from fastapi import APIRouter, Request

from chapter10.v2.AchParser.app.decorators.log_message_decorator import log_message
from chapter10.v2.AchParser.app.logging.audit_log import AuditLog
from chapter10.v2.AchParser.app.logging.audit_log_record import AuditLogRecord

router = APIRouter(prefix="/api/v1/audits")


@router.get(
    path="",
    response_model=list[AuditLogRecord],
    summary="Retrieve Audit Information",
    description="Retrieve audit records for the ACH API.",
    response_description="The overview of the requested audit records.",
    tags=["Audit"],
)
@log_message("Audit Information")
async def read_audit_information(request: Request) -> list[AuditLogRecord]:
    return AuditLog().get_all_log_records()
