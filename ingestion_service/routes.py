# ingestion_service/routes.py
from fastapi import APIRouter, UploadFile, File
from tasks import process_uploaded_file

router = APIRouter()

@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    contents = await file.read()
    task = process_uploaded_file.delay(file.filename, contents.decode("utf-8", errors="ignore"))
    return {"status": "queued", "task_id": task.id}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    task_id = process_uploaded_file.delay(file.filename, await file.read())
    return {"status": "queued", "task_id": str(task_id)}
