import pytest
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch
from backend.routers.analyze import parseResponse
from fastapi import HTTPException
from backend.routers.task12_in_memory_storage import temp_storage

client = TestClient(app)

def testValidPayload():
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": "Valid resume text here.",
        "job_description": "Valid job description here."
    }
    response = client.post("/api/analyze", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert "fitScore" in response.json()
    assert "improvementSuggestions" in response.json()

def testMissingFields():
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": "Valid resume text here.",
    }
    response = client.post("/api/analyze", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Both resume_text and job_description are required."}

def testCharacterLimitExceeded():
    long_text = "a" * 10001  # 10,001 characters
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": long_text,
        "job_description": "Valid job description here."
    }
    response = client.post("/api/analyze", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Inputs exceed the maximum character limit of 10,000 characters each."}


@patch('backend.routers.analyze.analyzeText')  # Mock the analyzeText function
def testHuggingFaceApiError(mock_analyze):
    mock_analyze.side_effect = Exception("API error")
    response = client.post("/api/analyze", headers={"Authorization": "Bearer test_token"})
    print(response)
    assert response.status_code == 400
    assert "detail" in response.json()

def testInputFormat():
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": "Valid resume text here.",
        "job_description": "Valid job description here."
    }
    response = client.post("/api/analyze", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert isinstance(response.json()["fitScore"], int)
    assert isinstance(response.json()["improvementSuggestions"], list)

def testInvalidInputFormat():
    temp_storage.clear()
    temp_storage["test_token"] = {
        "resume_text": 123456789,  # Invalid format: not a string
        "job_description": "Valid job description here."
    }
    response = client.post("/api/analyze", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Both resume_text and job_description must be strings."}

def test_valid_response():
    # Given a valid API response
    analysisResult = {
        "fitscore": "85",
        "suggestions": [
            "Add skills related to project management.",
            "Improve your summary section to include specific achievements."
        ]
    }
    
    result = parseResponse(analysisResult)
    
    assert result.fitScore == 85
    assert result.improvementSuggestions == [
        "Add skills related to project management.",
        "Improve your summary section to include specific achievements."
    ]

def test_missing_fit_score():
    # Given an API response missing the fit_score
    analysisResult = {
        "suggestions": [
            "Add skills related to project management.",
            "Improve your summary section to include specific achievements."
        ]
    }
    
    # When the parseResponse function is called
    with pytest.raises(HTTPException):
        parseResponse(analysisResult)

def test_malformed_response():
    # Given a malformed API response (e.g., missing results)
    analysisResult = {}
    
    # When the parseResponse function is called
    with pytest.raises(HTTPException):
        parseResponse(analysisResult)

def test_invalid_fit_score_type():
    # Given an API response with an invalid fit_score type
    analysisResult = {
        "fitscore": "invalid",
        "suggestions": [
            "Add skills related to project management.",
            "Improve your summary section to include specific achievements."
        ]
    }
    
    # When the parseResponse function is called
    with pytest.raises(HTTPException):
        parseResponse(analysisResult)

def test_empty_feedback():
    # Given an API response with empty feedback
    analysisResult = {
        "fitscore": "85",
        "suggestions": []
    }
    
    # When the parseResponse function is called
    result = parseResponse(analysisResult)
    
    assert result.fitScore == 85
    assert result.improvementSuggestions == []