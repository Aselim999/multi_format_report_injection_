# ingestion_service/Dockerfile

FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY ../requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libmagic1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
