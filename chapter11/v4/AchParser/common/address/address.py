from typing import Optional

from pydantic import BaseModel, Field, UUID4, ConfigDict

from chapter11.v4.AchParser.common.address.address_type import AddressType


class Address(BaseModel):
    address_id: Optional[UUID4] = Field(
        None,
        title="Address ID",
        description="Unique identifier for the address.",
    )
    address_type: AddressType = Field(
        None,
        title="Address Type",
        description="Type of address.",
    )
    address_line_1: str = Field(
        None,
        title="Address Line 1",
        description="Address Line 1.",
        max_length=255,
    )
    address_line_2: Optional[str] = Field(
        None,
        title="Address Line 2",
        description="Address Line 2.",
        max_length=255,
    )
    address_line_3: Optional[str] = Field(
        None,
        title="Address Line 3",
        description="Address Line 3.",
        max_length=255,
    )
    address_line_4: Optional[str] = Field(
        None,
        title="Address Line 4",
        description="Address Line 4.",
        max_length=255,
    )
    city: Optional[str] = Field(
        None,
        title="City",
        description="City.",
        max_length=255,
    )
    state: Optional[str] = Field(
        None,
        title="State",
        description="State.",
        max_length=255,
    )
    zip_code: Optional[int] = Field(
        None, title="Postal Code", description="Postal Code."
    )
    zip_code_4: Optional[int] = Field(
        None, title="Postal Code 4", description="Postal Code 4."
    )
