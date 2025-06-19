from celery import Celery
import os
import json
from datetime import datetime, date
from utils.file_handlers import (
    process_pdf, process_word, process_json,
    process_sql, process_hl7, process_dicom
)

from sqlalchemy.orm import Session
from db.models import IngestionLog, IngestionContent
from db.session import SessionLocal 
from utils.fhir_mapper import build_patient_resource, build_observation, build_diagnostic_report

celery_app = Celery("worker", broker="redis://redis:6379/0")

def default_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return str(obj)

@celery_app.task(name="ingestion_service.tasks.process_uploaded_file")
def process_uploaded_file(file_id, filename, content_bytes):
    ext = os.path.splitext(filename)[-1].lower()
    
    # Parse file
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

    parsed["file_id"] = file_id
    parsed["filename"] = filename

    # FHIR Resource Generation
    fhir_resources = None
    if "error" not in parsed:
        try:
            patient = build_patient_resource(name="Default User")
            observation = build_observation(value=str(parsed.get("content", "No content")))
            report = build_diagnostic_report(patient, observation)

            fhir_resources = {
                "patient": patient.dict(),
                "observation": observation.dict(),
                "report": report.dict()
            }

            parsed["fhir"] = fhir_resources
        except Exception as e:
            parsed["fhir_error"] = f"FHIR generation failed: {str(e)}"

    # Save output to file
    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/{file_id}_{filename}.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, default=default_serializer)

    # Log into DB
    db = None
    try:
        db: Session = SessionLocal()
        print("Inserting log into DB...")
        log = IngestionLog(
            file_id=file_id,
            filename=filename,
            type=parsed.get("type", "unknown"),
            status="success" if "error" not in parsed else "error",
            error=parsed.get("error"),
            content=str(parsed.get("content"))[:300],
        )
        full = IngestionContent(
            file_id=file_id,
            full_content=json.dumps(parsed.get("content", {}), default=default_serializer),
            fhir_data=json.dumps(fhir_resources, default=default_serializer) if fhir_resources else None
        )
        db.add(log)
        db.add(full)
        db.commit()
        print("✅ Log inserted successfully")

    except Exception as e:
        print(f"❌ Failed to log ingestion record: {e}")

    finally:
        if db:
            db.close()

    return parsed
