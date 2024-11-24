# backend/api/task10_validation.py

from fastapi import APIRouter, UploadFile, HTTPException

router = APIRouter()  # 初始化 APIRouter

MAX_FILE_SIZE_MB = 2 * 1024 * 1024  # 2MB in bytes

@router.post("/resume-upload")
async def resume_upload(resume_file: UploadFile):
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    file_content = await resume_file.read()
    if len(file_content) > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File size exceeds the 2MB limit.")

    return {"message": "Resume uploaded successfully."}

@router.post("/store-resume")
async def store_resume(resume_file: UploadFile):
    # 验证文件类型
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    # 模拟生成 session_id
    session_id = "test-session-id"
    return {"session_id": session_id}
