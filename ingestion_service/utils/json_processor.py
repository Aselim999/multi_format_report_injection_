import json
from pathlib import Path

def process_json(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Placeholder: You may normalize or extract specific keys here
    return json.dumps({
        "source": "json",
        "filename": file_path.name,
        "content": data
    }, ensure_ascii=False)
