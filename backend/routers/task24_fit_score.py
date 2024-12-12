from fastapi import APIRouter, HTTPException, Header
from backend.schemas import FitScorePayload
from backend.calculate_fit_score import calculateFitScore
from backend.generate_feedback import generateFeedback
from backend.routers.analyze import analyzeResumeAndJobDescription
from backend.routers.task12_in_memory_storage import temp_storage

router = APIRouter()

@router.post("/fit-score")
async def calculateFitScoreApi(payload: FitScorePayload, session_token: str = Header(...)):
    """
    Calculate the fit score and provide feedback based on the resume text and job description.
    """
    # Retrieves data from payload
    resumeText = payload.resumeText
    jobDescription = payload.jobDescription

    temp_storage[session_token] = {"resume_text": resumeText, "job_description": jobDescription}


    # Validate  presence, type, and character limits
    if not resumeText or not jobDescription:
        raise HTTPException(status_code=400, detail="Both resume_text and job_description are required.")
    if not isinstance(resumeText, str) or not isinstance(jobDescription, str):
        raise HTTPException(status_code=400, detail="Both resume_text and job_description must be strings.")
    if len(resumeText) > 10000 or len(jobDescription) > 10000:
        raise HTTPException(status_code=400, detail="Inputs exceed the maximum character limit of 10,000 characters each.")
    nlpResponse = await analyzeResumeAndJobDescription(session_token)
    fitScore = calculateFitScore(resumeText, jobDescription, nlpResponse)
    feedback = generateFeedback(resumeText, jobDescription, nlpResponse)

    print(f"fitscore\t {fitScore}")
    print(f"feedback\t {feedback}")
    return {"fitScore": fitScore["fitScore"], "matchedKeywords": fitScore["matchedKeywords"], "missingKeywords": feedback["missingKeywords"], "feedback": feedback['feedback']}
