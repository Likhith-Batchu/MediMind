
from pathlib import Path

import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException

from app.schemas.liver_risk import LiverRiskRequest

router = APIRouter(prefix="/ai", tags=["AI - Experimental"])

MODEL_PATH = Path("/app/ai_models/random_forest.joblib")


@router.post("/liver-risk")
def predict_liver_risk(request: LiverRiskRequest):
    try:
        model = joblib.load(MODEL_PATH)

        features = pd.DataFrame([request.model_features()])

        prediction = int(model.predict(features)[0])
        probabilities = model.predict_proba(features)[0]

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Experimental model artifact is unavailable.",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Experimental inference failed.",
        )

    return {
        "model": "Random Forest",
        "experimental_output": (
            "liver-disease class"
            if prediction == 1
            else "non-liver class"
        ),
        "class_id": prediction,
        "class_probability": {
            "non_liver_class": round(float(probabilities[0]), 4),
            "liver_disease_class": round(float(probabilities[1]), 4),
        },
        "notice": (
            "Research prototype only. Not clinically validated. "
            "This output is not a diagnosis or treatment recommendation."
        ),
    }
