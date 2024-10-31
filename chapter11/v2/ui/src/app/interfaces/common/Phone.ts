import {PhoneType} from "@/app/interfaces/common/PhoneType";

export interface Phone {
  phoneType: PhoneType;
  phoneNumber: string;
  extension?: string;
  allowSms: boolean;
}