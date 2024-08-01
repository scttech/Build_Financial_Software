from fastapi import APIRouter, Request, status

router = APIRouter()

@router.get("/files")
async def read_files():
    return [{"file": "File_1"}, {"file": "File_2"}]

@router.get("/files/{file_id}")
async def read_file(file_id: str):
    return {"file_id": file_id}

@router.post("/files", status_code=status.HTTP_201_CREATED)
async def create_file(request: Request):
    data = await request.json()
    return {"file": f"{data['file']}"}

@router.get("/files/{file_id}/records")
async def read_file_records(file_id: str):
    return [{"record": "Record_1"}, {"record": "Record_2"}]

@router.get("/files/{file_id}/records/{record_id}")
async def read_file_record(file_id: str, record_id: str):
    return {"file_id": file_id, "record_id": record_id}
