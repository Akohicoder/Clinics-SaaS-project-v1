from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    Boolean,
    Text
)

from sqlalchemy.orm import relationship

from app.database import Base

from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime

from sqlalchemy import Unicode

class Role(Base):
    __tablename__ = "Roles"

    RoleID = Column(Integer, primary_key=True, index=True)
    RoleName = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")

class Clinic(Base):
    __tablename__ = "Clinics"

    ClinicID = Column(Integer, primary_key=True, index=True)
    ClinicName = Column(String(100), nullable=False)
    Email = Column(String(150), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    Phone = Column(String(20))
    Address = Column(String(250))
    WhatsAppPhoneNumber = Column(String(20))
    WhatsAppPhoneNumberID = Column(String(100))
    WhatsAppAccessToken = Column(Text)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="clinic")
    patients = relationship("Patient", back_populates="clinic")
    appointments = relationship("Appointment", back_populates="clinic")

class User(Base):
    __tablename__ = "Users"

    UserID = Column(Integer, primary_key=True, index=True)
    ClinicID = Column(Integer, ForeignKey("Clinics.ClinicID"))
    FullName = Column(Unicode(100), nullable=False)
    PINHash = Column(String(255), nullable=False)
    RoleID = Column(Integer, ForeignKey("Roles.RoleID"))
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    clinic = relationship("Clinic", back_populates="users")
    role = relationship("Role", back_populates="users")

class Patient(Base):
    __tablename__ = "Patients"

    PatientID = Column(Integer, primary_key=True, index=True)

    ClinicID = Column(
        Integer,
        ForeignKey("Clinics.ClinicID")
    )

    FullName = Column(Unicode(100))

    Phone = Column(String)

    Gender = Column(String)

    DateOfBirth = Column(Date)

    Notes = Column(String)

    CreatedAt = Column(
    DateTime,
    default=datetime.utcnow
    )

    clinic = relationship(
        "Clinic",
        back_populates="patients"
    )

class Appointment(Base):
    __tablename__ = "Appointments"

    AppointmentID = Column(Integer, primary_key=True, index=True)
    ClinicID = Column(Integer, ForeignKey("Clinics.ClinicID"))
    PatientID = Column(Integer, ForeignKey("Patients.PatientID"))
    DoctorID = Column(Integer, ForeignKey("Users.UserID"))
    AppointmentDate = Column(DateTime)
    Status = Column(String(30))
    ReminderSent = Column(Boolean)
    Confirmed = Column(Boolean)
    Notes = Column(Text)

    clinic = relationship("Clinic", back_populates="appointments")

