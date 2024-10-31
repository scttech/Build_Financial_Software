from fastapi import APIRouter
from starlette.requests import Request

from chapter10.v1.AchParser.app.companies.companies_sql import CompaniesSql
from chapter10.v1.AchParser.app.companies.company_overview_record import (
    CompanyOverviewRecord,
)
from chapter10.v1.AchParser.app.decorators.log_message_decorator import log_message

router = APIRouter(prefix="/api/v1/companies")


@router.get(
    path="",
    response_model=list[CompanyOverviewRecord],
    summary="Retrieve an Overview of Companies",
    description="Return a list of defined companies.",
    response_description="An overview of the company.",
    tags=["Audit"],
)
@log_message("Company Overview")
async def get_company_overview(request: Request) -> list[CompanyOverviewRecord]:
    return CompaniesSql().get_all_companies()
