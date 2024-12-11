from fastapi import APIRouter, HTTPException, Header
import json

router = APIRouter()

# Temporary in-memory storage (this can be replaced by a file-based system)
temp_storage = {}

@router.get("/resume-data", status_code=200)
async def get_resume_data(session_token: str = Header(...)):
    print(f"Received session token: {session_token}")  # Log the received session token

    # Check if the session_token exists in temp_storage
    if session_token not in temp_storage:
        print(f"Session token {session_token} not found in storage.")  # Log if session is not found
        raise HTTPException(status_code=404, detail="Session not found.")
    
    # Retrieve the data for the session
    session_data = temp_storage[session_token]
    print(f"Retrieved session data: {session_data}")  # Log the retrieved session data

    return {
        "message": "Session data retrieved successfully.",
        "data": session_data 
    }

# For storing session data in a JSON file
def save_session_data():
    with open("backend/session_data.json", "w") as file:
        json.dump(temp_storage, file)
