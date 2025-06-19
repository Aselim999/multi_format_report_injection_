from pathlib import Path

def process_sql(file_path: Path) -> dict:
    try:
        # Try reading with utf-8
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            # Fallback to utf-16 if utf-8 fails
            content = file_path.read_text(encoding="utf-16")
        except UnicodeDecodeError:
            return {
                "type": "sql",
                "error": "Unsupported encoding format",
                "file_id": str(file_path.stem),
                "filename": file_path.name
            }

    return {
        "type": "sql",
        "content": content[:1000],  # Trim to avoid huge payloads
        "file_id": str(file_path.stem),
        "filename": file_path.name
    }
