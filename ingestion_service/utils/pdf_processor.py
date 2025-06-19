from pathlib import Path
import fitz  # PyMuPDF

def process_pdf(file_path: Path) -> dict:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            extracted = page.get_text()
            if extracted:
                try:
                    # Handle encoding for mixed Arabic/English characters
                    extracted = extracted.encode('utf-8', errors='ignore').decode('utf-8-sig', errors='ignore')
                except Exception:
                    pass
                text += extracted

        return {
            "type": "pdf",
            "filename": file_path.name,
            "content": text.strip()
        }

    except Exception as e:
        return {
            "type": "pdf",
            "filename": file_path.name,
            "content": f"⚠️ Error processing PDF: {str(e)}"
        }
