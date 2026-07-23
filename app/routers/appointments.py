from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import  get_current_clinic
from fastapi import HTTPException
from datetime import date


from app.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentListResponse,
    AppointmentUpdate
)

from app.services.appointment_service import (
    create_appointment,
    get_appointments_by_clinic,
    update_appointment,
    cancel_appointment
    )


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
    appointment_date: date | None = Query(default=None),
    doctor_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    return get_appointments_by_clinic(
        db,
        clinic_id,
        appointment_date,
        doctor_id,
        status 
    )

@router.put("/{appointment_id}", response_model=AppointmentResponse)
def edit_appointment(
    appointment_id: int,
    data: AppointmentUpdate,
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    appointment = update_appointment(
        db,
        clinic_id,
        appointment_id,
        data
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment

@router.delete("/{appointment_id}")
def cancel(
    appointment_id: int,
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    appointment = cancel_appointment(
        db,
        clinic_id,
        appointment_id
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return {
        "message": "Appointment cancelled successfully"
    }