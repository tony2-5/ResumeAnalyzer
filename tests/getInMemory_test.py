import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.routers.task12_in_memory_storage import temp_storage

client = TestClient(app)

@pytest.fixture(autouse=True)
def initTempStorage():
    temp_storage.clear()
    temp_storage["test-session"] = {"resume": "This is a test resume."}

def testGetResumeDataSuccess():
    """
    Test successful retrieval of session data with a valid session token.
    """
    response = client.get(
        "api/resume-data",
        headers={"session-token": "test-session"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Session data retrieved successfully.",
        "data": {"resume": "This is a test resume."}
    }


def testGetDataSessionNotFound():
    response = client.get(
        "api/resume-data",
        headers={"session-token": "invalid-session"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found."}