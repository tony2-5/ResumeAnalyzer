# backend/main.py

from fastapi import FastAPI
from database import database, engine, metadata
from routers import register, login, get_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Create all tables
metadata.create_all(engine)

#configure cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(register.router, prefix="/api")
app.include_router(login.router, prefix="/api")
app.include_router(get_user.router, prefix="/api")

@app.on_event("startup")
async def startup():
    """
    Connect to the database when the application starts.
    """
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    """
    Disconnect from the database when the application shuts down.
    """
    await database.disconnect()
