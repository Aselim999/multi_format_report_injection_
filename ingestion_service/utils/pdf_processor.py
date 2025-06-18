from pathlib import Path
import fitz  # PyMuPDF

def process_pdf(file_path: Path) -> dict:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            extracted = page.get_text()
            if extracted:
                text += extracted

        return {
            "type": "pdf",
            "filename": file_path.name,
            "content": text.strip()
        }

    except UnicodeDecodeError:
        return {
            "type": "pdf",
            "filename": file_path.name,
            "content": "⚠️ UnicodeDecodeError: Failed to decode PDF text. Try re-encoding the file."
        }

    except Exception as e:
        return {
            "type": "pdf",
            "filename": file_path.name,
            "content": f"⚠️ Error processing PDF: {str(e)}"
        }
