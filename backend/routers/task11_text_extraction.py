from fastapi import APIRouter, UploadFile, HTTPException, File
from pypdf import PdfReader
import io

router = APIRouter()

def extract_text_from_pdf(file: io.BytesIO) -> str:
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.replace("\n", " ").strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")

@router.post("/store-resume")
async def store_resume(resume_file: UploadFile = File(...)):
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    try:
        file_content = await resume_file.read()
        extracted_text = extract_text_from_pdf(io.BytesIO(file_content))
        return {"message": "Text extracted successfully.", "extracted_text": extracted_text}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
