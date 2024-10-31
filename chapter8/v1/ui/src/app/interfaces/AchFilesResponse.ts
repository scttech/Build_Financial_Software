
export interface AchFilesResponse {
    id: string;
    date: string;
    filename: string;
    originator: string;
    credit_total: number;
    debit_total: number;
    has_exceptions: boolean;
}