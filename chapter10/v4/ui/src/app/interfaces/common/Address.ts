import {AddressType} from "@/app/interfaces/common/AddressType";

export interface Address {
  addressType: AddressType;
  addressLine1: string;
  addressLine2?: string;
  addressLine3?: string;
  addressLine4?: string;
  city: string;
  state: string;
  zipCode: string;
  zipCode4?: string;
}