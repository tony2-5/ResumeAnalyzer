from fastapi import APIRouter, HTTPException
from sqlalchemy import delete, select
from backend.database import database
from backend.models import users

router = APIRouter()

@router.delete("/delete_user")
async def delete_user(email: str):
    """
    Deletes a user by email.

    Args:
        email (str): The email of the user to delete.

    Returns:
        dict: Success or error message.
    """
    # Query to check if the user exists
    query = select(users).where(users.c.email == email)
    user = await database.fetch_one(query)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Delete the user from the database
    delete_query = delete(users).where(users.c.email == email)
    await database.execute(delete_query)

    return {"message": f"User with email {email} deleted successfully."}