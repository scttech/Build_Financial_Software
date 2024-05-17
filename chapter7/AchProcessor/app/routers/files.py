import tempfile
from uuid import UUID

from fastapi import APIRouter, Request, status, UploadFile, File

from chapter7.AchProcessor.ach_processor.ach_file_processor import AchFileProcessor
from chapter7.AchProcessor.ach_processor.database.ach_file_sql import AchFileSql
from chapter7.AchProcessor.ach_processor.database.combined_ach_records import CombinedAchRecordsSql
from chapter7.AchProcessor.ach_processor.schemas.ach_file_schema import AchFileSchema
from chapter7.AchProcessor.ach_processor.schemas.ach_record.ach_record_schema import AchRecordSchema

router = APIRouter(prefix="/api/v1/files")

@router.get("")
async def read_files():
    return AchFileSql().get_records()

@router.get("/{file_id}")
async def read_file(file_id: UUID) -> AchFileSchema:
    return AchFileSql().get_record(file_id)

@router.post("", status_code=status.HTTP_201_CREATED)
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
    return {"filename": file.filename, "content_type": file.content_type, "last_seq": seq }

@router.get("/{file_id}/records")
async def read_file_records(file_id: UUID) -> list[AchRecordSchema]:
    return CombinedAchRecordsSql().get_records(file_id)

@router.get("/{file_id}/records/{record_id}")
async def read_file_record(file_id: UUID, record_id: UUID):
    return CombinedAchRecordsSql().get_record(file_id, record_id)
