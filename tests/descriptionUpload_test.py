import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.routers.task12_in_memory_storage import temp_storage

client = TestClient(app)

@pytest.fixture(autouse=True)
def clearTempStorage():
    temp_storage.clear()


def testUploadDescriptionSuccess():
    payload = {
        "job_description": "Looking for a skilled Python developer."
    }
    headers = {"session-token": "test_token"}
    temp_storage["test_token"] = {"resume": "uploaded_resume"}
    response = client.post(
        "api/job-description",
        json=payload,
        headers=headers
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "job_description": "Looking for a skilled Python developer.",
        "token": "test_token"
    }
    assert temp_storage["test_token"]["job_description"] == "Looking for a skilled Python developer."


def testUploadDescriptionMissingDescription():
    payload = {
        "job_description": ""
    }
    headers = {"session-token": "test_token"}

    response = client.post(
        "api/job-description",
        json=payload,
        headers=headers
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Job description is required."}


def testUploadDescriptionMissingSessionToken():
    payload = {
        "job_description": "Looking for a skilled Python developer."
    }

    response = client.post(
        "api/job-description",
        json=payload
    )
    assert response.status_code == 400 
    assert "detail" in response.json()


def test_upload_job_description_resume_not_uploaded():
    payload = {
        "job_description": "Looking for a skilled Python developer."
    }
    headers = {"session-token": "invalid_token"}

    response = client.post(
        "api/job-description",
        json=payload,
        headers=headers
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Upload resume first."}