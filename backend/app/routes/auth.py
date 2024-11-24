# backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext

router = APIRouter()

# Password hashing setup 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy users database for demonstration purposes
fake_users_db = {}

# Pydantic models for request validation
class User(BaseModel):
    username: str 
    password: str

class UserInDB(User):
    hashed_password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Sign-Up Route 
@router.post("/signup")
async def signup(user: User):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password cannot be empty")
    
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed_password}
    
    return {"message": "User registered successfully"}

# Login Route
@router.post("/login")
async def login(credentials: LoginRequest):
    if not credentials.username or not credentials.password:
        raise HTTPException(status_code=400, detail="Username and password cannot be empty")
    
    user = fake_users_db.get(credentials.username)
    if user is None or not verify_password(credentials.password, user['hashed_password']):
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    
    return {"message": "Login successful"}
