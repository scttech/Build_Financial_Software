
export interface AchExceptionDetailsResponse {
    id: string;
    created_at: Date;
    exception_code: string;
    description: string;
    unparsed_record: string;
    company_name: string;
    recovery_option: string;
}