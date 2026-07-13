from sqlalchemy.orm import Session

from app.models import Patient
from app.schemas import PatientCreate



def create_patient(
    db: Session,
    clinic_id: int,
    data: PatientCreate
):


    patient = Patient(
        ClinicID=clinic_id,
        FullName=data.FullName,
        Phone=data.Phone,
        Gender=data.Gender,
        DateOfBirth=data.DateOfBirth,
        Notes=data.Notes
    )

    db.add(patient)

    db.commit()

    db.refresh(patient)

    print("FullName =", data.FullName)
    print(type(data.FullName))

    return patient


def get_patients_by_clinic(
    db: Session,
    clinic_id: int
):
    return (
        db.query(Patient)
        .filter(Patient.ClinicID == clinic_id)
        .all()
    )