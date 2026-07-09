from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import ClinicLogin
from app.database import get_db
from app.services.auth_service import get_clinic_by_email
from app.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    data: ClinicLogin,
    db: Session = Depends(get_db)
):

    clinic = get_clinic_by_email(db, data.email)

    if clinic is None:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    if not verify_password(
        data.password,
        clinic.PasswordHash
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    token = create_access_token({
        "clinic_id": clinic.ClinicID,
        "email": clinic.Email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }