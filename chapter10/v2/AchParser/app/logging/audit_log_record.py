from datetime import datetime
from typing import Optional

from pydantic import (
    Field,
    UUID4,
    BaseModel,
    IPvAnyNetwork,
    AnyUrl,
    field_validator,
)


class AuditLogRecord(BaseModel):
    audit_log_id: Optional[UUID4] = Field(
        None,
        title="Audit Log ID",
        description="Unique identifier for the audit log entry.",
    )
    created_at: Optional[datetime] = Field(
        None,
        title="Created At",
        description="Timestamp when the audit log entry was created.",
    )
    user_id: Optional[str] = Field(
        None,
        title="User ID",
        description="Identifier for the user associated with the audit log entry.",
        max_length=25,
    )
    ip_address: Optional[IPvAnyNetwork] = Field(
        None,
        title="IP Address",
        description="IP address from which the request originated.",
    )
    user_agent: Optional[str] = Field(
        None,
        title="User Agent",
        description="User agent string of the client's browser.",
        max_length=255,
    )
    http_request: Optional[str] = Field(
        None,
        title="HTTP Request",
        description="HTTP request method used.",
        max_length=7,
    )
    http_response: Optional[int] = Field(
        None,
        title="HTTP Response",
        description="HTTP response status code returned.",
        ge=100,
        le=599,
    )
    url: Optional[AnyUrl] = Field(
        None, title="URL", description="URL accessed by the request.", max_length=255
    )
    message: str = Field(
        ..., title="Message", description="Description of the audit log event."
    )

    @field_validator("url", mode="before")
    @classmethod
    def convert_url_to_str(cls, v: AnyUrl) -> str:
        return str(v)

    class Config:
        json_schema_extra = {
            "example": {
                "audit_log_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "created_at": "2024-05-25T12:34:56",
                "user_id": "user123",
                "ip_address": "192.168.0.1",
                "user_agent": "Mozilla/5.0",
                "http_request": "GET",
                "http_response": 200,
                "url": "http://example.com",
                "message": "User viewed ACH file",
            }
        }
