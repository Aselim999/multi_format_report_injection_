from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from tasks import process_uploaded_file

import uuid

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        file_id = str(uuid.uuid4())
        
        task = process_uploaded_file.delay(file_id, file.filename, file_bytes)
        
        return JSONResponse(
            status_code=202,
            content={
                "status": "queued",
                "task_id": task.id,
                "file_id": file_id,
                "filename": file.filename
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
