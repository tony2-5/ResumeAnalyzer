import pytest
from backend.calculate_fit_score import calculateFitScore
from unittest.mock import patch

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "resumeText, jobDescription, expectedFitScore",
    [
        # Full match
        (
            "Python software engineer with experience in AWS and REST APIs",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            77,
        ),
        # Large match
        (
            "Python developer with experience in AWS and REST APIs",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            61,
        ),
        # Partial match
        (
            "Python developer with knowledge of AWS",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            23,
        ),
        # No match
        (
            "Graphic designer with skills in Photoshop",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            15,
        ),
        # Non-alphanumeric characters in resume and job description
        (
            "Python developer, with REST API experience! 3 years working with AWS.",
            "Looking for a software engineer with Python, AWS, REST APIs, 5+ years experience.",
            46,
        ),
        # Non-weighted keywords in the job description
        (
            "Python developer with REST API experience",
            "Looking for a software engineer with C++, AWS, REST APIs.",
            20,
        ),
    ],
)

@patch("backend.routers.task24_fit_score.calculateFitScore")
def testCalculateFitScore(
    mockGenerateFeedback,
    resumeText,
    jobDescription,
    expectedFitScore
):
    # Set up mocks
    mockGenerateFeedback.return_value = {
        "fitScore": expectedFitScore
    }

    # Call the function under test
    response = calculateFitScore(
        resumeText=resumeText, 
        jobDescription=jobDescription, 
        nlpResponse={
            "fitScore": expectedFitScore,
            "jobDescriptionSkills": {
                "required": [],
                "preferred": []
            },
            "suggestions": []
        }
    )

    # Assert the response
    assert response["fitScore"] == expectedFitScore
