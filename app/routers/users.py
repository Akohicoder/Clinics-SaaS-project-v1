from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_clinic
from app.services.user_service import get_users_by_clinic
from app.schemas import UserResponse

from fastapi import HTTPException
from app.schemas import PinLoginRequest
from app.services.user_service import pin_login

from app.security import create_user_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    return get_users_by_clinic(db, clinic_id)

@router.post("/pin-login")
def login_with_pin(
    data: PinLoginRequest,
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    user = pin_login(
        db,
        clinic_id,
        data.user_id,
        data.pin
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user is False:
        raise HTTPException(
            status_code=401,
            detail="Wrong PIN"
        )

    token = create_user_access_token({
        "clinic_id": clinic_id,
        "user_id": user.UserID,
        "role_id": user.RoleID,
        "full_name": user.FullName
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.UserID,
            "name": user.FullName,
            "role_id": user.RoleID
        }
    }