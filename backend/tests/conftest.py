"""
Shared pytest fixtures for backend tests.

Uses the SAME PostgreSQL database as the app (via DATABASE_URL) rather
than mocking the DB — Phase 1's goal is to prove auth actually works
against a real database, not against a fake. Each test wraps its DB
work in a transaction that's rolled back afterward, so tests don't
leave data behind or interfere with each other.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine
from app.main import app
from app.db.session import get_db


@pytest.fixture()
def db_session():
    """
    Yields a DB session wrapped in a transaction that is rolled back
    at the end of the test, so test data (users, etc.) never persists.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    """
    TestClient with the app's get_db dependency overridden to use the
    same rolled-back-per-test session as db_session, so what the test
    sets up and what the API sees are the same transaction.
    """

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass  # db_session fixture owns closing/rollback

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
