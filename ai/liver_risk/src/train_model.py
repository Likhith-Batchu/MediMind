
import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# --------------------------------------------------
# 1. PATHS AND CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ilpd_raw.csv"
MODEL_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.20

NUMERIC_FEATURES = [
    "Age", "TB", "DB", "Alkphos", "Sgpt",
    "Sgot", "TP", "ALB", "A/G Ratio",
]
CATEGORICAL_FEATURES = ["Gender"]


# --------------------------------------------------
# 2. LOAD AND VALIDATE DATA
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

required_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES + ["Selector"]

if not set(required_columns).issubset(df.columns):
    raise ValueError("Dataset is missing required columns.")

if df["Selector"].isna().any():
    raise ValueError("Target contains missing values.")

if not set(df["Selector"].unique()).issubset({1, 2}):
    raise ValueError("Unexpected target labels found.")

print("=" * 65)
print("MEDIMIND AI - LIVER RISK MODEL EXPERIMENT")
print("=" * 65)

print(f"\nOriginal dataset shape: {df.shape}")

# Remove exact duplicate records before splitting to reduce leakage risk.
duplicate_count = int(df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)

print(f"Exact duplicate rows removed: {duplicate_count}")
print(f"Dataset shape after deduplication: {df.shape}")

# ILPD label mapping: 1 = liver patient, 2 = non-liver patient.
# Encode liver disease as the positive class (1).
y = (df["Selector"] == 1).astype(int)
X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()

print("\nTarget distribution (1 = liver disease, 0 = non-liver):")
print(y.value_counts().sort_index())

# --------------------------------------------------
# 3. STRATIFIED TRAIN/TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)

print(f"\nTraining records: {len(X_train)}")
print(f"Test records: {len(X_test)}")


# --------------------------------------------------
# 4. PREPROCESSING PIPELINES
# --------------------------------------------------

numeric_preprocessing = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_preprocessing = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_preprocessing, NUMERIC_FEATURES),
    ("categorical", categorical_preprocessing, CATEGORICAL_FEATURES),
])


# --------------------------------------------------
# 5. DEFINE MODELS
# --------------------------------------------------

models = {
    "Logistic Regression": LogisticRegression(
        class_weight="balanced",
        max_iter=2000,
        random_state=RANDOM_STATE,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        min_samples_leaf=2,
    ),
}


# --------------------------------------------------
# 6. TRAIN AND EVALUATE
# --------------------------------------------------

results = []
fitted_models = {}

for name, estimator in models.items():
    print(f"\n{'-' * 65}")
    print(f"Training: {name}")

    pipeline = Pipeline([
        ("preprocessing", preprocessor),
        ("model", estimator),
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "model": name,
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "f1": f1_score(
            y_test, predictions, zero_division=0
        ),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    results.append(metrics)
    fitted_models[name] = pipeline

    print("\nMetrics:")
    for metric, value in metrics.items():
        if metric != "model":
            print(f"{metric:12s}: {value:.4f}")

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, predictions, labels=[0, 1]))

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Non-liver", "Liver disease"],
            zero_division=0,
        )
    )


# --------------------------------------------------
# 7. SAVE COMPARISON RESULTS
# --------------------------------------------------

results_df = pd.DataFrame(results)
results_df.to_csv(RESULTS_DIR / "model_comparison.csv", index=False)

print("\nMODEL COMPARISON")
print(results_df.to_string(index=False))


# --------------------------------------------------
# 8. SAVE EXPERIMENT METADATA
# --------------------------------------------------

metadata = {
    "dataset": "UCI Indian Liver Patient Dataset",
    "random_state": RANDOM_STATE,
    "test_size": TEST_SIZE,
    "duplicate_rows_removed": duplicate_count,
    "training_records": len(X_train),
    "test_records": len(X_test),
    "positive_class": "Selector == 1 (liver patient)",
    "features": NUMERIC_FEATURES + CATEGORICAL_FEATURES,
    "warning": (
        "Research prototype only. Not clinically validated; "
        "not intended for diagnosis or treatment."
    ),
}

with open(RESULTS_DIR / "experiment_metadata.json", "w") as file:
    json.dump(metadata, file, indent=2)


# --------------------------------------------------
# 9. SAVE BOTH TRAINED PIPELINES
# --------------------------------------------------

for name, pipeline in fitted_models.items():
    filename = name.lower().replace(" ", "_") + ".joblib"
    joblib.dump(pipeline, MODEL_DIR / filename)
    print(f"Saved model: {MODEL_DIR / filename}")

print(f"\nResults saved in: {RESULTS_DIR}")
print("\nExperiment complete.")
