from uuid import UUID

from fastapi import APIRouter, Request, status

from chapter6.AchProcessor_V2.ach_processor.database.ach_file_sql import AchFileSql
from chapter6.AchProcessor_V2.ach_processor.database.combined_ach_records import CombinedAchRecordsSql
from chapter6.AchProcessor_V2.ach_processor.schemas.ach_file_schema import AchFileSchema

router = APIRouter(prefix="/api/v1/files")

@router.get("")
async def read_files():
    return AchFileSql().get_records()

@router.get("/{file_id}")
async def read_file(file_id: UUID) -> AchFileSchema:
    return AchFileSql().get_record(file_id)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_file(request: Request):
    data = await request.json()
    return {"file": f"{data['file']}"}

@router.get("/{file_id}/records")
async def read_file_records(file_id: UUID):
    return CombinedAchRecordsSql().get_records(file_id)

@router.get("/{file_id}/records/{record_id}")
async def read_file_record(file_id: UUID, record_id: UUID):
    return CombinedAchRecordsSql().get_record(file_id, record_id)
