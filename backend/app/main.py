# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.resume import router as resume_router 
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

# Include the resume router
app.include_router(resume_router, prefix="/api")
# Include the authentication routes
app.include_router(auth_router, prefix="/api/auth")
