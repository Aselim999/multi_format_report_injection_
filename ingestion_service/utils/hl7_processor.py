from pathlib import Path

def process_hl7(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Placeholder: HL7 parsing can be done with hl7apy or similar
    return f"""{{
        "source": "hl7",
        "filename": "{file_path.name}",
        "content": "HL7 message received. Sample data: {content[:100]}"
    }}"""
