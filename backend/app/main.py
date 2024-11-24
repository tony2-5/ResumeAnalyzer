# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.resume_upload import router as resume_upload_router
from app.routes.job_description import router as job_description_router
from app.routes.auth import router as auth_router

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the resume upload router
app.include_router(resume_upload_router, prefix="/api")
# Include the job description upload router
app.include_router(job_description_router, prefix="/api")
# Include the authentication routes
app.include_router(auth_router, prefix="/api/auth")
