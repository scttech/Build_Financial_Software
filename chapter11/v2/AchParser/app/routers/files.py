import tempfile
from uuid import UUID

from fastapi import (
    APIRouter,
    status,
    UploadFile,
    File,
    HTTPException,
    Depends,
    Security,
    Query,
    Request,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from chapter11.v2.AchParser.ach_processor.ach_file_processor import AchFileProcessor
from chapter11.v2.AchParser.ach_processor.database.ach_combined_records_sql import (
    AchCombinedRecordsSql,
)
from chapter11.v2.AchParser.ach_processor.database.ach_file_sql import AchFileSql
from chapter11.v2.AchParser.ach_processor.database.exception.ach_exceptions_sql import (
    AchExceptionsSql,
)
from chapter11.v2.AchParser.ach_processor.database.search.batch_search_sql import (
    BatchSearchSql,
)
from chapter11.v2.AchParser.ach_processor.database.search.transaction_search_sql import (
    TransactionSearchSql,
)
from chapter11.v2.AchParser.ach_processor.schemas.api.ach_batch_entries_response import (
    AchBatchEntriesResponse,
)
from chapter11.v2.AchParser.ach_processor.schemas.api.ach_batches_response import (
    AchBatchesResponse,
)
from chapter11.v2.AchParser.ach_processor.schemas.api.ach_exception_details_response import (
    AchExceptionDetailsResponse,
)
from chapter11.v2.AchParser.ach_processor.schemas.api.ach_exceptions_response import (
    AchExceptionsResponse,
)
from chapter11.v2.AchParser.ach_processor.schemas.api.ach_files_response import (
    AchFilesResponse,
)
from chapter11.v2.AchParser.ach_processor.schemas.api.batch_search_response import (
    BatchSearchResponse,
)
from chapter11.v2.AchParser.ach_processor.schemas.api.transaction_search_response import (
    TransactionSearchResponse,
)
from chapter11.v2.AchParser.ach_processor.schemas.database.ach_file_schema import (
    AchFileSchema,
)
from chapter11.v2.AchParser.ach_processor.schemas.database.ach_record.ach_record_schema import (
    AchRecordSchema,
)
from chapter11.v2.AchParser.app.decorators.log_message_decorator import log_message

router = APIRouter(prefix="/api/v1/files")
security_scheme_http_bearer = HTTPBearer()


@router.get(
    path="",
    response_model=list[AchFilesResponse],
    summary="Retrieve Uploaded ACH Files",
    description="Retrieve the details of an ACH file including credit/debit totals.",
    response_description="The details of the requested ACH file.",
    tags=["ACH Files"],
)
@log_message("Retrieving ACH files")
async def read_files(request: Request) -> list[AchFilesResponse]:
    return AchFileSql().get_files_response()


@router.get(
    path="/transactions/search",
    response_model=list[TransactionSearchResponse],
    summary="Retrieve ACH Transactions",
    description="Retrieve the transactions matching the specified criteria.",
    response_description="ACH Transactions.",
    response_model_exclude_none=True,
    tags=["ACH Files"],
)
@log_message("Retrieving ACH transactions")
async def get_ach_transactions(
    request: Request,
    criteria: str = Query(..., description="Search criteria for transactions"),
) -> list[TransactionSearchResponse]:
    return TransactionSearchSql().get_transactions(criteria)


@router.get(
    path="/batches/search",
    response_model=list[BatchSearchResponse],
    summary="Retrieve ACH Batches",
    description="Retrieve the batches matching the specified criteria.",
    response_description="ACH Batches.",
    response_model_exclude_none=True,
    tags=["ACH Files"],
)
@log_message("Retrieving ACH batches")
async def search_ach_batches(
    request: Request,
    criteria: str = Query(..., description="Search criteria for batches"),
) -> list[BatchSearchResponse]:
    return BatchSearchSql().get_batches(criteria)


@router.get(
    path="/exceptions",
    response_model=list[AchExceptionsResponse],
    summary="Retrieve ACH File Exceptions",
    description="Retrieve the exceptions in an ACH file.",
    response_description="The exceptions in the requested ACH file.",
    response_model_exclude_none=True,
    tags=["ACH Files"],
)
@log_message("Retrieving ACH exceptions for all files")
async def read_exceptions_for_all_files(
    request: Request,
) -> list[AchExceptionsResponse]:
    return AchExceptionsSql().get_exceptions_response()


@router.get("/{file_id}", tags=["ACH Files"])
@log_message("Get a specific ACH file")
async def read_file(request: Request, file_id: UUID) -> AchFileSchema:
    return AchFileSql().get_record(file_id)


@router.get(
    path="/{file_id}/exceptions",
    response_model=list[AchExceptionsResponse],
    summary="Retrieve ACH File Exceptions",
    description="Retrieve the exceptions in an ACH file.",
    response_description="The exceptions in the requested ACH file.",
    response_model_exclude_none=True,
    tags=["ACH Files"],
)
@log_message("Get ACH exceptions for a specific file")
async def read_exceptions_for_file(
    request: Request, file_id: UUID
) -> list[AchExceptionsResponse]:
    return AchExceptionsSql().get_exceptions_response(file_id)


@router.get(
    path="/{file_id}/exceptions/{exception_id}",
    response_model=AchExceptionDetailsResponse,
    summary="Retrieve the ACH exception details and unparsed record",
    description="Retrieve the exception details and unparsed record for a specific ACH exception.",
    response_description="The exception details and unparsed record for the requested ACH exception.",
    response_model_exclude_none=True,
    tags=["ACH Files"],
)
@log_message("User retrieved ACH exception details")
async def read_exceptions_for_file(
    request: Request, file_id: UUID, exception_id: UUID
) -> AchExceptionDetailsResponse:
    return AchExceptionsSql().get_exception_detail_response(file_id, exception_id)


@router.get(
    "/{file_id}/batches",
    response_model=list[AchBatchesResponse],
    summary="Retrieve Details of ACH Batches in a File",
    description="Retrieve the details of ACH batches in a file including credit/debit totals.",
    response_description="The details of the requested ACH batches.",
    tags=["ACH Files"],
)
@log_message("User retrieved ACH batches for a file")
async def read_batches_from_file(
    request: Request, file_id: UUID
) -> list[AchBatchesResponse]:
    return AchFileSql().get_batches(file_id)


async def verify_token(
    auth: HTTPAuthorizationCredentials = Security(security_scheme_http_bearer),
):
    print(f"The token is {auth.credentials} and the scheme is {auth.scheme}")
    if auth.scheme != "Bearer" or auth.credentials != "secret_token":
        print(f"Invalid token {auth.credentials}, raising exception")
        raise HTTPException(status_code=400, detail="Invalid token")
    return auth


@router.get(
    "/{file_id}/batches/{batch_id}/entries",
    response_model=list[AchBatchEntriesResponse],
    summary="Retrieve the entries for a specific ACH batch",
    description="Retrieve the entries for a specific ACH batch",
    response_description="The entry information for the requested ACH batch.",
    tags=["ACH Files"],
)
@log_message("User retrieved ACH entries for a batch")
async def read_entries_for_batch(
    request: Request, file_id: UUID, batch_id: UUID
) -> list[AchBatchEntriesResponse]:
    return AchFileSql().get_entries(file_id, batch_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    tags=["ACH Files"],
    dependencies=[Depends(verify_token)],
)
@log_message("User uploaded an ACH file")
async def create_file(request: Request, file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        data = await file.read()
        # Create temporary file
        temp_file.write(data)

    parser = AchFileProcessor()
    ach_file = AchFileSchema(file_name=file.filename, file_hash=file.content_type)
    ach_files_id = AchFileSql().insert_record(ach_file)
    try:
        print(f"Processing file {temp_file.name}")
        seq = parser.parse(ach_files_id, temp_file.name)
    except Exception as e:
        print(e)
        return {"error": "Invalid file"}
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "last_seq": seq,
    }


@router.get("/{file_id}/records", tags=["ACH Files"])
@log_message("User retrieved records for a file")
async def read_file_records(request: Request, file_id: UUID) -> list[AchRecordSchema]:
    return AchCombinedRecordsSql().get_records(file_id)


@router.get("/{file_id}/records/{record_id}", tags=["ACH Files"])
@log_message("User retrieved specific record for a file")
async def read_file_record(request: Request, file_id: UUID, record_id: UUID):
    return AchCombinedRecordsSql().get_record(file_id, record_id)
