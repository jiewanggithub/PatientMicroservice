# main.py
from typing import Dict, List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, status
from models.patient import PatientCreate, PatientRead, PatientUpdate  # import your models
from models.transcription import TranscriptionCreate, TranscriptionRead
from models.appointment import AppointmentRead, AppointmentCreate, AppointmentBase
import os
from datetime import datetime


app = FastAPI(
    title="PatientMicroservice API",
    version="1.0.0",
    description="API for patients, appointments, and transcriptions.",
)

# In-memory stores
patients: Dict[UUID, PatientRead] = {}
appointments: Dict[UUID, Dict[UUID, AppointmentRead]] = {}   # patient_id -> {appointment_id: AppointmentRead}
transcriptions: Dict[UUID, Dict[UUID, TranscriptionRead]] = {}  # patient_id -> {transcription_id: TranscriptionRead}

port = int(os.environ.get("FASTAPI_PORT", 8000))

# -------------------------------------------------------------------
# FastAPI app definition
# -------------------------------------------------------------------
app = FastAPI(
    title="PatientMicroservice API",
    description="API for managing patients using Pydantic v2 models.",
    version="1.0.0",
)

# -------------------------------------------------------------------
# Patient endpoints
# -------------------------------------------------------------------

# List all patients
@app.get("/patients", response_model=List[PatientRead])
def list_patients() -> List[PatientRead]:
    """Return all patient records."""
    return list(patients.values())


# Create a new patient
@app.post("/patients", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate) -> PatientRead:
    """Create a new patient record."""
    new_patient = PatientRead(
        id=uuid4(),
        first_name=patient.first_name,
        last_name=patient.last_name,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        phone_number=patient.phone_number,
        email=patient.email,
        address=patient.address,
        emergency_contact=patient.emergency_contact,
        created_at=datetime.utcnow(),
        updated_at=None,
    )
    patients[new_patient.id] = new_patient
    return new_patient


# Retrieve a specific patient
@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: UUID) -> PatientRead:
    """Retrieve a patient by ID."""
    patient = patients.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# Update a patient's information
@app.put("/patients/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: UUID, update: PatientUpdate) -> PatientRead:
    """Update an existing patient record."""
    existing = patients.get(patient_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Patient not found")

    updated_data = update.dict(exclude_unset=True)
    updated_patient = existing.model_copy(update=updated_data)
    updated_patient.updated_at = datetime.utcnow()

    patients[patient_id] = updated_patient
    return updated_patient


# Delete a patient record
@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: UUID):
    """Delete a patient by ID."""
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    del patients[patient_id]
    return None


# -------------------------------------------------------------------
# Appointments – Retrieve
# -------------------------------------------------------------------
@app.get(
    "/patients/{patient_id}/appointments",
    response_model=List[AppointmentRead],
    summary="List a patient's appointments",
)
def list_appointments(patient_id: UUID) -> List[AppointmentRead]:
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    return list(appointments.get(patient_id, {}).values())

@app.get(
    "/patients/{patient_id}/appointments/{appointment_id}",
    response_model=AppointmentRead,
    summary="Get one appointment",
)
def get_appointment(patient_id: UUID, appointment_id: UUID) -> AppointmentRead:
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    appts = appointments.get(patient_id, {})
    appt = appts.get(appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

# -------------------------------------------------------------------
# 📝 Transcriptions – Retrieve
# -------------------------------------------------------------------
@app.get(
    "/patients/{patient_id}/transcriptions",
    response_model=List[TranscriptionRead],
    summary="List transcriptions for a patient",
)
def list_transcriptions(patient_id: UUID) -> List[TranscriptionRead]:
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    return list(transcriptions.get(patient_id, {}).values())

@app.get(
    "/patients/{patient_id}/transcriptions/{transcription_id}",
    response_model=TranscriptionRead,
    summary="Retrieve one transcription",
)
def get_transcription(patient_id: UUID, transcription_id: UUID) -> TranscriptionRead:
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    tmap = transcriptions.get(patient_id, {})
    t = tmap.get(transcription_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transcription not found")
    return t

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
