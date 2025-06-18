# ingestion_service/tasks.py
from celery_app import app

@app.task
def process_uploaded_file(filename, content):
    print(f"Processing {filename}")
    # For now, just print. Later, call file-specific processors.
    return {"filename": filename, "length": len(content)}

# ingestion_service/tasks.py
from celery_app import app
import magic
import mimetypes
from utils.pdf_processor import process_pdf
from utils.json_processor import process_json

@app.task
def process_uploaded_file(filename, content):
    print(f"Processing {filename}")
    extension = filename.split('.')[-1].lower()

    if extension == "pdf":
        return process_pdf(content, filename)
    elif extension == "json":
        return process_json(content, filename)
    else:
        print(f"Unsupported file type: {extension}")
        return {"status": "unsupported", "filename": filename}


from celery import Celery
from pathlib import Path
import os
import magic  # file type detection
import uuid

from utils.pdf_processor import process_pdf
from utils.json_processor import process_json
from utils.hl7_processor import process_hl7
from utils.dicom_processor import process_dicom

app = Celery("worker", broker="redis://redis:6379/0")

UPLOAD_DIR = "/app/uploads"

@app.task(bind=True)
def process_uploaded_file(self, file_path):
    try:
        full_path = Path(UPLOAD_DIR) / file_path
        file_type = magic.from_file(str(full_path), mime=True)

        if "pdf" in file_type:
            result = process_pdf(full_path)
        elif "json" in file_type:
            result = process_json(full_path)
        elif "hl7" in full_path.name.lower():
            result = process_hl7(full_path)
        elif "dicom" in file_type or full_path.suffix.lower() in ['.dcm']:
            result = process_dicom(full_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Simulate saving result to DB or return output
        task_id = str(uuid.uuid4())
        output_file = Path("/app/outputs") / f"{task_id}.json"
        output_file.write_text(result, encoding="utf-8")

        return {"status": "completed", "task_id": task_id}

    except Exception as e:
        self.retry(exc=e, countdown=10, max_retries=3)
        return {"status": "failed", "error": str(e)}
