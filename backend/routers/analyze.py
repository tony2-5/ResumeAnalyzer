import json
from fastapi import APIRouter, HTTPException, Header
import requests
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGING_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

router = APIRouter()

# Helper function to call Hugging Face API
def analyze_text(resume_text, job_description):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Creating a question for the model
    question = f"What skills are required for this position: {job_description}?"
    
    # The resume text will be used as the context for the question-answering model
    data = {
        "inputs": {
            "question": question,
            "context": resume_text
        }
    }

    print("Sending data to Hugging Face:", data)  # Log the data being sent to Hugging Face API
    response = requests.post(API_URL, headers=headers, json=data)
    print("Received response from Hugging Face:", response.status_code, response.text)  # Log the Hugging Face API response

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Hugging Face error: {response.text}")
    return response.json()

@router.post("/analyze")
async def analyze_resume_and_job_description(authorization: str = Header(...)):
    # Fetch the access token from the Authorization header
    access_token = authorization.split("Bearer ")[1]
    print(f"Access Token extracted: {access_token}")  # Log the extracted access token

    try:
        print("Fetching resume data from backend...")
        resume_data_response = requests.get(f"http://127.0.0.1:8000/api/resume-data", headers={"Authorization": f"Bearer {access_token}"})

        print(f"Received resume data response with status code: {resume_data_response.status_code}")  # Log the response status

        if resume_data_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve resume data.")
        
        resume_data = resume_data_response.json()
        print("Resume data fetched:", resume_data)  # Log the fetched resume data

        resume_text = resume_data.get("resume_text")
        job_description = resume_data.get("job_description")

        if not resume_text or not job_description:
            raise HTTPException(status_code=400, detail="Missing resume text or job description.")

        # Call Hugging Face API for analysis
        print("Calling Hugging Face API for analysis...")
        analysis_result = analyze_text(resume_text, job_description)

        # Log the analysis result
        print("Analysis result:", analysis_result)

        # Save the result to a JSON file
        with open("backend/data.json", "w") as json_file:
            json.dump(analysis_result, json_file)

        return {"message": "Analysis completed successfully."}

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail="Unable to process the request. Please try again later.")
