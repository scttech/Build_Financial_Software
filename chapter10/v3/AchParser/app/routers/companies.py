from uuid import UUID

from fastapi import APIRouter
from starlette.requests import Request

from chapter10.v3.AchParser.app.companies.companies_sql import CompaniesSql
from chapter10.v3.AchParser.app.companies.company_detail_record import (
    CompanyDetailRecord,
)
from chapter10.v3.AchParser.app.companies.company_overview_record import (
    CompanyOverviewRecord,
)
from chapter10.v3.AchParser.app.decorators.log_message_decorator import log_message
from chapter10.v3.AchParser.common.database.files.expected_files_record import (
    ExpectedFilesRecord,
)
from chapter10.v3.AchParser.common.database.files.expected_files_sql import (
    ExpectedFilesSql,
)

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


@router.get(
    path="/{company_id}/expected_files",
    response_model=list[ExpectedFilesRecord],
    summary="Retrieve the list of expected files for a company",
    description="Returns a list of expected files for a company.",
    response_description="The expected files.",
    response_model_exclude_none=True,
    tags=["Companies"],
)
@log_message("Expected Files for Company")
async def get_expected_files(
    request: Request, company_id: UUID
) -> list[ExpectedFilesRecord]:
    return ExpectedFilesSql().get_expected_files_for_company(company_id)
