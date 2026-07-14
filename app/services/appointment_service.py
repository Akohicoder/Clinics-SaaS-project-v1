from sqlalchemy.orm import Session

from app.models import Appointment, Patient, User
from app.schemas import AppointmentCreate


def create_appointment(
    db: Session,
    clinic_id: int,
    data: AppointmentCreate
):
    patient = (
        db.query(Patient)
        .filter(
            Patient.PatientID == data.PatientID,
            Patient.ClinicID == clinic_id
        )
        .first()
    )

    if patient is None:
        raise ValueError("Patient not found or does not belong to the clinic.")

    doctor = (
        db.query(User)
        .filter(
            User.UserID == data.DoctorID,
            User.ClinicID == clinic_id
        )
        .first()
    )

    if doctor is None:
        raise ValueError("Doctor not found or does not belong to the clinic.")

    appointment = Appointment(
        ClinicID=clinic_id,
        PatientID=data.PatientID,
        DoctorID=data.DoctorID,
        AppointmentDate=data.AppointmentDate,
        Status="Pending",
        ReminderSent=False,
        Confirmed=False,
        Notes=data.Notes
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

def get_appointments_by_clinic(
    db: Session,
    clinic_id: int
):
    return (
        db.query(
            Appointment.AppointmentID,
            Patient.FullName.label("PatientName"),
            User.FullName.label("DoctorName"),
            Appointment.AppointmentDate,
            Appointment.Status
        )
        .join(
            Patient,
            Appointment.PatientID == Patient.PatientID
        )
        .join(
            User,
            Appointment.DoctorID == User.UserID
        )
        .filter(
            Appointment.ClinicID == clinic_id
        )
        .all()
    )


    return appointment