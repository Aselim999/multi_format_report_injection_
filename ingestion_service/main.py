# TODO: implement main.py
# ingestion_service/main.py
from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Multi-Format Ingestion Service",
    version="1.0.0"
)

app.include_router(router, prefix="/api")
