# backend/app/routes/resume.py
from fastapi import APIRouter, UploadFile, Form, HTTPException

router = APIRouter()

# Endpoint for uploading resume
@router.post("/resume/upload")
async def upload_resume(file: UploadFile):
    # Validate file type
    if file.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF or Word document.")

    try:
        # Read the file (e.g., store or process it)
        content = await file.read()
        # Here you could process the resume content, e.g., extracting text from PDF
        return {"filename": file.filename, "message": "Resume uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Endpoint for uploading job description
@router.post("/job-description/upload")
async def upload_job_description(job_desc: str = Form(...)):
    if not job_desc:
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    # Here, you can process the job description (e.g., save to database or pass for analysis)
    return {"message": "Job description uploaded successfully", "job_desc": job_desc}
