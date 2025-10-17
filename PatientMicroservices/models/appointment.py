from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class AppointmentBase(BaseModel):
    title: str = Field(..., description="Short reason or title for the appointment.")
    starts_at: datetime = Field(..., description="Start time (UTC).")
    ends_at: Optional[datetime] = Field(None, description="End time (UTC).")
    location: Optional[str] = Field(None, description="Optional location/room.")

    model_config = {
        "title": "AppointmentBase",
        "json_schema_extra": {
            "example": {
                "title": "Follow-up visit",
                "starts_at": "2025-10-20T14:00:00Z",
                "ends_at": "2025-10-20T14:30:00Z",
                "location": "Clinic Room 3B",
            }
        },
    }

class AppointmentCreate(AppointmentBase):
    model_config = {"title": "AppointmentCreate"}

class AppointmentRead(AppointmentBase):
    id: UUID = Field(default_factory=uuid4, description="Appointment ID.")
    patient_id: UUID = Field(..., description="Owner patient ID.")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    model_config = {
        "title": "AppointmentRead",
        "json_schema_extra": {
            "example": {
                "id": "6a9a6f1a-6e82-4d44-9d8f-5d7b3c7f71fd",
                "patient_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Follow-up visit",
                "starts_at": "2025-10-20T14:00:00Z",
                "ends_at": "2025-10-20T14:30:00Z",
                "location": "Clinic Room 3B",
                "created_at": "2025-10-17T15:00:00Z",
                "updated_at": None,
            }
        },
    }
