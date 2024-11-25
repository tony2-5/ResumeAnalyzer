from fastapi import APIRouter, HTTPException, Header

router = APIRouter()

# Temporary in-memory storage
temp_storage = {

}

@router.get("/resume-data", status_code=200)
async def get_resume_data(session_token: str = Header(...)):
    # Check if the session_token exists in temp_storage
    if session_token not in temp_storage:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    # Retrieve the data for the session
    session_data = temp_storage[session_token]
    
    return {
        "message": "Session data retrieved successfully.",
        "data": session_data 
    }