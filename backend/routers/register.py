from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from models import users
from schemas import UserCreate, UserResponse
from database import database
from auth import getPasswordHash

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def registerUser(user: UserCreate):
    """
    Registering new user.
    """
  
    query = select(users).where(users.c.email == user.email)
    existingUser = await database.fetch_one(query)
    if existingUser:
        raise HTTPException(status_code=400, detail="Email already registered.")


    hashedPassword = getPasswordHash(user.password)


    insertQuery = users.insert().values(
        email=user.email,
        username=user.username,
        hashed_password=hashedPassword
    )
    await database.execute(insertQuery)

    return UserResponse(email=user.email, username=user.username)
