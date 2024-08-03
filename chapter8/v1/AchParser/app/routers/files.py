import tempfile
from uuid import UUID

from fastapi import APIRouter, status, UploadFile, File

from chapter8.AchParserMvpNoSignOnScreen.ach_processor.ach_file_processor import AchFileProcessor
from chapter8.AchParserMvpNoSignOnScreen.ach_processor.database.ach_file_sql import AchFileSql
from chapter8.AchParserMvpNoSignOnScreen.ach_processor.database.combined_ach_records import CombinedAchRecordsSql
from chapter8.AchParserMvpNoSignOnScreen.ach_processor.schemas.api.ach_batch_entries_response import \
    AchBatchEntriesResponse
from chapter8.AchParserMvpNoSignOnScreen.ach_processor.schemas.api.ach_batches_response import AchBatchesResponse
from chapter8.AchParserMvpNoSignOnScreen.ach_processor.schemas.api.ach_files_response import AchFilesResponse
from chapter8.AchParserMvpNoSignOnScreen.ach_processor.schemas.database.ach_file_schema import AchFileSchema
from chapter8.AchParserMvpNoSignOnScreen.ach_processor.schemas.database.ach_record.ach_record_schema import \
    AchRecordSchema

router = APIRouter(prefix="/api/v1/files")


@router.get(
    "",
    response_model=list[AchFilesResponse],
    summary="Retrieve Uploaded ACH Files",
    description="Retrieve the details of an ACH file including credit/debit totals.",
    response_description="The details of the requested ACH file.",
    tags=["ACH Files"],
)
async def read_files() -> list[AchFilesResponse]:
    return AchFileSql().get_files_response()


@router.get("/{file_id}", tags=["ACH Files"])
async def read_file(file_id: UUID) -> AchFileSchema:
    return AchFileSql().get_record(file_id)


@router.get(
    "/{file_id}/batches",
    response_model=list[AchBatchesResponse],
    summary="Retrieve Details of ACH Batches in a File",
    description="Retrieve the details of ACH batches in a file including credit/debit totals.",
    response_description="The details of the requested ACH batches.",
    tags=["ACH Files"],
)
async def read_batches_from_file(file_id: UUID) -> list[AchBatchesResponse]:
    return AchFileSql().get_batches(file_id)


@router.get(
    "/{file_id}/batches/{batch_id}/entries",
    response_model=list[AchBatchEntriesResponse],
    summary="Retrieve the entries for a specific ACH batch",
    description="Retrieve the entries for a specific ACH batch",
    response_description="The entry information for the requested ACH batch.",
    tags=["ACH Files"],
)
async def read_entries_for_batch(
    file_id: UUID, batch_id: UUID
) -> list[AchBatchEntriesResponse]:
    return AchFileSql().get_entries(file_id, batch_id)


@router.post("", status_code=status.HTTP_201_CREATED, tags=["ACH Files"])
async def create_file(file: UploadFile = File(...)):
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
async def read_file_records(file_id: UUID) -> list[AchRecordSchema]:
    return CombinedAchRecordsSql().get_records(file_id)


@router.get("/{file_id}/records/{record_id}", tags=["ACH Files"])
async def read_file_record(file_id: UUID, record_id: UUID):
    return CombinedAchRecordsSql().get_record(file_id, record_id)
