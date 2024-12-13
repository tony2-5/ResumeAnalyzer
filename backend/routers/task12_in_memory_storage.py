from fastapi import APIRouter, HTTPException, Header
import json

router = APIRouter()

# Temporary in-memory storage (this can be replaced by a file-based system)
temp_storage = {}

@router.get("/resume-data", status_code=200)
async def getResumeData(sessionToken: str = Header(...)):
    '''
    Get resume data from temp storage
    '''

    # Check if the session_token exists in temp_storage
    if sessionToken not in temp_storage:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    # Retrieve the data for the session
    session_data = temp_storage[sessionToken]

    return {
        "message": "Session data retrieved successfully.",
        "data": session_data 
    }

