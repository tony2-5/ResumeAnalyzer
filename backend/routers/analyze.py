import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Header, Body
from backend.routers.task12_in_memory_storage import temp_storage

# Load Hugging Face API key
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGING_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

router = APIRouter()

def analyze_text(resume_text: str, job_description: str):
    """
    Send a request to the Hugging Face NLP API for text analysis.
    :param resume_text: Extracted resume content
    :param job_description: Job description provided by the user
    :return: API response
    """
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    question = f"What skills are required for this position: {job_description}?"
    context = resume_text

    data = {
        "inputs": {
            "question": question,
            "context": context
        }
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Hugging Face error: {response.text}"
        )
    return response.json()

@router.post("/analyze")
async def analyze_resume_and_job_description(
    authorization: str = Header(...),
    payload: dict = Body(...)
):
    """
    Analyze the resume and job description to generate a fit score and feedback.
    :param authorization: Authorization token from the client
    :param payload: User input from the frontend
    :return: Analysis results including fitScore, skillsMatched, and improvementSuggestions
    """
    session_token = authorization.split("Bearer ")[1]
    if session_token not in temp_storage:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    session_data = temp_storage[session_token]
    resume_text = session_data.get("resume_text")
    job_description = session_data.get("job_description")

    # Validate presence and character limits
    if not resume_text or not job_description:
        raise HTTPException(status_code=400, detail="Both resume_text and job_description are required.")
    if len(resume_text) > 10000 or len(job_description) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Inputs exceed the maximum character limit of 10,000 characters each."
        )

    try:
        # Call Hugging Face API and process the response
        analysis_result = analyze_text(resume_text, job_description)

        fit_score = int(analysis_result.get("score", 0) * 100)  # Convert to percentage
        skills_matched = analysis_result.get("answer", "").split(", ")  # Split skills into a list
        improvement_suggestions = [
            "Add specific achievements to your resume.",
            "Highlight leadership experience in previous roles.",
            "Include additional technical skills related to the job description."
        ]  # Placeholder suggestions

        return {
            "fitScore": fit_score,
            "skillsMatched": skills_matched,
            "improvementSuggestions": improvement_suggestions
        }
    except Exception as e:
        print(f"Error during analysis: {str(e)}")  # Log for debugging
        raise HTTPException(status_code=500, detail=f"Error processing analysis: {str(e)}")
