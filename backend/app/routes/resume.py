# backend/app/routes/resume.py
from fastapi import APIRouter, UploadFile, Form, HTTPException

router = APIRouter()

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile, job_desc: str = Form(...)):
    # Validate file type
    if file.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file format.")

    try:
        # Read file content (for now we just process the file as needed)
        content = await file.read()
        # This is where file processing would happen (e.g., extracting text from PDF)
        return {"filename": file.filename, "job_desc": job_desc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
