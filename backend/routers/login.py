# backend/routers/login.py

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from models import users
from schemas import UserLogin, Token
from database import database
from auth import verifyPassword, createAccessToken, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=Token)
async def loginUser(user: UserLogin):
    """
    Authenticates a user and returns a JWT token.

    Args:
        user (UserLogin): Login credentials.

    Returns:
        Token: Access token and token type.
    """
    # Fetch user from the database
    query = select(users).where(users.c.email == user.email)
    dbUser = await database.fetch_one(query)
    if not dbUser:
        raise HTTPException(status_code=400, detail="Invalid email or password.")

    # Verify password
    if not verifyPassword(user.password, dbUser['hashed_password']):
        raise HTTPException(status_code=400, detail="Invalid email or password.")

    # Generate JWT token
    accessTokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    accessToken = createAccessToken(
        data={"sub": dbUser['email']}, expiresDelta=accessTokenExpires
    )

    return {"accessToken": accessToken, "tokenType": "bearer"}
