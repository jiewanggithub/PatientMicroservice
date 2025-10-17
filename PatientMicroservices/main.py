from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.db import get_db, Base, engine
from models.models import PatientORM
from models.patient import PatientCreate, PatientUpdate, PatientRead

app = FastAPI(title="PatientMicroservice API", version="1.0.0")

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

# --- Patient CRUD only ---
@app.get("/patients", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db)):
    return db.query(PatientORM).all()

@app.post("/patients", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    row = PatientORM(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    row = db.query(PatientORM).get(patient_id)
    if not row:
        raise HTTPException(404, "Patient not found")
    return row

@app.put("/patients/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: str, payload: PatientUpdate, db: Session = Depends(get_db)):
    row = db.query(PatientORM).get(patient_id)
    if not row:
        raise HTTPException(404, "Patient not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(row, k, v)
    db.commit()
    db.refresh(row)
    return row

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    row = db.query(PatientORM).get(patient_id)
    if not row:
        raise HTTPException(404, "Patient not found")
    db.delete(row)
    db.commit()
    return None



# List all patients
# @app.get("/patients", response_model=List[PatientRead])
# def list_patients() -> List[PatientRead]:
#     """Return all patient records."""
#     return list(patients.values())
#
#
# # Create a new patient
# @app.post("/patients", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
# def create_patient(patient: PatientCreate) -> PatientRead:
#     """Create a new patient record."""
#     new_patient = PatientRead(
#         id=uuid4(),
#         first_name=patient.first_name,
#         last_name=patient.last_name,
#         date_of_birth=patient.date_of_birth,
#         gender=patient.gender,
#         phone_number=patient.phone_number,
#         email=patient.email,
#         address=patient.address,
#         emergency_contact=patient.emergency_contact,
#         created_at=datetime.utcnow(),
#         updated_at=None,
#     )
#     patients[new_patient.id] = new_patient
#     return new_patient


# Retrieve a specific patient
# @app.get("/patients/{patient_id}", response_model=PatientRead)
# def get_patient(patient_id: UUID) -> PatientRead:
#     """Retrieve a patient by ID."""
#     patient = patients.get(patient_id)
#     if not patient:
#         raise HTTPException(status_code=404, detail="Patient not found")
#     return patient
#
#
# # Update a patient's information
# @app.put("/patients/{patient_id}", response_model=PatientRead)
# def update_patient(patient_id: UUID, update: PatientUpdate) -> PatientRead:
#     """Update an existing patient record."""
#     existing = patients.get(patient_id)
#     if not existing:
#         raise HTTPException(status_code=404, detail="Patient not found")
#
#     updated_data = update.dict(exclude_unset=True)
#     updated_patient = existing.model_copy(update=updated_data)
#     updated_patient.updated_at = datetime.utcnow()
#
#     patients[patient_id] = updated_patient
#     return updated_patient
#
#
# # Delete a patient record
# @app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_patient(patient_id: UUID):
#     """Delete a patient by ID."""
#     if patient_id not in patients:
#         raise HTTPException(status_code=404, detail="Patient not found")
#     del patients[patient_id]
#     return None
#
#
# # -------------------------------------------------------------------
# # Appointments – Retrieve
# # -------------------------------------------------------------------