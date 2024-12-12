import pytest
from unittest.mock import AsyncMock, patch
from backend.generate_feedback import generateFeedback

@pytest.fixture
def mock_generateFeedback():
    """Mock the generateFeedback function."""
    return AsyncMock(return_value={"missingKeywords": ["Python, AWS"], "feedback": ["Learn REST APIs"]})

@pytest.mark.parametrize(
    "resume_text, job_description, expected_missing_keywords, expected_suggestions",
    [
        # Full match
        (
            "Python software engineer with experience in AWS and REST APIs",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            [],
            [],
        ),
        # Large match
        (
            "Python developer with experience in AWS and REST APIs",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ['engineer', 'software'],
            [
                {'category': 'experience', 'text': "Consider including 'engineer' in your resume to align with the job description."},
                {'category': 'experience', 'text': "Consider including 'software' in your resume to align with the job description."}
            ],
        ),
        # Partial match
        (
            "Python developer with knowledge of AWS",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ['apis', 'engineer', 'experience', 'rest', 'software'],
            [
                {'category': 'experience', 'text': "Consider including 'apis' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'engineer' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'experience' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'rest' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'software' in your resume to align with the job description."}
            ],
        ),
        # No match
        (
            "Graphic designer with skills in Photoshop",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ['apis', 'aws', 'engineer', 'experience', 'python', 'rest', 'software'],
            [
                {'category': 'experience', 'text': "Consider including 'apis' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'aws' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'engineer' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'experience' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'python' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'rest' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'software' in your resume to align with the job description."}
            ],
        ),
        # Non-alphanumeric characters in resume and job description
        (
            "Python developer, with REST API experience! 3 years working with AWS.",
            "Looking for a software engineer with Python, AWS, REST APIs, 5+ years experience.",
            ['5+', 'apis', 'engineer', 'software'],
            [
                {'category': 'skills', 'text': "Add details that demonstrate your expertise in '5+'."}, 
                {'category': 'experience', 'text': "Consider including 'apis' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'engineer' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'software' in your resume to align with the job description."}
            ],
        ),
        # Non-weighted keywords in the job description
        (
            "Python developer with REST API experience",
            "Looking for a software engineer with C++, AWS, REST APIs.",
            ['apis', 'aws', 'c++', 'engineer', 'software'],
            [
                {'category': 'experience', 'text': "Consider including 'apis' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'aws' in your resume to align with the job description."}, 
                {'category': 'skills', 'text': "Add details that demonstrate your expertise in 'c++'."}, 
                {'category': 'experience', 'text': "Consider including 'engineer' in your resume to align with the job description."}, 
                {'category': 'experience', 'text': "Consider including 'software' in your resume to align with the job description."}
            ],
        ),
    ],
)

@patch("backend.routers.task24_fit_score.generateFeedback")
def test_generate_feedback(
    mock_generate_feedback,
    resume_text,
    job_description,
    expected_missing_keywords,
    expected_suggestions
):
    # Set up mocks
    mock_generate_feedback.return_value = {
        "missingKeywords": expected_missing_keywords,
        "feedback": expected_suggestions
    }

    # Call the function under test
    response = generateFeedback(
        resumeText=resume_text, 
        jobDescription=job_description, 
        nlpResponse={
            "jobDescriptionSkills": {
                "required": [],
                "preferred": []
            },
            "suggestions": []
        }
    )

    # Assert the response
    print(response)
    print(expected_missing_keywords)
    print(expected_suggestions)
    assert response["missingKeywords"] == expected_missing_keywords
    assert response["feedback"]["suggestions"] == expected_suggestions