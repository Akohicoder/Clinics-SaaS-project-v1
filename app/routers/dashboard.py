from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_clinic
from app.schemas import DashboardResponse
from app.services.dashboard_service import get_dashboard_stats

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/", response_model=DashboardResponse)
def dashboard(
    db: Session = Depends(get_db),
    payload=Depends(get_current_clinic)
):
    clinic_id = payload["clinic_id"]

    return get_dashboard_stats(
        db,
        clinic_id
    )