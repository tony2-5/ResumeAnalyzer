from pydantic import BaseModel, EmailStr, Field
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserResponse(BaseModel):
    email: EmailStr
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    accessToken: str
    tokenType: str

class JobDescriptionInput(BaseModel):
    job_description: str = Field(..., max_length=5000)

class AnalyzeRequest(BaseModel):
    """
    Request payload structure for the /analyze endpoint.
    """
    resume_text: str = Field(..., max_length=10000)
    job_description: str = Field(..., max_length=10000)

class AnalyzeResponse(BaseModel):
    """
    Response structure for the /analyze endpoint.
    """
    fitScore: int = Field(..., ge=0, le=100)
    skillsMatched: List[str]
    improvementSuggestions: List[str]