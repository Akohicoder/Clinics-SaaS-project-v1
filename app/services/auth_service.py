from sqlalchemy.orm import Session
from app.models import Clinic


def get_clinic_by_email(db: Session, email: str):
    return db.query(Clinic).filter(Clinic.Email == email).first()