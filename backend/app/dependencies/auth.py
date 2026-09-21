"""
FastAPI dependencies for authentication and role-based authorization.

get_current_user is the ONLY place a request's JWT is decoded and
turned into a User. Every protected route depends on it (directly or
via one of the require_* dependencies below), so there is exactly one
code path to audit for "how does auth actually work".

This is also the enforcement point the system prompt for this project
cares about most: role checks happen here, server-side, on every
request — never trusted from the frontend.
"""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import InvalidTokenError, decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories import user_repository

# tokenUrl points at our login route so FastAPI's /docs "Authorize" button
# works out of the box — it doesn't create any extra endpoint itself.
_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(_oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
    except InvalidTokenError:
        raise credentials_error

    subject = payload.get("sub")
    if subject is None:
        raise credentials_error

    try:
        user_id = uuid.UUID(subject)
    except ValueError:
        raise credentials_error

    user = user_repository.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_error

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive"
        )

    return user


def _require_role(*allowed_roles: UserRole):
    """
    Factory for role-restricted dependencies. Returns a dependency
    function rather than being one itself, so `require_patient`,
    `require_doctor`, `require_admin` below stay simple and readable
    at the route definition instead of every route writing out a
    role-check inline.
    """

    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return dependency


require_patient = _require_role(UserRole.PATIENT)
require_doctor = _require_role(UserRole.DOCTOR)
require_admin = _require_role(UserRole.ADMIN)
