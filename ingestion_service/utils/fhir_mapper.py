# utils/fhir_mapper.py

from fhir.resources.patient import Patient
from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.observation import Observation
from fhir.resources.humanname import HumanName
from fhir.resources.meta import Meta
from fhir.resources.fhirtypes import DateTime as FHIRDate
from fhir.resources.fhirtypes import ReferenceType as FHIRReference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.quantity import Quantity
from datetime import datetime
import uuid

def build_patient_resource(name="Unknown", birth_date="2000-01-01"):
    patient_id = str(uuid.uuid4())
    return Patient(
        id=patient_id,
        name=[HumanName(given=[name])],
        birthDate=birth_date,
        meta=Meta(profile=["http://hl7.org/fhir/StructureDefinition/Patient"])
    )


def build_observation(code_text="Report Summary", value="No details", date=None):
    try:
        numeric_value = float(value)
        return Observation(
            id=str(uuid.uuid4()),
            status="final",
            code=CodeableConcept(text=code_text),
            valueQuantity=Quantity(value=numeric_value),
            effectiveDateTime=FHIRDate.validate(date or datetime.utcnow().isoformat())
        )
    except (ValueError, TypeError):
        return Observation(
            id=str(uuid.uuid4()),
            status="final",
            code=CodeableConcept(text=code_text),
            valueString=value,
            effectiveDateTime=FHIRDate.validate(date or datetime.utcnow().isoformat())
        )


def build_diagnostic_report(patient, observation):
    return DiagnosticReport(
        id=str(uuid.uuid4()),
        status="final",
        code=CodeableConcept(text="Multi-format report"),
        subject=FHIRReference(reference=f"Patient/{patient.id}"),
        result=[FHIRReference(reference=f"Observation/{observation.id}")],
        presentedForm=[{
            "contentType": "application/json",
            "data": "..."  # You can embed Base64 if needed
        }]
    )
