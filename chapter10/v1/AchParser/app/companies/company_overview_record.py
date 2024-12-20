from typing import Optional

from pydantic import (
    Field,
    UUID4,
    BaseModel,
)

from chapter10.v1.AchParser.app.companies.industry_type import IndustryType


class CompanyOverviewRecord(BaseModel):
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
    logo: Optional[str] = Field(
        None,
        title="Logo",
        description="Base64 Image of the Logo.",
    )
