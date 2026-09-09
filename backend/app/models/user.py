"""
User model — the single auth identity for every person in MediMind AI
(patient, doctor, or admin). Patient/Doctor-specific fields (Phase 2)
will live in their own tables, related 1:1 back to this User via
user_id — this table stays auth-only on purpose.
"""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserRole(str, enum.Enum):
    """
    Enum instead of a free-text string column — this is deliberate:
    it lets the database itself reject an invalid role value, and it
    gives us a single source of truth that both the model and the
    Pydantic schemas import from.
    """

    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    # Never store or return plaintext passwords. This column holds a
    # bcrypt hash only — see app/core/security.py (Step 3).
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            # Without this, SQLAlchemy stores the Python member NAMES
            # ('PATIENT') in Postgres instead of the enum's actual string
            # VALUES ('patient'). We want the DB constraint to match the
            # lowercase values our API and UserRole(str, Enum) actually use.
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        default=UserRole.PATIENT,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        # Deliberately excludes password_hash from repr — reprs can end
        # up in logs/tracebacks, and the hash has no business being there.
        return f"<User id={self.id} email={self.email} role={self.role.value}>"
