from fastapi.testclient import TestClient
from API.main import app  # Import the main FastAPI app

client = TestClient(app)

def test_valid_feedback_response():
    """
    Test that the feedback and fit score are returned correctly.
    """
    payload = {
        "resume_text": "Experienced Python developer with REST API experience.",
        "job_description": "Looking for a Python developer with REST API experience and AWS knowledge."
    }
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "fit_score" in data
    assert "feedback" in data
    assert isinstance(data["fit_score"], int)  # Fit score should be an integer
    assert isinstance(data["feedback"], list)  # Feedback should be a list of strings

def test_missing_fields():
    """
    Test that the API returns an error when fields are missing.
    """
    payload = {"resume_text": "Missing job description"}
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 422  # 修改为 422
    assert "job_description" in response.json()["detail"][0]["loc"]


def test_oversized_input():
    """
    Test that the API handles oversized input.
    """
    oversized_text = "A" * 10001  # Exceeds character limit
    payload = {"resume_text": oversized_text, "job_description": oversized_text}
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 422  # 修改为 422
    assert "resume_text" in response.json()["detail"][0]["loc"]
