from pathlib import Path

def process_pdf(file_path: Path) -> str:
    # Placeholder: in a real app, extract text using PDF parser like PyMuPDF or pdfminer
    return f"""{{
        "source": "pdf",
        "filename": "{file_path.name}",
        "content": "PDF content extracted successfully."
    }}"""
