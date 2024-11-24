from fastapi import APIRouter, UploadFile, Form, HTTPException
from uuid import uuid4

router = APIRouter()

# Temporary in-memory storage
temp_storage = {}

@router.post("/store-resume")
async def store_resume(resume_file: UploadFile):
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    # Generate session ID and mock resume text
    session_id = str(uuid4())
    temp_storage[session_id] = {
        "resume_text": "Extracted text from PDF.",
        "job_description": None,
    }
    return {"session_id": session_id, "message": "Resume stored successfully."}

@router.post("/store-job-description")
async def store_job_description(session_id: str = Form(...), job_description: str = Form(...)):
    if session_id not in temp_storage:
        raise HTTPException(status_code=404, detail="Session ID not found.")
    temp_storage[session_id]["job_description"] = job_description
    return {"message": "Job description stored successfully."}

@router.get("/session/{session_id}")
async def get_session_data(session_id: str):
    if session_id not in temp_storage:
        raise HTTPException(status_code=404, detail="Session ID not found.")
    return temp_storage[session_id]

@router.delete("/session/{session_id}")
async def delete_session_data(session_id: str):
    if session_id not in temp_storage:
        raise HTTPException(status_code=404, detail="Session ID not found.")
    del temp_storage[session_id]
    return {"message": "Session data deleted successfully."}
