"""
User repository — the only module that runs SQL/ORM queries against the
`users` table. Services call this rather than touching `db.query(...)`
directly, so if the query layer ever needs to change (e.g. caching,
different DB), only this file changes.
"""

import uuid

from sqlalchemy.orm import Session

from app.models.user import User, UserRole


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, password_hash: str, role: UserRole) -> User:
    user = User(email=email, password_hash=password_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
