# 🏥 Multi-Format Report Injection System

This application ingests, processes, and standardizes healthcare reports from various sources (PDF, Word, DICOM, HL7, SQL, JSON) into a unified FHIR R4-compatible format for integration with ThakaaMed’s AI analysis pipeline.

---

## 📦 Features

- ✅ Supports multi-format ingestion: PDF, DOCX, DICOM, HL7 v2, SQL, JSON
- 🧠 Standardizes output to FHIR R4 (Patient, Observation, DiagnosticReport)
- 🗃️ Stores raw and FHIR outputs into PostgreSQL
- ⚙️ Background async processing with Celery + Redis
- 🔐 JWT authentication for upload endpoint
- 🐳 Microservices architecture using Docker
- 🌐 RESTful API with Swagger docs

---

## 🚀 Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/your-org/multi-format-ingestion.git
cd multi-format-ingestion
```

2. Add .env file
   Create a .env file at the root:

ini



# .env

SECRET_KEY=your_jwt_secret_key 3. Start the services
bash


docker-compose up --build
Access the API at http://localhost:8000

📂 Project Structure
graphql


.
├── app/
│ ├── main.py # FastAPI entrypoint
│ ├── routes.py # Upload endpoint
│ ├── tasks.py # Celery background task
│ ├── db/ # SQLAlchemy models & session
│ ├── utils/
│ │ ├── file_handlers.py # Parsers for each file type
│ │ ├── fhir_mapper.py # FHIR R4 resource builder
│ │ └── auth.py # JWT token generator & verifier
├── outputs/ # Saved parsed JSON results
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
🔐 JWT Authentication
To upload, include your JWT token:

bash


curl -X POST http://localhost:8000/upload?token=<JWT_TOKEN> \
 -F "file=@/path/to/your/file.pdf"
🧪 Testing Strategy

1. Unit Tests
   Test all parsers individually (test_file_handlers.py)

Test FHIR mappers (test_fhir_mapper.py)

Test authentication (test_auth.py)

2. Integration Tests
   Upload endpoint with different file types (test_upload_endpoint.py)

Full flow: Upload → Background Task → DB entry

Run all tests:
bash


pytest
📥 Example Upload Response
json


{
"status": "queued",
"task_id": "abcd-1234",
"file_id": "uuid-file-id",
"filename": "report.pdf"
}
🧪 Sample Files
Place test files under samples/ to try:

PDF

DOCX

DICOM

HL7

SQL

JSON

🐳 Docker Deployment
Build + Start
bash


docker-compose up --build
Shut Down
bash


docker-compose down
📚 API Docs
Once the app is running, access:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🔐 Security
JWT Auth protects all upload endpoints

Character encoding handled (Arabic/English)

Future: TLS/HTTPS, encrypted volumes

✅ Deliverables Summary
Deliverable Status
Multi-format ingestion ✅ Done
DICOM/HL7/SQL/JSON/Doc/PDF ✅ Done
FHIR R4 output ✅ Done
Celery/Redis async tasks ✅ Done
PostgreSQL logs ✅ Done
Swagger API ✅ Done
Docker-based setup ✅ Done
JWT auth ✅ Done
Character encoding (Arabic) ✅ Done
Output saved to disk/DB ✅ Done
Testing (unit + integration) ✅ In progress
Deployment guide ✅ This README

🧠 Authors
Abdalla Mustafa Selim
Healthcare Integrations Engineer | Backend Dev | FHIR/DICOM/HL7 Enthusiast
