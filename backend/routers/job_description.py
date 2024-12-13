from fastapi import APIRouter, HTTPException, Header
from backend.schemas import JobDescriptionInput
from backend.routers.task12_in_memory_storage import temp_storage

router = APIRouter()

@router.post("/job-description", status_code=200)
async def uploadJobDescription(request: JobDescriptionInput, sessionToken: str = Header(...)):
    # Validate job description
    if not request.job_description:
        raise HTTPException(status_code=400, detail="Job description is required.")
    if len(request.job_description) > 10000:
        raise HTTPException(status_code=400, detail="Job description exceeds character limit.")
    
    # Check if resume is uploaded first
    if sessionToken not in temp_storage or "resume_text" not in temp_storage[sessionToken]:
        raise HTTPException(status_code=400, detail="Upload resume first.")
    # Store the job description
    temp_storage[sessionToken]["job_description"] = request.job_description.replace("\n", " ").strip()

    return {"job_description": request.job_description, "token": sessionToken}
