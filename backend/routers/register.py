from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from backend.models import users
from backend.schemas import UserCreate
from backend.database import database
from backend.auth import getPasswordHash

router = APIRouter()

@router.post("/register", status_code=201)
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

    return  { "message": "User registered." }
