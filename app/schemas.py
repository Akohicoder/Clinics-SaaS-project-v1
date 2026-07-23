from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional



class ClinicLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    UserID: int
    FullName: str
    RoleID: int
    Avatar: str | None = None

    class Config:
        from_attributes = True

class PinLoginRequest(BaseModel):
    user_id: int
    pin: str

class PatientCreate(BaseModel):
    FullName: str
    Phone: str
    Gender: str
    DateOfBirth: date
    Notes: str | None = None

class PatientResponse(BaseModel):
    PatientID: int
    ClinicID: int
    FullName: str
    Phone: str
    Gender: str
    DateOfBirth: date
    Notes: str | None = None
    CreatedAt: datetime | None = None

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    PatientID: int
    DoctorID: int
    AppointmentDate: datetime
    Notes: str | None = None

class AppointmentResponse(BaseModel):
    AppointmentID: int
    ClinicID: int
    PatientID: int
    DoctorID: int
    AppointmentDate: datetime
    Status: str
    ReminderSent: bool
    Confirmed: bool
    Notes: str | None = None

    class Config:
        from_attributes = True

class AppointmentListResponse(BaseModel):
    AppointmentID: int
    PatientName: str
    DoctorName: str
    AppointmentDate: datetime
    Status: str

    class Config:
        from_attributes = True

class AppointmentUpdate(BaseModel):
    DoctorID: int
    AppointmentDate: datetime
    Status: str
    Notes: str | None = None

class DashboardResponse(BaseModel):
    total_patients: int
    today_appointments: int
    confirmed_appointments: int
    pending_appointments: int
    cancelled_appointments: int

class DashboardResponse(BaseModel):
    total_patients: int
    today_appointments: int
    confirmed_appointments: int
    pending_appointments: int
    cancelled_appointments: int
