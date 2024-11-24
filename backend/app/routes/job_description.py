# backend/app/routes/job_description.py
from fastapi import APIRouter, Form, HTTPException

router = APIRouter()

@router.post("/upload-job-description/")
async def upload_job_description(job_desc: str = Form(...)):
    if not job_desc:
        raise HTTPException(status_code=400, detail="Job description is required.")
    
    return {"job_description": job_desc}
