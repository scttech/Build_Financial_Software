import {AddressType} from "@/app/interfaces/common/AddressType";

export interface CompanyAddressResponse {
  address_type: AddressType;
  address_line_1: string;
  address_line_2?: string;
  address_line_3?: string;
  address_line_4?: string;
  city: string;
  state: string;
  zip_code: string;
  zip_code_4?: string;
}