# TODO: implement utils.py
from typing import Optional
# from ingestion_service.tasks import process_uploaded_file
import mimetypes

SUPPORTED_TYPES = {
    ".pdf": "PDF",
    ".docx": "WORD",
    ".doc": "WORD",
    ".json": "JSON",
    ".hl7": "HL7",
    ".sql": "SQL",
    ".dcm": "DICOM"
}

def enqueue_file_task(filename: str, content: bytes, file_type: str):
    # Call the background task
    process_uploaded_file.delay(filename, content, file_type)

def validate_file_type(filename: str) -> Optional[str]:
    for ext in SUPPORTED_TYPES:
        if filename.lower().endswith(ext):
            return SUPPORTED_TYPES[ext]
    return None

def enqueue_file_task(filename: str, content: bytes, file_type: str):
    # TODO: implement Redis/RabbitMQ queue logic later
    print(f"[QUEUE] Enqueued {filename} of type {file_type}")
