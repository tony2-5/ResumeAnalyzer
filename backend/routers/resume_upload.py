# backend/app/routes/resume.py
import io
from fastapi import APIRouter, Header, UploadFile, HTTPException
from backend.routers.task11_text_extraction import extractTextFromPdf
from backend.routers.task12_in_memory_storage import temp_storage
router = APIRouter()

# Endpoint for uploading resume
MAX_FILE_SIZE_MB = 2 * 1024 * 1024  # 2MB in bytes

@router.post("/resume-upload",status_code=200)
async def resumeUpload(resume_file: UploadFile, session_token: str = Header(...)):
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    file_content = await resume_file.read()
    if len(file_content) > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File size exceeds the 2MB limit.")

    file_like_object = io.BytesIO(file_content)

    extracted_text = extractTextFromPdf(file_like_object)

    temp_storage[session_token] = {
        "resume_text": extracted_text,
    }

    return {"message": "Resume uploaded successfully.",
            "token": session_token
            }

