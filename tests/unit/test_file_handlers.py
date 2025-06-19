import json
from app.utils.file_handlers import process_json

def test_process_json_valid():
    # Arrange
    valid_content = json.dumps({
        "patient": "John Doe",
        "age": 35,
        "diagnosis": "Hypertension"
    }).encode("utf-8")  # simulate file bytes

    # Act
    result = process_json(valid_content)

    # Assert
    assert isinstance(result, dict)
    assert result["type"] == "json"
    assert result["content"]["patient"] == "John Doe"
def test_process_json_invalid():
    invalid_content = b"{ bad json"

    result = process_json(invalid_content)

    assert "error" in result
    assert result["type"] == "json"
