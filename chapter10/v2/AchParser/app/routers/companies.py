from uuid import UUID

from fastapi import APIRouter
from starlette.requests import Request

from chapter10.v2.AchParser.app.companies.companies_sql import CompaniesSql
from chapter10.v2.AchParser.app.companies.company_detail_record import (
    CompanyDetailRecord,
)
from chapter10.v2.AchParser.app.companies.company_overview_record import (
    CompanyOverviewRecord,
)
from chapter10.v2.AchParser.app.decorators.log_message_decorator import log_message

router = APIRouter(prefix="/api/v1/companies")


@router.get(
    path="",
    response_model=list[CompanyOverviewRecord],
    summary="Retrieve an Overview of Companies",
    description="Return a list of defined companies.",
    response_description="An overview of the company.",
    tags=["Companies"],
)
@log_message("Company Overview")
async def get_company_overview(request: Request) -> list[CompanyOverviewRecord]:
    return CompaniesSql().get_all_companies()


@router.get(
    path="/{company_id}",
    response_model=CompanyDetailRecord,
    summary="Retrieve a Company",
    description="Return a company by its ID.",
    response_description="The company.",
    tags=["Companies"],
)
@log_message("Company Detail")
async def get_company(request: Request, company_id: UUID) -> CompanyDetailRecord:
    return CompaniesSql().get_company_by_id(company_id)
