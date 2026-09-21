"""
Core security primitives: password hashing and JWT creation/validation.

Nothing in this file talks to the database or FastAPI — it's pure,
testable crypto/token logic used by the auth service and dependencies.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# passlib handles bcrypt correctly (salting, work factor) — we do not
# implement our own hashing scheme.
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password for storage. Never store the plain value."""
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Check a plaintext password against a stored bcrypt hash."""
    return _pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str, role: str) -> str:
    """
    Create a signed JWT access token.

    `subject` is the user's id (as a string) — stored in the standard
    `sub` claim. `role` is embedded so authorization checks don't need
    a DB lookup on every request, though /auth/me still re-reads from
    the DB to return authoritative user data.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


class InvalidTokenError(Exception):
    """Raised when a JWT is missing, malformed, expired, or has a bad signature."""


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT. Raises InvalidTokenError on any failure
    (bad signature, expired, malformed) so callers have one error type
    to handle rather than reaching into jose's exception hierarchy.
    """
    try:
        return jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError as exc:
        raise InvalidTokenError("Could not validate token") from exc
