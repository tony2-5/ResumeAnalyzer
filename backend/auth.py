import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from backend.database import database
from backend.models import users
import os
from dotenv import load_dotenv

### Load the .env file
load_dotenv()

SECRET_KEY = os.getenv('JWT_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def getPasswordHash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verifyPassword(plainPassword: str, hashedPassword: str) -> bool:
    return bcrypt.checkpw(plainPassword.encode('utf-8'), hashedPassword.encode('utf-8'))

def createAccessToken(data: dict, expiresDelta: Optional[timedelta] = None) -> str:
    toEncode = data.copy()
    expire = datetime.utcnow() + (expiresDelta or timedelta(minutes=15))
    toEncode.update({"exp": expire.timestamp()})
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt

def decodeAccessToken(token: str) -> dict:
    try:
        decodedToken = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decodedToken
    except jwt.PyJWTError as e:
        raise e

async def getCurrentUser(token: str = Depends(oauth2Scheme)):
    try:
        payload = decodeAccessToken(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Cannot authorize user.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Cannot authorize user.")


    query = select(users).where(users.c.email == email)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=401, detail="Cannot find user.")

    return user