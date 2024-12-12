import pytest
from backend.routers.task24_fit_score import calculateFitScoreApi
from backend.schemas import FitScorePayload
from backend.routers.task12_in_memory_storage import temp_storage

# Fixture to initialize temp_storage for each test
@pytest.fixture(autouse=True)
def initTempStorage():
    temp_storage.clear()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, session_token, expected_fit_score",
    [
        # Full match
        (
            FitScorePayload(
                resumeText="Python software engineer with experience in AWS and REST APIs",
                jobDescription="Looking for a software engineer with experience in Python, AWS, and REST APIs."
            ),
            "fullmatch",
            88,
        ),
        # Large match
        (
            FitScorePayload(
                resumeText="Python developer with experience in AWS and REST APIs",
                jobDescription="Looking for a software engineer with experience in Python, AWS, and REST APIs."
            ),
            "largematch",
            81,
        ),
        # Partial match
        (
            FitScorePayload(
                resumeText="Python developer with knowledge of AWS",
                jobDescription="Looking for a software engineer with experience in Python, AWS, and REST APIs."
            ),
            "partialmatch",
            40,
        ),
        # No match
        (
            FitScorePayload(
                resumeText="Graphic designer with skills in Photoshop",
                jobDescription="Looking for a software engineer with experience in Python, AWS, and REST APIs."
            ),
            "nomatch",
            8,
        ),
        # Non-alphanumeric characters in resume and job description
        (
            FitScorePayload(
                resumeText="Python developer, with REST API experience! 3 years working with AWS.",
                jobDescription="Looking for a software engineer with Python, AWS, REST APIs, 5+ years experience."
            ),
            "nonalpha",
            53,
        ),
        # Non-weighted keywords in the job description
        (
            FitScorePayload(
                resumeText="Python developer with REST API experience",
                jobDescription="Looking for a software engineer with C++, AWS, REST APIs."
            ),
            "nonweighted",
            30,
        ),
    ],
)
async def testCalculateFitScore(payload, session_token, expected_fit_score):
    print(payload.resumeText)
    print(payload.jobDescription)
    result = await calculateFitScoreApi(payload, session_token)
    print(result)
    assert result["fitScore"] == expected_fit_score
