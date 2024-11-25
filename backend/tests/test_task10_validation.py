# backend/tests/test_task10_validation.py

from fastapi.testclient import TestClient
from backend.main import app 
import os

client = TestClient(app)

def test_valid_resume_upload():
    file_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    with open(file_path, "rb") as file:
        response = client.post("/api/resume-upload", files={"resume_file": file})
        assert response.status_code == 200
        assert response.json()["message"] == "Resume uploaded successfully."

def test_invalid_resume_file_type():
    file_path = os.path.join(os.path.dirname(__file__), "sample.txt")
    with open(file_path, "rb") as file:
        response = client.post("/api/resume-upload", files={"resume_file": file})
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid file type. Only PDF files are allowed."
