from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_clinic

from app.schemas import PatientCreate, PatientResponse
from app.services.patient_service import (
    create_patient,
    get_patients_by_clinic
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.post("/", response_model=PatientResponse)
def add_patient(
    data: PatientCreate,
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):

    clinic_id = payload["clinic_id"]

    return create_patient(
        db,
        clinic_id,
        data
    )

@router.get("/", response_model=list[PatientResponse])
def get_patients(
    search: str |None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    sort: str = Query(default="id"),
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    return get_patients_by_clinic(
        db,
        clinic_id,
        search,
        page,
        size,
        sort
    )