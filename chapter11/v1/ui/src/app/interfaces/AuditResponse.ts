
export interface AuditResponse {
    audit_log_id: string;
    created_at: Date;
    user_id: string;
    ip_address: string;
    user_agent: string;
    http_request: string;
    http_response: number;
    url: string;
    message: string;
}