import pytest
from backend.generate_feedback import generateFeedback

@pytest.mark.parametrize(
    "resume, jobDescription, required, preferred, feedback",
    [
        # Full match
        (
            "Python developer with experience in AWS and REST APIs",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            {"missingKeywords": [],
             "suggestions": []},
        ),
        # Partial match
        (
            "Python developer with knowledge of AWS",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            {"missingKeywords": ["apis", "rest"],
             "suggestions": [
                 "Consider including 'apis' in your resume to align with the job description.",
                 "Consider including 'rest' in your resume to align with the job description."
             ]},
        ),
        # No match
        (
            "Graphic designer with skills in Photoshop",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            {"missingKeywords": ["apis", "aws", "python", "rest"],
             "suggestions": [
                 "Consider including 'apis' in your resume to align with the job description.",
                 "Consider including 'aws' in your resume to align with the job description.",
                 "Consider including 'python' in your resume to align with the job description.",
                 "Consider including 'rest' in your resume to align with the job description."
             ]},
        ),
        # Empty inputs
        (
            "",
            "Looking for a software engineer with experience in Python, AWS, and REST APIs.",
            ["python", "aws"],
            ["rest", "apis"],
            {"missingKeywords": [],
             "suggestions": []},
        ),
        # Non-alphanumeric characters in the resume and job description
        (
            "Python developer, with REST API experience! 3 years working with AWS.",
            "Looking for a software engineer with Python, AWS, REST APIs, 5+ years experience.",
            None,
            None,
            {"missingKeywords": ["5", "apis"],
             "suggestions": [
                 "Highlight achievements or experience related to 5 years.",
                 "Consider including 'apis' in your resume to align with the job description."
             ]},
        ),
        # Non-weighted keywords
        (
            "Python developer with REST API experience",
            "Looking for a software engineer with C++, AWS, REST APIs.",
            None,
            None,
            {"missingKeywords": ["apis", "aws", "c++"],
             "suggestions": [
                 "Consider including 'apis' in your resume to align with the job description.",
                 "Consider including 'aws' in your resume to align with the job description.",
                 "Add details that demonstrate your expertise in 'c++'."
             ]},
        ),
    ],
)
def testGenerateFeedback(resume, jobDescription, required, preferred, feedback):
    assert generateFeedback(resume, jobDescription, required, preferred) == feedback
