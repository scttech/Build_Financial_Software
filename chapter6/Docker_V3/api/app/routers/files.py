from fastapi import APIRouter, Request, status, File, UploadFile

router = APIRouter(prefix="/api/v1/files")

@router.get("")
async def read_files():
    return [{"file": "File_1"}, {"file": "File_2"}]

@router.get("/{file_id}")
async def read_file(file_id: str) -> str:
    return {"file_id": "1"}

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_file(file: UploadFile = File(...)):
    return None

@router.get("/{file_id}/records")
async def read_file_records(file_id: str):
    return [{"record": "Record_1"}, {"record": "Record_2"}]

@router.get("/{file_id}/records/{record_id}")
async def read_file_record(file_id: str, record_id: str):
    return {"file_id": file_id, "record_id": record_id}
