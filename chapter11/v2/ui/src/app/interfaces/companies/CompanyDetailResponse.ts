import {TinType} from "@/app/interfaces/common/TinType";
import {Phone} from "@/app/interfaces/common/Phone";
import {Address} from "@/app/interfaces/common/Address";
import {CompanyAddressResponse} from "@/app/interfaces/companies/CompanyAddressResponse";
import {CompanyPhoneResponse} from "@/app/interfaces/companies/CompanyPhoneResponse";

export interface CompanyDetailResponse {
    company_id: string;
    name: string;
    industry: string;
    logo: string;
    website: string;
    tax_id_type: TinType;
    tax_id_number: string;
    duns: number;
    addresses: CompanyAddressResponse[];
    phones: CompanyPhoneResponse[];
}