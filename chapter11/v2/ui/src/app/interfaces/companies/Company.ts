import {TinType} from "@/app/interfaces/common/TinType";
import {IndustryType} from "@/app/interfaces/common/IndustryType";
import {Phone} from "@/app/interfaces/common/Phone";
import {Address} from "@/app/interfaces/common/Address";

export interface Company {
  name: string;
  taxIdType: TinType;
  taxIdNumber: string;
  duns: number;
  logo?: string | null;
  website?: string;
  industry?: IndustryType;
  addresses: Address[];
  phones: Phone[];
}