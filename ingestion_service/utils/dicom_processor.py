from pathlib import Path

def process_dicom(file_path: Path) -> str:
    # Placeholder: real parsing with pydicom
    return f"""{{
        "source": "dicom",
        "filename": "{file_path.name}",
        "content": "DICOM metadata parsed successfully."
    }}"""
