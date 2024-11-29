from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# Define the input data structure
class FitScorePayload(BaseModel):
    resume_text: str = Field(..., max_length=10000, description="The text of the resume")
    job_description: str = Field(..., max_length=10000, description="The job description text")

# Define route
@router.post("/api/fit-score")
async def calculate_fit_score(payload: FitScorePayload):
    """
    Calculate the fit score and provide feedback based on the resume text and job description.
    """
    # Retrieves data from payload
    resume_text = payload.resume_text
    job_description = payload.job_description

    # If the field is empty, an error is returned
    if not resume_text or not job_description:
        raise HTTPException(status_code=400, detail="Both resume_text and job_description are required.")

    # Logic for calculating match scores (placeholder logic)
    fit_score = calculate_score(resume_text, job_description)
    feedback = generate_feedback(resume_text, job_description)

    return {"fit_score": fit_score, "feedback": feedback}


def calculate_score(resume_text: str, job_description: str) -> int:
    """
    Calculate how your resume matches the job description
    """
    from collections import Counter
    import re

    def tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())

    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)

    resume_counter = Counter(resume_tokens)
    job_counter = Counter(job_tokens)

    matches = sum((resume_counter & job_counter).values())
    total_keywords = len(job_tokens)

    return int((matches / total_keywords) * 100) if total_keywords > 0 else 0


def generate_feedback(resume_text: str, job_description: str) -> list:
    """
    Generate feedback to improve your resume.
    """
    from collections import Counter
    import re

    def tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())

    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)

    resume_counter = Counter(resume_tokens)
    job_counter = Counter(job_tokens)

    missing_keywords = [word for word in job_counter if word not in resume_counter]

    feedback = [f"Consider adding the skill '{word}' to your resume." for word in missing_keywords]
    return feedback[:5]
