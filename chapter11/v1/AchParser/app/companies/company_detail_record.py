from typing import Optional

from pydantic import (
    Field,
    UUID4,
    BaseModel,
)

from chapter11.v1.AchParser.app.companies.industry_type import IndustryType
from chapter11.v1.AchParser.common.address.address import Address
from chapter11.v1.AchParser.common.phone.phone import Phone


class CompanyDetailRecord(BaseModel):
    company_id: Optional[UUID4] = Field(
        None,
        title="Company ID",
        description="Unique identifier for the company.",
    )
    name: Optional[str] = Field(
        None,
        title="Name",
        description="Name of the company.",
        max_length=255,
    )
    industry: Optional[IndustryType] = Field(
        None,
        title="Industry",
        description="Type of industry the company operates in.",
    )
    ach_company_id: Optional[str] = Field(
        None,
        title="ACH Company ID",
        description="ACH Company ID.",
    )
    logo: Optional[str] = Field(
        None,
        title="Logo",
        description="Base64 Image of the Logo.",
        pattern=r"^data:image\/[a-zA-Z]+;base64,[A-Za-z0-9+/=]+$",
    )
    website: Optional[str] = Field(
        None,
        title="Website",
        description="Company Website URL.",
    )
    tax_id_type: Optional[str] = Field(
        None,
        title="Tax ID Type",
        description="Type of Tax ID.",
    )
    tax_id_number: Optional[str] = Field(
        None,
        title="Tax ID Number",
        description="Tax ID Number.",
    )
    duns: Optional[int] = Field(
        None,
        title="DUNS",
        description="DUNS Number.",
    )
    addresses: Optional[list[Address]] = Field(
        None,
        title="Addresses",
        description="List of Addresses.",
    )
    phones: Optional[list[Phone]] = Field(
        None,
        title="Phones",
        description="List of Phone Numbers.",
    )
