import pytest
from backend.calculate_fit_score import calculate_fit_score  # Replace 'your_module_name' with your actual module name

@pytest.mark.parametrize(
    "resume, job_description, required, preferred, expected_score",
    [
        # Full match
        (
            "Python developer with experience in AWS and REST APIs",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            100,
        ),
        # Partial match
        (
            "Python developer with knowledge of AWS",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            70,
        ),
        # No match
        (
            "Graphic designer with skills in Photoshop",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            0,
        ),
        # Empty inputs
        (
            "",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            0,
        ),
        # Non-alphanumeric characters in the resume and job description
        (
            "Python developer, with REST API experience! 3 years working with AWS.",
            "Looking for a software engineer with Python, AWS, REST APIs, 5+ years experience.",
            None,
            None,
            46,  # Expected score (to be determined based on matching tokens)
        ),
        # Non-weighted keywords
        (
            "Python developer with REST API experience",
            "Looking for a software engineer with Python, AWS, REST APIs.",
            None,
            None,
            30,  # Proportional match
        ),
    ],
)
def test_calculate_fit_score(resume, job_description, required, preferred, expected_score):
    assert calculate_fit_score(resume, job_description, required, preferred) == expected_score
