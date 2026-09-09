"""
Import every model here so that:
1. `Base.metadata` knows about all tables (needed for Alembic autogenerate).
2. Other modules can `from app.models import User` instead of reaching
   into individual files.
"""

from app.models.user import User, UserRole  # noqa: F401
