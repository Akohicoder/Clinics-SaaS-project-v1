from sqlalchemy.orm import Session
from sqlalchemy import or_

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


from sqlalchemy import or_

def get_patients_by_clinic(
    db: Session,
    clinic_id: int,
    search: str | None = None,
    page: int = 1,
    size: int = 10,
    sort: str = "PatientID"
):

    query = (
        db.query(Patient)
        .filter(Patient.ClinicID == clinic_id)
    )

    if search:
        query = query.filter(
            or_(
                Patient.FullName.contains(search),
                Patient.Phone.contains(search)
            )
        )

    if sort == "name":
        query = query.order_by(Patient.FullName)

    elif sort == "date":
        query = query.order_by(Patient.CreatedAt.desc())

    else:
        query = query.order_by(Patient.PatientID)

    return (
        query
        .offset((page - 1) * size)
        .limit(size)
        .all()
)