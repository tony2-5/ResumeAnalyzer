# backend/routers/get_user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from schemas import UserResponse
from auth import getCurrentUser
from database import database
from models import users

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
async def readCurrentUser(currentUser: dict = Depends(getCurrentUser)):
    """
    Retrieves the current logged-in user's information.

    Args:
        currentUser (dict): User information from the token.

    Returns:
        UserResponse: User's email and username.
    """
    query = select(users).where(users.c.email == currentUser['email'])
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="Cannot find user.")
    
    return UserResponse(email=user['email'], username=user['username'])
