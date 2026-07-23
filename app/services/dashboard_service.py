from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func, Date

from app.models import Patient, Appointment

def get_dashboard_stats(
    db: Session,
    clinic_id: int
):
    total_patients = (
    db.query(func.count(Patient.PatientID))
    .filter(Patient.ClinicID == clinic_id)
    .scalar()
)

    today_appointments = (
    db.query(func.count(Appointment.AppointmentID))
    .filter(
        Appointment.ClinicID == clinic_id,
        func.cast(Appointment.AppointmentDate, Date) == date.today()
    )
    .scalar()
)
    confirmed_appointments = (
        db.query(func.count(Appointment.AppointmentID))
        .filter(
            Appointment.ClinicID == clinic_id,
            Appointment.Status == "Confirmed"
        )
        .scalar()
    )

    pending_appointments = (
        db.query(func.count(Appointment.AppointmentID))
        .filter(
            Appointment.ClinicID == clinic_id,
            Appointment.Status == "Pending"
        )
        .scalar()
    )

    cancelled_appointments = (
        db.query(func.count(Appointment.AppointmentID))
        .filter(
            Appointment.ClinicID == clinic_id,
            Appointment.Status == "Cancelled"
        )
        .scalar()
    )

    return {
        "total_patients": total_patients,
        "today_appointments": today_appointments,
        "confirmed_appointments": confirmed_appointments,
        "pending_appointments": pending_appointments,
        "cancelled_appointments": cancelled_appointments
    }