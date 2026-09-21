"""
Pydantic schemas for User-related requests and responses.

Rule enforced by design here: UserResponse has no password_hash field at
all, so it is structurally impossible for an endpoint using this schema
to leak it, regardless of what the ORM object contains.
"""

import re
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import UserRole

_PASSWORD_MIN_LENGTH = 8


class UserRegister(BaseModel):
    """
    Request body for public self-registration.

    Deliberately has NO `role` field — public registration always
    creates a PATIENT account. This is enforced by the schema shape
    itself, not just by service-layer logic, so there's no field a
    client could even attempt to set to "admin".
    """

    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < _PASSWORD_MIN_LENGTH:
            raise ValueError(
                f"Password must be at least {_PASSWORD_MIN_LENGTH} characters long"
            )
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Safe user representation returned by the API. No password_hash."""

    id: uuid.UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
