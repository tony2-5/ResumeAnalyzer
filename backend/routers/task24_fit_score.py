from fastapi import APIRouter, HTTPException
from backend.schemas import FitScorePayload
from backend.calculate_fit_score import calculateFitScore
from backend.generate_feedback import generateFeedback

router = APIRouter()

@router.post("/fit-score")
async def calculateFitScoreApi(payload: FitScorePayload):
    """
    Calculate the fit score and provide feedback based on the resume text and job description.
    """
    # Retrieves data from payload
    resumeText = payload.resumeText
    jobDescription = payload.jobDescription

    # Validate  presence, type, and character limits
    if not resumeText or not jobDescription:
        raise HTTPException(status_code=400, detail="Both resume_text and job_description are required.")
    if not isinstance(resumeText, str) or not isinstance(jobDescription, str):
        raise HTTPException(status_code=400, detail="Both resume_text and job_description must be strings.")
    if len(resumeText) > 10000 or len(jobDescription) > 10000:
        raise HTTPException(status_code=400, detail="Inputs exceed the maximum character limit of 10,000 characters each.")

    fitScore = calculateFitScore(resumeText, jobDescription)
    feedback = generateFeedback(resumeText, jobDescription)

    return {"fitScore": fitScore, "feedback": feedback['suggestions']}
