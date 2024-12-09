import os
import json
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Header
from backend.routers.task12_in_memory_storage import temp_storage
from backend.schemas import AnalyzeResponse

# Load Hugging Face API key
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGING_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"

router = APIRouter()

def analyzeText(resumeText: str, jobDescription: str):
    """
    Send a request to the Hugging Face NLP API for text analysis.
    :param resume_text: Extracted resume content
    :param job_description: Job description provided by the user
    :return: API response
    """
    client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

    input = [
        {
            "role": "user",
            "content": f"What is the fitscore from 0-100 and only improvement suggestions as bullets for the given resume based on the given job description: resume? Resume: {resumeText}, Job description: {jobDescription}. Keep it brief. Seperate the fitscore and suggestions into parsable json no json tags"
        }
    ]
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct", 
        messages=input, 
        max_tokens=500
    )

    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        raise ValueError("Error decoding response from hugging face")

def parseResponse(analysisResult: json):
    fitScore = analysisResult.get("fitscore")
    if fitScore is None:
        raise HTTPException(status_code=400, detail="Missing 'fitscore' in API response.")
    try:
        fitScore = int(fitScore)
    except Exception:
         raise HTTPException(status_code=400, detail="Invalid fitscore formatting")
    

    improvementSuggestions = analysisResult.get("suggestions")

    if not isinstance(improvementSuggestions, list):
        raise HTTPException(status_code=400, detail="'suggestions' must be a list.")
    
    if not all(isinstance(suggestion, str) for suggestion in improvementSuggestions):
        raise HTTPException(status_code=400, detail="All items in 'suggestions' must be strings.")

    return AnalyzeResponse(
        fitScore=fitScore,
        improvementSuggestions=improvementSuggestions
    )
    

@router.post("/analyze")
async def analyzeResumeAndJobDescription(authorization: str = Header(...)):
    """
    Analyze the resume and job description to generate a fit score and feedback.
    :param authorization: Authorization token from the client
    :param payload: User input from the frontend
    :return: Analysis results including fitScore, skillsMatched, and improvementSuggestions
    """
    sessionToken = authorization.split("Bearer ")[1]
    if sessionToken not in temp_storage:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    sessionData = temp_storage[sessionToken]
    resumeText = sessionData.get("resume_text")
    jobDescription = sessionData.get("job_description")

    # Validate  presence, type, and character limits
    if not resumeText or not jobDescription:
        raise HTTPException(status_code=400, detail="Both resume_text and job_description are required.")
    if not isinstance(resumeText, str) or not isinstance(jobDescription, str):
        raise HTTPException(status_code=400, detail="Both resume_text and job_description must be strings.")
    if len(resumeText) > 10000 or len(jobDescription) > 10000:
        raise HTTPException(status_code=400,detail="Inputs exceed the maximum character limit of 10,000 characters each.")

    try:
        # Call Hugging Face API and process the response
        analysisResult = analyzeText(resumeText, jobDescription)
    except Exception as e:
        print(f"Error during analysis: {str(e)}") 
        raise HTTPException(status_code=400, detail=f"Error processing analysis: {str(e)}")
    
    return parseResponse(analysisResult)
