"""
Health check routes.

Purpose: prove that (a) the API is up, and (b) the API can reach the
database. This is the first thing we test in Phase 0 before building
any real features.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "MediMind AI backend"}


@router.get("/health/db")
def health_check_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
