"""
Declarative base class that all SQLAlchemy models will inherit from.
Kept in its own file so Alembic can import it without pulling in
every model module (avoids circular imports later).
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
