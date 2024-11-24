# main.py
from fastapi import FastAPI
from api.task10_validation import router as task10_router
from api.task12_in_memory_storage import router as task12_router
from api.task11_text_extraction import router as task11_router

app = FastAPI()
app.include_router(task10_router, prefix="/api")
app.include_router(task12_router, prefix="/api")
app.include_router(task12_router, prefix="/api", tags=["Task 12"])
app.include_router(task11_router)