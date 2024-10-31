import {PhoneType} from "@/app/interfaces/common/PhoneType";

export interface CompanyPhoneResponse {
  phone_type: PhoneType;
  phone_number: string;
  extension?: string;
  allow_sms: boolean;
}