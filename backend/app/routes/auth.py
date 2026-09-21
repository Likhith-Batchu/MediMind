"""
Authentication routes.

Kept intentionally thin: each route only translates HTTP <-> service
calls and maps service-layer exceptions to HTTP status codes. No
database queries and no business logic live here directly.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserLogin, UserRegister, UserResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """
    Public registration. Always creates a PATIENT account — see
    UserRegister schema (no role field) and auth_service.register_patient
    (role hardcoded), enforced at two independent layers on purpose.
    """
    try:
        user = auth_service.register_patient(
            db, email=payload.email, password=payload.password
        )
    except auth_service.EmailAlreadyRegisteredError:
        # Registration intentionally DOES confirm the email is taken —
        # unlike login, there's no meaningful enumeration risk here
        # (the user is actively trying to create/claim that address),
        # and a vague error would just make the form confusing to use.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        user = auth_service.authenticate_user(
            db, email=payload.email, password=payload.password
        )
    except auth_service.InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_token_for_user(user)
    return Token(access_token=access_token, user=user)


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
