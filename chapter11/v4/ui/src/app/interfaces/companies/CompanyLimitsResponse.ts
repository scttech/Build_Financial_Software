export interface CompanyLimitsResponse {
    company_limit_id: string;
    daily_debit_limit: number;
    daily_credit_limit: number;
    current_debit_total: number;
    current_credit_total: number;
    daily_debit_exceeded: boolean;
    daily_credit_exceeded: boolean;
}