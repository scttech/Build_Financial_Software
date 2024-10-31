from typing import Optional

from pydantic import BaseModel, Field, UUID4

from chapter11.v4.AchParser.common.phone.phone_type import PhoneType


class Phone(BaseModel):
    phone_id: Optional[UUID4] = Field(
        None,
        title="Phone ID",
        description="Unique identifier for the phone number.",
    )
    phone_type: PhoneType = Field(
        None,
        title="Phone Type",
        description="Type of phone number.",
    )
    phone_number: int = Field(
        None,
        title="Phone Number",
        description="Phone number.",
    )
    extension: Optional[int] = Field(
        None,
        title="Extension",
        description="Phone number extension.",
        max_length=10,
    )
