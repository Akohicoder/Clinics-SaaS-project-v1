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

