import {ScheduleType} from "@/app/interfaces/common/ScheduleType";

export interface CompanyExpectedFilesResponse {
    company_expected_file_id: string;
    file_name: string;
    schedule: ScheduleType;
    file_type: boolean;
    last_file_date: Date;
    next_file_date: Date;
}