# backend/main.py

from fastapi import FastAPI
from database import database, engine, metadata
from routers import register, login, get_user

app = FastAPI()

# Create all tables
metadata.create_all(engine)

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
