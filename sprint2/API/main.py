from fastapi import FastAPI
from API.task24_fit_score import router as task24_router

app = FastAPI()

app.include_router(task24_router)
