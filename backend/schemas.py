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
    job_description: str = Field(..., max_length=10000)

class FitScorePayload(BaseModel):
    resumeText: str = Field(..., max_length=10000, description="The text of the resume")
    jobDescription: str = Field(..., max_length=10000, description="The job description text")
