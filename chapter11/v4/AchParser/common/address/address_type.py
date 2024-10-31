from enum import Enum


class AddressType(str, Enum):
    MAILING = "mailing"
    STREET = "street"
