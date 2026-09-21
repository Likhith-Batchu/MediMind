"""
Health check routes.

Also includes role-gated diagnostic endpoints (/health/patient-only etc.)
whose only purpose is to prove require_patient / require_doctor /
require_admin actually enforce role boundaries. These are not real
product features — Phase 2+ will add real role-protected endpoints
(appointments, records, etc.) that replace the need to test against
these stand-ins.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import require_admin, require_doctor, require_patient
from app.models.user import User

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "MediMind AI backend"}


@router.get("/health/db")
def health_check_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}


@router.get("/health/patient-only")
def patient_only_check(current_user: User = Depends(require_patient)):
    return {"message": f"Hello patient {current_user.email}"}


@router.get("/health/doctor-only")
def doctor_only_check(current_user: User = Depends(require_doctor)):
    return {"message": f"Hello doctor {current_user.email}"}


@router.get("/health/admin-only")
def admin_only_check(current_user: User = Depends(require_admin)):
    return {"message": f"Hello admin {current_user.email}"}
