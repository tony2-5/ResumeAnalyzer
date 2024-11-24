# backend/main.py

from fastapi import FastAPI, Request
from backend.database import database, engine, metadata
from backend.routers import register, login, get_user
from api.task10_validation import router as task10_router
from api.task12_in_memory_storage import router as task12_router
from api.task11_text_extraction import router as task11_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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
app.include_router(task10_router, prefix="/api")
app.include_router(task12_router, prefix="/api")
app.include_router(task12_router, prefix="/api", tags=["Task 12"])
app.include_router(task11_router)

# handler to capture 422 errors and make them 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )

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