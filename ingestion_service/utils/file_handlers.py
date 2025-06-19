import json
import os
from io import BytesIO
from typing import Any, Dict
from PyPDF2 import PdfReader
import docx
import fitz  # PyMuPDF for fallback PDF parsing
import hl7
import pydicom
from utils.dicom_sr_processor import process_dicom_sr


def process_pdf(file_bytes: bytes) -> Dict[str, Any]:
    try:
        reader = PdfReader(BytesIO(file_bytes))
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return {"type": "pdf", "content": text}
    except Exception as e:
        return {"type": "pdf", "error": str(e)}

def process_word(file_bytes: bytes) -> Dict[str, Any]:
    try:
        doc = docx.Document(BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return {"type": "word", "content": text}
    except Exception as e:
        return {"type": "word", "error": str(e)}

def process_json(file_bytes: bytes) -> Dict[str, Any]:
    try:
        data = json.loads(file_bytes.decode('utf-8'))
        return {"type": "json", "content": data}
    except Exception as e:
        return {"type": "json", "error": str(e)}

def process_sql(file_bytes: bytes) -> Dict[str, Any]:
    try:
        sql_text = file_bytes.decode("utf-8")
        return {"type": "sql", "statements": sql_text}
    except Exception as e:
        return {"type": "sql", "error": str(e)}

def process_hl7(file_bytes: bytes) -> Dict[str, Any]:
    try:
        msg_text = file_bytes.decode("utf-8")
        msg = hl7.parse(msg_text)
        return {"type": "hl7", "segments": [str(segment) for segment in msg]}
    except Exception as e:
        return {"type": "hl7", "error": str(e)}

def process_dicom(file_bytes: bytes) -> Dict[str, Any]:
    try:
        ds = pydicom.dcmread(BytesIO(file_bytes))

        # If this is a Structured Report, delegate to the SR processor
        if hasattr(ds, "ContentSequence"):
            return process_dicom_sr(ds)

        # Otherwise, return basic metadata
        extracted = {
            "PatientName": str(ds.get("PatientName", "")),
            "StudyDate": str(ds.get("StudyDate", "")),
            "Modality": str(ds.get("Modality", "")),
            "StudyDescription": str(ds.get("StudyDescription", "")),
        }
        return {"type": "dicom", "content": extracted}
    except Exception as e:
        return {"type": "dicom", "error": str(e)}

