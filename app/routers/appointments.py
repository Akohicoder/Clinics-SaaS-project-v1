from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import  get_current_clinic


from app.schemas import AppointmentCreate, AppointmentListResponse, AppointmentResponse
from app.services.appointment_service import (create_appointment,get_appointments_by_clinic)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

@router.post("/", response_model=AppointmentResponse)
def add_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    return create_appointment(
        db,
        clinic_id,
        data
    )

@router.get("/", response_model=list[AppointmentListResponse])
def get_appointments(
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    return get_appointments_by_clinic(
        db,
        clinic_id
    )