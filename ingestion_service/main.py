from fastapi import FastAPI
from routes import router
from db.models import init_db

if __name__ == "__main__":
    init_db()

app = FastAPI(
    title="ThakaaMed Multi-Format Report Injection API",
    description="Upload and queue multi-format reports for AI-ready processing.",
    version="1.0.0"
)

# Register all routes from routes.py
app.include_router(router)
