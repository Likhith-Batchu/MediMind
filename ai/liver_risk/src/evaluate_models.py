
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

BASE = Path(__file__).resolve().parent.parent
df = pd.read_csv(BASE / "data" / "ilpd_raw.csv").drop_duplicates().reset_index(drop=True)

numeric = [
    "Age", "TB", "DB", "Alkphos", "Sgpt",
    "Sgot", "TP", "ALB", "A/G Ratio",
]
categorical = ["Gender"]

X = df[numeric + categorical]
y = (df["Selector"] == 1).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

models = {
    "Logistic Regression": BASE / "models" / "logistic_regression.joblib",
    "Random Forest": BASE / "models" / "random_forest.joblib",
}

results_dir = BASE / "results"
plots_dir = results_dir / "evaluation_plots"
plots_dir.mkdir(parents=True, exist_ok=True)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scoring = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1",
    "roc_auc": "roc_auc",
}

summary = []
plt.figure(figsize=(8, 6))

for name, path in models.items():
    model = joblib.load(path)

    # Cross-validation uses training data only.
    cv_scores = cross_validate(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,
        return_train_score=False,
        n_jobs=-1,
    )

    row = {"model": name}
    print(f"\n{'=' * 55}\n{name}")
    print("5-fold cross-validation on training data:")

    for metric in scoring:
        values = cv_scores[f"test_{metric}"]
        row[f"cv_{metric}_mean"] = values.mean()
        row[f"cv_{metric}_std"] = values.std()
        print(f"{metric:10s}: {values.mean():.4f} ± {values.std():.4f}")

    # Evaluate the already-fitted model on the untouched holdout.
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    row.update({
        "holdout_accuracy": accuracy_score(y_test, predictions),
        "holdout_precision": precision_score(y_test, predictions, zero_division=0),
        "holdout_recall": recall_score(y_test, predictions, zero_division=0),
        "holdout_f1": f1_score(y_test, predictions, zero_division=0),
        "holdout_roc_auc": roc_auc_score(y_test, probabilities),
    })
    summary.append(row)

    print("\nHoldout metrics:")
    for metric in ["accuracy", "precision", "recall", "f1", "roc_auc"]:
        print(f"{metric:10s}: {row[f'holdout_{metric}']:.4f}")

    # Confusion matrix
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(
        y_test,
        predictions,
        labels=[0, 1],
        display_labels=["Non-liver", "Liver disease"],
        ax=ax,
        colorbar=False,
    )
    ax.set_title(f"{name} — Holdout Confusion Matrix")
    fig.tight_layout()
    fig.savefig(
        plots_dir / f"{name.lower().replace(' ', '_')}_confusion_matrix.png",
        dpi=200,
    )
    plt.close(fig)

    # ROC curve
    RocCurveDisplay.from_predictions(
        y_test, probabilities, name=name
    )

plt.plot([0, 1], [0, 1], linestyle="--", label="Chance baseline")
plt.title("ROC Curves — Holdout Test Set")
plt.tight_layout()
plt.legend()
plt.savefig(plots_dir / "roc_curves.png", dpi=200)
plt.close()

summary_df = pd.DataFrame(summary)
summary_df.to_csv(results_dir / "validated_model_comparison.csv", index=False)

print("\nSaved cross-validation and holdout results to:")
print(results_dir / "validated_model_comparison.csv")
print(f"\nSaved evaluation plots to:\n{plots_dir}")
