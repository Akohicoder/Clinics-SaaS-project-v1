from datetime import date

from sqlalchemy import func, Date
from sqlalchemy.orm import Session
from starlette import status
from starlette import status

from app.models import Appointment, Patient, User
from app.schemas import AppointmentCreate, AppointmentUpdate


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
    clinic_id: int,
    appointment_date: date | None = None,
    doctor_id: int | None = None,
    status: str | None = None

):
    query = (
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
    )
    if appointment_date:
        query = query.filter(
        func.cast(Appointment.AppointmentDate, Date) == appointment_date
    )

    if doctor_id:
        query = query.filter(
        Appointment.DoctorID == doctor_id
    )

    if status:
        query = query.filter(
        Appointment.Status == status
    )
    return query.all()


def update_appointment(
    db: Session,
    clinic_id: int,
    appointment_id: int,
    data: AppointmentUpdate
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.AppointmentID == appointment_id,
            Appointment.ClinicID == clinic_id
        )
        .first()
    )

    if appointment is None:
        return None

    doctor = (
        db.query(User)
        .filter(
            User.UserID == data.DoctorID,
            User.ClinicID == clinic_id
        )
        .first()
    )

    if doctor is None:
        raise ValueError("Doctor not found")

    appointment.DoctorID = data.DoctorID
    appointment.AppointmentDate = data.AppointmentDate
    appointment.Status = data.Status
    appointment.Notes = data.Notes

    db.commit()
    db.refresh(appointment)

    return appointment

def cancel_appointment(
    db: Session,
    clinic_id: int,
    appointment_id: int
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.AppointmentID == appointment_id,
            Appointment.ClinicID == clinic_id
        )
        .first()
    )

    if appointment is None:
        return None

    appointment.Status = "Cancelled"

    db.commit()
    db.refresh(appointment)

    return appointment