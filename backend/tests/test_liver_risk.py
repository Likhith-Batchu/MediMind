
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.routes import liver_risk

client = TestClient(app)

VALID_PAYLOAD = {
    "Age": 45,
    "Gender": "Male",
    "TB": 1.0,
    "DB": 0.3,
    "Alkphos": 200,
    "Sgpt": 30,
    "Sgot": 35,
    "TP": 6.8,
    "ALB": 3.5,
    "A_G_Ratio": 1.0,
}


def test_liver_risk_valid_request():
    response = client.post("/api/v1/ai/liver-risk", json=VALID_PAYLOAD)

    assert response.status_code == 200
    data = response.json()

    assert data["model"] == "Random Forest"
    assert data["class_id"] in (0, 1)
    assert data["experimental_output"] in (
        "liver-disease class",
        "non-liver class",
    )
    assert set(data["class_probability"]) == {
        "non_liver_class",
        "liver_disease_class",
    }
    assert "not clinically validated" in data["notice"].lower()

    scores = data["class_probability"]
    assert 0 <= scores["non_liver_class"] <= 1
    assert 0 <= scores["liver_disease_class"] <= 1


def test_liver_risk_missing_required_field():
    payload = VALID_PAYLOAD.copy()
    payload.pop("Age")

    response = client.post("/api/v1/ai/liver-risk", json=payload)

    assert response.status_code == 422


def test_liver_risk_invalid_gender():
    payload = VALID_PAYLOAD.copy()
    payload["Gender"] = "Unknown"

    response = client.post("/api/v1/ai/liver-risk", json=payload)

    assert response.status_code == 422


def test_liver_risk_rejects_extra_fields():
    payload = VALID_PAYLOAD.copy()
    payload["unexpected_field"] = 123

    response = client.post("/api/v1/ai/liver-risk", json=payload)

    assert response.status_code == 422


def test_liver_risk_missing_model_returns_503():
    with patch.object(
        liver_risk,
        "MODEL_PATH",
        liver_risk.MODEL_PATH.parent / "missing-model.joblib",
    ):
        response = client.post(
            "/api/v1/ai/liver-risk",
            json=VALID_PAYLOAD,
        )

    assert response.status_code == 503
