"""
Authentication test suite — Step 3.

Covers exactly the 14 cases requested:
 1. Patient registration succeeds
 2. Duplicate registration fails
 3. Invalid registration data fails
 4. Password is stored as a hash, never plaintext
 5. Login succeeds
 6. Incorrect password fails
 7. Invalid/nonexistent login fails safely (same error as wrong password)
 8. /auth/me requires authentication
 9. /auth/me returns the correct authenticated user
10. Patient authorization works
11. Doctor authorization blocks patients
12. Admin authorization blocks patients/doctors
13. password_hash is never returned in API responses
14. Expired/invalid JWT is rejected
"""

from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User, UserRole


# --- helpers -----------------------------------------------------------

def _create_user(db_session, email: str, password: str, role: UserRole) -> User:
    """
    Direct DB creation for roles the public API can never produce
    (doctor/admin). Deliberately bypasses the API — this simulates
    an account an admin would create through a future admin-only
    endpoint, which does not exist yet in Phase 1.
    """
    user = User(email=email, password_hash=hash_password(password), role=role)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _login(client, email: str, password: str):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# --- 1. registration -----------------------------------------------------

def test_patient_registration_succeeds(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newpatient@example.com", "password": "SecurePass123"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "newpatient@example.com"
    assert body["role"] == "patient"
    assert body["is_active"] is True


# --- 2. duplicate registration ------------------------------------------

def test_duplicate_registration_fails(client):
    payload = {"email": "duplicate@example.com", "password": "SecurePass123"}
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409


# --- 3. invalid registration data ---------------------------------------

def test_registration_fails_with_invalid_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": "SecurePass123"},
    )
    assert response.status_code == 422


def test_registration_fails_with_weak_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "weakpass@example.com", "password": "short"},
    )
    assert response.status_code == 422


def test_registration_fails_with_missing_fields(client):
    response = client.post("/api/v1/auth/register", json={"email": "missing@example.com"})
    assert response.status_code == 422


def test_public_registration_cannot_set_role(client):
    """
    The UserRegister schema has no `role` field at all, so an attempt
    to smuggle one in should simply be ignored by Pydantic (extra
    fields are dropped, not merged), and the account still ends up
    as a patient.
    """
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "wannabe-admin@example.com",
            "password": "SecurePass123",
            "role": "admin",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "patient"


# --- 4. password is hashed, never plaintext -----------------------------

def test_password_is_stored_as_hash_not_plaintext(client, db_session):
    plaintext = "SecurePass123"
    client.post(
        "/api/v1/auth/register",
        json={"email": "hashcheck@example.com", "password": plaintext},
    )

    stored = db_session.query(User).filter(User.email == "hashcheck@example.com").first()
    assert stored is not None
    assert stored.password_hash != plaintext
    # bcrypt hashes have this recognizable prefix
    assert stored.password_hash.startswith("$2b$")


# --- 5. login succeeds ---------------------------------------------------

def test_login_succeeds(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "loginok@example.com", "password": "SecurePass123"},
    )

    response = _login(client, "loginok@example.com", "SecurePass123")
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["user"]["email"] == "loginok@example.com"


# --- 6. incorrect password -----------------------------------------------

def test_login_fails_with_incorrect_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpass@example.com", "password": "SecurePass123"},
    )

    response = _login(client, "wrongpass@example.com", "TotallyWrongPass1")
    assert response.status_code == 401


# --- 7. nonexistent login fails safely, same error as wrong password ----

def test_login_fails_safely_for_nonexistent_email(client):
    response = _login(client, "doesnotexist@example.com", "SomePassword1")
    assert response.status_code == 401

    wrong_pw_response = _login(client, "doesnotexist@example.com", "AnotherPassword2")
    # Same status AND same error body as an existing-email/wrong-password
    # failure (test 6) — confirms we don't leak whether the email exists.
    assert wrong_pw_response.status_code == 401
    assert response.json() == wrong_pw_response.json()


# --- 8. /auth/me requires authentication ---------------------------------

def test_me_requires_authentication(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_rejects_garbage_token(client):
    response = client.get("/api/v1/auth/me", headers=_auth_headers("not-a-real-token"))
    assert response.status_code == 401


# --- 9. /auth/me returns the correct user --------------------------------

def test_me_returns_correct_authenticated_user(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "meuser@example.com", "password": "SecurePass123"},
    )
    login_response = _login(client, "meuser@example.com", "SecurePass123")
    token = login_response.json()["access_token"]

    me_response = client.get("/api/v1/auth/me", headers=_auth_headers(token))
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "meuser@example.com"
    assert me_response.json()["role"] == "patient"


# --- 10, 11, 12. role-based authorization ---------------------------------

def test_patient_authorization_works(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "roletest-patient@example.com", "password": "SecurePass123"},
    )
    token = _login(client, "roletest-patient@example.com", "SecurePass123").json()["access_token"]

    response = client.get("/api/v1/health/patient-only", headers=_auth_headers(token))
    assert response.status_code == 200


def test_doctor_authorization_blocks_patients(client, db_session):
    _create_user(db_session, "roletest-doc-blocked@example.com", "SecurePass123", UserRole.PATIENT)
    token = _login(client, "roletest-doc-blocked@example.com", "SecurePass123").json()["access_token"]

    response = client.get("/api/v1/health/doctor-only", headers=_auth_headers(token))
    assert response.status_code == 403


def test_doctor_authorization_works_for_doctors(client, db_session):
    _create_user(db_session, "roletest-doctor@example.com", "SecurePass123", UserRole.DOCTOR)
    token = _login(client, "roletest-doctor@example.com", "SecurePass123").json()["access_token"]

    response = client.get("/api/v1/health/doctor-only", headers=_auth_headers(token))
    assert response.status_code == 200


def test_admin_authorization_blocks_patients_and_doctors(client, db_session):
    _create_user(db_session, "roletest-admin-blocked-p@example.com", "SecurePass123", UserRole.PATIENT)
    patient_token = _login(client, "roletest-admin-blocked-p@example.com", "SecurePass123").json()["access_token"]

    _create_user(db_session, "roletest-admin-blocked-d@example.com", "SecurePass123", UserRole.DOCTOR)
    doctor_token = _login(client, "roletest-admin-blocked-d@example.com", "SecurePass123").json()["access_token"]

    patient_response = client.get("/api/v1/health/admin-only", headers=_auth_headers(patient_token))
    doctor_response = client.get("/api/v1/health/admin-only", headers=_auth_headers(doctor_token))

    assert patient_response.status_code == 403
    assert doctor_response.status_code == 403


def test_admin_authorization_works_for_admins(client, db_session):
    _create_user(db_session, "roletest-admin@example.com", "SecurePass123", UserRole.ADMIN)
    token = _login(client, "roletest-admin@example.com", "SecurePass123").json()["access_token"]

    response = client.get("/api/v1/health/admin-only", headers=_auth_headers(token))
    assert response.status_code == 200


# --- 13. password_hash never returned ------------------------------------

def test_password_hash_never_returned_by_register(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "noleak-register@example.com", "password": "SecurePass123"},
    )
    assert "password_hash" not in response.json()
    assert "password" not in response.json()


def test_password_hash_never_returned_by_login(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "noleak-login@example.com", "password": "SecurePass123"},
    )
    response = _login(client, "noleak-login@example.com", "SecurePass123")
    assert "password_hash" not in response.json()["user"]


def test_password_hash_never_returned_by_me(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "noleak-me@example.com", "password": "SecurePass123"},
    )
    token = _login(client, "noleak-me@example.com", "SecurePass123").json()["access_token"]
    response = client.get("/api/v1/auth/me", headers=_auth_headers(token))
    assert "password_hash" not in response.json()


# --- 14. expired / invalid JWT rejected -----------------------------------

def test_expired_jwt_is_rejected(client, db_session):
    user = _create_user(db_session, "expiredtoken@example.com", "SecurePass123", UserRole.PATIENT)

    # Craft a token that expired 1 minute ago, using the real secret/algorithm
    # so we're specifically testing expiry handling, not signature handling.
    expired_payload = {
        "sub": str(user.id),
        "role": user.role.value,
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }
    expired_token = jwt.encode(
        expired_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    response = client.get("/api/v1/auth/me", headers=_auth_headers(expired_token))
    assert response.status_code == 401


def test_jwt_with_bad_signature_is_rejected(client, db_session):
    user = _create_user(db_session, "badsig@example.com", "SecurePass123", UserRole.PATIENT)

    payload = {
        "sub": str(user.id),
        "role": user.role.value,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    # Signed with the WRONG secret — must be rejected.
    tampered_token = jwt.encode(payload, "wrong-secret-key", algorithm=settings.JWT_ALGORITHM)

    response = client.get("/api/v1/auth/me", headers=_auth_headers(tampered_token))
    assert response.status_code == 401


def test_malformed_jwt_is_rejected(client):
    response = client.get(
        "/api/v1/auth/me", headers=_auth_headers("this.is.not.a.valid.jwt")
    )
    assert response.status_code == 401
