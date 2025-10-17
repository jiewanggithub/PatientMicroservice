# models.py
from __future__ import annotations
from sqlalchemy import String, Date, Text, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
import uuid

def uuid_str() -> str:
    return str(uuid.uuid4())

class PatientORM(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name:  Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[Date | None] = mapped_column(Date, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(32), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    emergency_contact: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str | None] = mapped_column(TIMESTAMP, nullable=True, onupdate=func.current_timestamp())
