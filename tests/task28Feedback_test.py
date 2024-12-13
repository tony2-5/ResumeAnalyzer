from fastapi.testclient import TestClient
from backend.main import app
from backend.routers.task12_in_memory_storage import temp_storage

client = TestClient(app)

def testValidFeedbackResponse():
    """
    Test that the feedback and fit score are returned correctly.
    """
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": "Valid resume text here.",
        "job_description": "Valid job description here."
    }
    payload = {
        "resumeText": "Experienced Python developer with REST API experience.",
        "jobDescription": "Looking for a Python developer with REST API experience and AWS knowledge."
    }
    headers= {
        'sessionToken': "test_token"
    }
    response = client.post("/api/fit-score", json=payload, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "fitScore" in data
    assert "matchedKeywords" in data
    assert "missingKeywords" in data
    assert "feedback" in data

def testMissingJobDescription():
    """
    Test that the API returns an error when fields are missing.
    """
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": "Valid resume text here.",
    }
    payload = {
        "resumeText": "Experienced Python developer with REST API experience.",
    }
    headers= {
        'sessionToken': "test_token"
    }
    response = client.post("/api/fit-score", json=payload,headers=headers)
    assert response.status_code == 400
    assert "jobDescription" in response.json()["detail"][0]["loc"]

def testMissingResume():
    """
    Test that the API returns an error when fields are missing.
    """
    temp_storage.clear()
    temp_storage["test_token"] = {
        "job_description": "Valid job description here."
    }
    payload = {
        "jobDescription": "Looking for a Python developer with REST API experience and AWS knowledge."
    }
    headers= {
        'sessionToken': "test_token"
    }
    response = client.post("/api/fit-score", json=payload, headers=headers)
    assert response.status_code == 400
    assert "resumeText" in response.json()["detail"][0]["loc"]

def testOversizedInput():
    """
    Test that the API handles oversized input.
    """
    oversizedText = "A" * 10001  # Exceeds character limit
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": oversizedText,
        "job_description": oversizedText
    }
    payload = {"resumeText": oversizedText, "jobDescription": oversizedText}
    headers= {
        'sessionToken': "test_token"
    }
    response = client.post("/api/fit-score", json=payload, headers=headers)
    assert response.status_code == 400 
    assert "resumeText" in response.json()["detail"][0]["loc"]

def testInvalidResume():
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": 123456789,
        "job_description": "Valid job description here."
    }
    payload = {
        "resumeText": 123456789,  # Invalid format: not a string
        "jobDescription": "Valid job description here."
    }
    headers= {
        'sessionToken': "test_token"
    }
    response = client.post("/api/fit-score", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"][0]["msg"] == 'Input should be a valid string'

def testInvalidDescription():
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": "Valid resume.",
        "job_description": 123456789
    }
    payload = {
        "resumeText": "Valid resume.",
        "jobDescription": 123456789 # Invalid format: not a string
    }
    headers= {
        'sessionToken': "test_token"
    }
    response = client.post("/api/fit-score", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"][0]["msg"] == 'Input should be a valid string'