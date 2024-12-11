from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def testValidFeedbackResponse():
    """
    Test that the feedback and fit score are returned correctly.
    """
    payload = {
        "resumeText": "Experienced Python developer with REST API experience.",
        "jobDescription": "Looking for a Python developer with REST API experience and AWS knowledge."
    }
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert "fitScore" in data
    assert "feedback" in data
    assert isinstance(data["fitScore"], int)  # Fit score should be an integer
    assert isinstance(data["feedback"], list)  # Feedback should be a list of strings

def testMissingJobDescription():
    """
    Test that the API returns an error when fields are missing.
    """
    payload = {"resumeText": "Missing job description"}
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 400
    assert "jobDescription" in response.json()["detail"][0]["loc"]

def testMissingResume():
    """
    Test that the API returns an error when fields are missing.
    """
    payload = {"jobDescription": "Missing resume"}
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 400
    assert "resumeText" in response.json()["detail"][0]["loc"]

def testOversizedInput():
    """
    Test that the API handles oversized input.
    """
    oversized_text = "A" * 10001  # Exceeds character limit
    payload = {"resumeText": oversized_text, "jobDescription": oversized_text}
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 400 
    assert "resumeText" in response.json()["detail"][0]["loc"]

def testInvalidResume():
    payload = {
        "resumeText": 123456789,  # Invalid format: not a string
        "jobDescription": "Valid job description here."
    }
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"][0]["msg"] == 'Input should be a valid string'

def testInvalidDescription():
    payload = {
        "resumeText": "Valid resume.",
        "jobDescription": 123456789 # Invalid format: not a string
    }
    response = client.post("/api/fit-score", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"][0]["msg"] == 'Input should be a valid string'