from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class TranscriptionBase(BaseModel):
    source: str = Field(..., description="Where this came from (e.g., 'visit-note', 'upload').")
    content: str = Field(..., description="Raw text or URL pointer to the doc.")

    model_config = {
        "title": "TranscriptionBase",
        "json_schema_extra": {
            "example": {
                "source": "visit-note",
                "content": "Patient reports improved symptoms. BP 120/78...",
            }
        },
    }

class TranscriptionCreate(TranscriptionBase):
    model_config = {"title": "TranscriptionCreate"}

class TranscriptionRead(TranscriptionBase):
    id: UUID = Field(default_factory=uuid4, description="Transcription ID.")
    patient_id: UUID = Field(..., description="Owner patient ID.")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "title": "TranscriptionRead",
        "json_schema_extra": {
            "example": {
                "id": "4b2c2a08-8a2f-49f8-9c1a-0c9f39d2d6e1",
                "patient_id": "550e8400-e29b-41d4-a716-446655440000",
                "source": "visit-note",
                "content": "Patient reports improved symptoms. BP 120/78...",
                "created_at": "2025-10-17T15:05:00Z",
            }
        },
    }
