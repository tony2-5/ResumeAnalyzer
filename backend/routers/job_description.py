# backend/app/routes/job_description.py
from fastapi import APIRouter, HTTPException, Header
from backend.schemas import JobDescriptionInput
from backend.routers.task12_in_memory_storage import temp_storage

router = APIRouter()

@router.post("/job-description", status_code=200)
async def uploadJobDescription(request: JobDescriptionInput, session_token: str = Header(...)):
    if not request.job_description:
        raise HTTPException(status_code=400, detail="Job description is required.")
    if len(request.job_description) > 5000:
        raise HTTPException(status_code=400, detail="Job description exceeds character limit.")
    if session_token not in temp_storage:
        raise HTTPException(status_code=400, detail="Upload resume first.")
    temp_storage[session_token]["job_description"] = request.job_description
    
    return {"job_description": request.job_description,
            "token": session_token
            }
