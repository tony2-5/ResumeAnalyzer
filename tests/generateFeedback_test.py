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
    "payload, session_token, expected_missing_keywords, expected_suggestions",
    [
        # Full match
        (
            FitScorePayload(
                resumeText="Python software engineer with experience in AWS and REST APIs",
                jobDescription="Looking for a software engineer with experience in Python, AWS, and REST APIs."
            ),
            "fullmatch",
            [],
            [
                {'category': 'education', 'text': 'Ensure to highlight relevant projects that demonstrate expertise in Python, AWS, and REST APIs in the interview.'}
            ],
        ),
        # Large match
        (
            FitScorePayload(
                resumeText="Python developer with experience in AWS and REST APIs",
                jobDescription="Looking for a software engineer with experience in Python, AWS, and REST APIs."
            ),
            "largematch",
            ['engineer', 'software'],
            [
                {'category': 'experience', 'text': "Consider including 'engineer' in your resume to align with the job description."},
                {'category': 'experience', 'text': "Consider including 'software' in your resume to align with the job description."}
            ],
        ),
        # Partial match
        (
            FitScorePayload(
                resumeText="Python developer with knowledge of AWS",
                jobDescription="Looking for a software engineer with experience in Python, AWS, and REST APIs."
            ),
            "partialmatch",
            ['rest'],
            [
                {'category': 'experience', 'text': 'Consider highlighting experience with REST APIs to increase fit score'},
                {'category': 'experience', 'text': 'Emphasize software engineering background to better match job description'}
            ],
        ),
        # No match
        (
            FitScorePayload(
                resumeText="Graphic designer with skills in Photoshop",
                jobDescription="Looking for a software engineer with experience in Python, AWS, and REST APIs."
            ),
            "nomatch",
            ['apis', 'aws', 'engineer', 'experience', 'python', 'rest', 'software'],
            [
                {'category': 'experience', 'text': "Consider including 'apis' in your resume to align with the job description."},
                {'category': 'experience', 'text': "Consider including 'aws' in your resume to align with the job description."},
                {'category': 'experience', 'text': "Consider including 'experience' in your resume to align with the job description."},
                {'category': 'experience', 'text': "Consider including 'rest' in your resume to align with the job description."},
                {'category': 'education', 'text': 'Consider taking courses in software engineering to transition into the field.'},
                {'category': 'skills', 'text': 'Develop skills in Python programming language to enhance your job prospects.'}
            ],
        ),
        # Non-alphanumeric characters in resume and job description
        (
            FitScorePayload(
                resumeText="Python developer, with REST API experience! 3 years working with AWS.",
                jobDescription="Looking for a software engineer with Python, AWS, REST APIs, 5+ years experience."
            ),
            "nonalpha",
            ['5+', 'apis', 'engineer', 'software'],
            [
                {'category': 'experience', 'text': "Consider including 'apis' in your resume to align with the job description."},
                {'category': 'experience', 'text': 'Gain 2 more years of experience to meet the 5+ year requirement'},
                {'category': 'achievements', 'text': 'Highlight specific software engineering skills to increase fit score'}
            ],
        ),
        # Non-weighted keywords in the job description
        (
            FitScorePayload(
                resumeText="Python developer with REST API experience",
                jobDescription="Looking for a software engineer with C++, AWS, REST APIs."
            ),
            "nonweighted",
            ['apis', 'aws', 'c++', 'engineer', 'software'],
            [
                {'category': 'experience', 'text': "Consider including 'apis' in your resume to align with the job description."},
                {'category': 'experience', 'text': "Consider including 'engineer' in your resume to align with the job description."},
                {'category': 'experience', 'text': "Consider including 'software' in your resume to align with the job description."},
                {'category': 'skills', 'text': 'Consider learning C++ to enhance your skill set and become a more competitive candidate.'},
                {'category': 'experience', 'text': 'Gain experience with AWS to improve your cloud computing skills and increase your chances of getting hired.'}
            ],
        ),
    ],
)
async def testGenerateFeedback(payload, session_token, expected_missing_keywords, expected_suggestions):
    print(payload.resumeText)
    print(payload.jobDescription)
    result = await calculateFitScoreApi(payload, session_token)
    print(result)
    assert result["missingKeywords"] == expected_missing_keywords
    assert result["feedback"]["suggestions"] == expected_suggestions
