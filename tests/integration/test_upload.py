import requests

def test_upload_sample_json():
    token = "your_test_token_here"
    files = {"file": ("sample.json", b'{"test": "value"}')}
    response = requests.post(
        "http://localhost:8000/upload?token=" + token,
        files=files
    )
    assert response.status_code == 202
    data = response.json()
    assert "file_id" in data
    assert "task_id" in data
