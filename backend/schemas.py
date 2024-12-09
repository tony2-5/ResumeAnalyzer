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

class AnalyzeResponse(BaseModel):
    """
    Response structure for the /analyze endpoint.
    """
    fitScore: int = Field(..., ge=0, le=100)
    improvementSuggestions: List[str]
