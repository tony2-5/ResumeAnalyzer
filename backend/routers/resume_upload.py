import io
from fastapi import APIRouter, Header, UploadFile, HTTPException
from backend.routers.task11_text_extraction import extractTextFromPdf
from backend.routers.task12_in_memory_storage import temp_storage

router = APIRouter()

# Max file size for upload (2MB)
MAX_FILE_SIZE_MB = 2 * 1024 * 1024  

@router.post("/resume-upload", status_code=200)
async def resumeUpload(resume_file: UploadFile, session_token: str = Header(...)):
    # Validate file type and size
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    file_content = await resume_file.read()
    if len(file_content) > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File size exceeds the 2MB limit.")

    # Convert file content to a BytesIO object
    file_like_object = io.BytesIO(file_content)

    # Extract text from the PDF
    extracted_text = extractTextFromPdf(file_like_object)

    # Store the resume text in temporary storage
    if session_token not in temp_storage:
        temp_storage[session_token] = {}
    
    temp_storage[session_token]["resume_text"] = extracted_text

    return {"message": "Resume uploaded successfully.", "token": session_token}
