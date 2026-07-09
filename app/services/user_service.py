from sqlalchemy.orm import Session
from app.models import User
from app.security import verify_password




def get_users_by_clinic(db: Session, clinic_id: int):
    return (
        db.query(User)
        .filter(User.ClinicID == clinic_id)
        .all()
    )


def pin_login(
    db: Session,
    clinic_id: int,
    user_id: int,
    pin: str
):
    user = (
        db.query(User)
        .filter(
            User.UserID == user_id,
            User.ClinicID == clinic_id,
            User.IsActive == True
        )
        .first()
    )

    if user is None:
        return None

    if not verify_password(pin, user.PINHash):
        return False

    return user
