from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_clinic

from app.schemas import PatientCreate, PatientResponse
from app.services.patient_service import create_patient

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