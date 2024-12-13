import os
import json
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from backend.routers.task12_in_memory_storage import temp_storage

# Load Hugging Face API key
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGING_API_KEY')

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
            "content": 'Your response must be in this exact example format and follow json standards in english: {"fitscore": 0-100, jobDescriptionSkills:{ preferred: [], required: []},"suggestions": []} for the given resume and based on the given job description. Suggestions should be about a sentence long each. Get all the job description skills and should be 1-2 words. No additional comments. Be on the lookout for bad job descriptions.  Resume: '+resumeText+', Job description: '+jobDescription
        }
    ]
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct", 
        messages=input, 
        max_tokens=800
    )
    print(response.choices[0].message.content)
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        return handleBadJson(response.choices[0].message.content)
    
def handleBadJson(badJson):
    client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

    input = [
        {
            "role": "user",
            "content": "Return only this json in the correct form no additional tags: "+badJson
        }
    ]
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct", 
        messages=input, 
        max_tokens=800
    )
    print(response.choices[0].message.content)
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        raise ValueError("Error decoding response from hugging face")


def parseResponse(analysisResult: dict):
    """
    Parses the analysis result to extract the fit score, qualifications, and suggestions.
    :param analysisResult: The response JSON from the analysis API
    :return: A dictionary containing fitScore, qualifications, and suggestions
    """
    # Validate and extract "fitscore"
    fitScore = analysisResult.get("fitscore")
    if fitScore is None:
        raise HTTPException(status_code=400, detail="Missing 'fitscore' in API response.")
    try:
        fitScore = int(fitScore)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid 'fitscore' formatting. Must be an integer.")


    # Validate "job_description"
    jobDescription = analysisResult.get("jobDescriptionSkills")
    if not isinstance(jobDescription, dict):
        raise HTTPException(status_code=400, detail="jobDescriptionSkills must be a dictionary.")

    preferredQualifications = jobDescription.get("preferred")
    if not isinstance(preferredQualifications, list):
        raise HTTPException(status_code=400, detail="'jobDescriptionSkills.preferred' must be a list.")
    if not all(isinstance(item, str) for item in preferredQualifications):
        raise HTTPException(status_code=400, detail="All items in 'jobDescriptionSkills.preferred' must be strings.")

    requiredQualifications = jobDescription.get("required")
    if not isinstance(requiredQualifications, list):
        raise HTTPException(status_code=400, detail="'jobDescriptionSkills.required' must be a list.")
    if not all(isinstance(item, str) for item in requiredQualifications):
        raise HTTPException(status_code=400, detail="All items in 'jobDescriptionSkills.required' must be strings.")

    # Validate and extract "suggestions"
    improvementSuggestions = analysisResult.get("suggestions")
    if not isinstance(improvementSuggestions, list):
        raise HTTPException(status_code=400, detail="'suggestions' must be a list.")
    if not all(isinstance(suggestion, str) for suggestion in improvementSuggestions):
        raise HTTPException(status_code=400, detail="All items in 'suggestions' must be strings.")

    return {
        "fitScore": fitScore,
        "jobDescriptionSkills": {
            "preferred": preferredQualifications,
            "required": requiredQualifications,
        },
        "suggestions": improvementSuggestions,
    }

    

@router.post("/analyze")
async def analyzeResumeAndJobDescription(sessionToken: str):
    """
    Analyze the resume and job description to generate a fit score and feedback.
    :param authorization: Authorization token from the client
    :param payload: User input from the frontend
    :return: Analysis results including fitScore, skillsMatched, and improvementSuggestions
    """
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
        raise HTTPException(
            status_code=400,
            detail="Inputs exceed the maximum character limit of 10,000 characters each."
        )

    try:
        # Call Hugging Face API and process the response
        analysisResult = analyzeText(resumeText, jobDescription)
    except Exception as e:
        print(f"Error during analysis: {str(e)}") 
        raise HTTPException(status_code=400, detail=f"Error processing analysis: {str(e)}")
    
    return parseResponse(analysisResult)
