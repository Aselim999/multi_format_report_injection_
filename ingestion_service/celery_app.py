# ingestion_service/celery_app.py
from celery import Celery

app = Celery(
    "ingestion_service",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

app.conf.task_routes = {
    "tasks.*": {"queue": "ingestion"}
}
