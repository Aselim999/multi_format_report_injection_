# TODO: implement main.py
from fastapi import FastAPI
from ingestion_service.routes import router as ingestion_router

app = FastAPI(
    title="Multi-Format Report Injection API",
    version="0.1"
)

app.include_router(ingestion_router, prefix="/api")
