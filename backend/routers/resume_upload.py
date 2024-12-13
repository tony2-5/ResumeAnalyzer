import io
from fastapi import APIRouter, Header, UploadFile, HTTPException
from backend.routers.task11_text_extraction import extractTextFromPdf
from backend.routers.task12_in_memory_storage import temp_storage

router = APIRouter()

# Max file size for upload (2MB)
MAX_FILE_SIZE_MB = 2 * 1024 * 1024  

@router.post("/resume-upload", status_code=200)
async def resumeUpload(resumeFile: UploadFile, sessionToken: str = Header(...)):
    '''
    Upload resume to backend temp storage
    '''
    # Validate file type and size
    if resumeFile.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    fileContent = await resumeFile.read()
    if len(fileContent) > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File size exceeds the 2MB limit.")

    # Convert file content to a BytesIO object
    fileLikeObject = io.BytesIO(fileContent)

    # Extract text from the PDF
    extractedText = extractTextFromPdf(fileLikeObject)

    # Store the resume text in temporary storage
    if sessionToken not in temp_storage:
        temp_storage[sessionToken] = {}
    
    temp_storage[sessionToken]["resume_text"] = extractedText

    return {"message": "Resume uploaded successfully.", "token": sessionToken}
