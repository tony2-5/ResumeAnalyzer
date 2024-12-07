import pytest
from backend.generate_feedback import generate_feedback  # Replace 'your_module_name' with your actual module name

@pytest.mark.parametrize(
    "resume, job_description, required, preferred, missing_keywords",
    [
        # Full match
        (
            "Python developer with experience in AWS and REST APIs",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            {"missing_keywords": []},
        ),
        # Partial match
        (
            "Python developer with knowledge of AWS",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            {"missing_keywords": ["apis", "rest"]},
        ),
        # No match
        (
            "Graphic designer with skills in Photoshop",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            {"missing_keywords": ["apis", "aws", "python", "rest"]},
        ),
        # Empty inputs
        (
            "",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            {"missing_keywords": []},
        ),
        # Non-alphanumeric characters in the resume and job description
        (
            "Python developer, with REST API experience! 3 years working with AWS.",
            "Looking for a software engineer with Python, AWS, REST APIs, 5+ years experience.",
            None,
            None,
            {"missing_keywords": []},
        ),
        # Non-weighted keywords
        (
            "Python developer with REST API experience",
            "Looking for a software engineer with Python, AWS, REST APIs.",
            None,
            None,
            {"missing_keywords": []},
        ),
    ],
)
def test_generate_feedback(resume, job_description, required, preferred, missing_keywords):
    assert generate_feedback(resume, job_description, required, preferred) == missing_keywords
