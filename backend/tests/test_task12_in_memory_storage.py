from fastapi.testclient import TestClient
from backend.main import app 
import os

client = TestClient(app)

def test_valid_resume_upload():
    file_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    with open(file_path, "rb") as file:
        response = client.post("/api/store-resume", files={"resume_file": file})
        assert response.status_code == 200
        assert "session_id" in response.json()

def test_store_resume():
    file_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    with open(file_path, "rb") as file:
        response = client.post("/api/store-resume", files={"resume_file": file})
        assert response.status_code == 200
        assert "session_id" in response.json()

def test_store_job_description():
    file_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    with open(file_path, "rb") as file:
        response = client.post("/api/store-resume", files={"resume_file": file})
        session_id = response.json()["session_id"]

    response = client.post(
        "/api/store-job-description",
        data={"session_id": session_id, "job_description": "Sample job description."},
    )
    assert response.status_code == 200

def test_get_session_data():
    file_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    with open(file_path, "rb") as file:
        response = client.post("/api/store-resume", files={"resume_file": file})
        session_id = response.json()["session_id"]

    response = client.get(f"/api/session/{session_id}")
    assert response.status_code == 200

def test_delete_session_data():
    file_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    with open(file_path, "rb") as file:
        response = client.post("/api/store-resume", files={"resume_file": file})
        session_id = response.json()["session_id"]

    response = client.delete(f"/api/session/{session_id}")
    assert response.status_code == 200
