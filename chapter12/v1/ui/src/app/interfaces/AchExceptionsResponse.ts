
export interface AchExceptionsResponse {
    id: string;
    file_id: string;
    file_name: string;
    created_at: Date;
    batch_id: string;
    entry_id: string;
    record_number: number;
    exception_code: string;
    description: string;
}