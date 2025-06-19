from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.humanname import HumanName
from fhir.resources.fhirdate import FHIRDate

import uuid
from datetime import datetime

def build_patient_resource(name: str, gender: str = "unknown", birth_date: str = None):
    patient_id = str(uuid.uuid4())
    return Patient(
        id=patient_id,
        name=[HumanName(text=name)],
        gender=gender,
        birthDate=FHIRDate(birth_date) if birth_date else None
    )

def build_observation(code: str, value: str):
    return Observation(
        id=str(uuid.uuid4()),
        status="final",
        code={"text": code},
        valueString=value,
        effectiveDateTime=FHIRDate(datetime.utcnow().isoformat())
    )

def build_diagnostic_report(patient: Patient, observations: list):
    return DiagnosticReport(
        id=str(uuid.uuid4()),
        status="final",
        subject={"reference": f"Patient/{patient.id}"},
        result=[{"reference": f"Observation/{obs.id}"} for obs in observations],
        presentedForm=[{"contentType": "text/plain", "data": "Base64-encoded-summary"}]
    )
