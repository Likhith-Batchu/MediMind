"""
Authentication business logic.

Routes call this layer; this layer calls the repository. Routes never
touch the database directly. This is also where we make the two
security-sensitive decisions explicit:

1. Public registration can only ever produce a PATIENT account.
2. Login failures (wrong password vs. unknown email) return the exact
   same error, so a client can't use the API to enumerate which
   emails are registered.
"""

from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories import user_repository


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    """Raised for both 'no such user' and 'wrong password' — see module docstring."""


def register_patient(db: Session, email: str, password: str) -> User:
    if user_repository.get_user_by_email(db, email) is not None:
        raise EmailAlreadyRegisteredError(f"Email already registered: {email}")

    password_hash = hash_password(password)
    # role is hardcoded to PATIENT here — not read from any client input,
    # by design, so there's no code path where a request body could
    # result in a DOCTOR or ADMIN account.
    return user_repository.create_user(
        db, email=email, password_hash=password_hash, role=UserRole.PATIENT
    )


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = user_repository.get_user_by_email(db, email)

    # Deliberately identical failure for "no user" and "wrong password".
    # Also deliberately still runs verify_password-shaped work either way
    # would be a further hardening step (constant-time against timing
    # attacks) — out of scope for this phase, noted in SECURITY.md.
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError("Incorrect email or password")

    if not user.is_active:
        raise InvalidCredentialsError("Incorrect email or password")

    return user


def create_token_for_user(user: User) -> str:
    return create_access_token(subject=str(user.id), role=user.role.value)
