from celery import Celery
import os
import json
from utils.file_handlers import (
    process_pdf, process_word, process_json,
    process_sql, process_hl7, process_dicom
)

celery_app = Celery("worker", broker="redis://redis:6379/0")

@celery_app.task(name="ingestion_service.tasks.process_uploaded_file")
def process_uploaded_file(file_id, filename, content_bytes):
    ext = os.path.splitext(filename)[-1].lower()
    
    # Select the correct parser based on file extension
    if ext == ".pdf":
        parsed = process_pdf(content_bytes)
    elif ext in [".docx", ".doc"]:
        parsed = process_word(content_bytes)
    elif ext == ".json":
        parsed = process_json(content_bytes)
    elif ext == ".sql":
        parsed = process_sql(content_bytes)
    elif ext == ".hl7" or "hl7" in filename.lower():
        parsed = process_hl7(content_bytes)
    elif ext == ".dcm":
        parsed = process_dicom(content_bytes)
    else:
        parsed = {"error": "Unsupported file type", "filename": filename}

    # Add metadata
    parsed["file_id"] = file_id
    parsed["filename"] = filename

    # Save output to JSON
    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/{file_id}_{filename}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)

    return parsed