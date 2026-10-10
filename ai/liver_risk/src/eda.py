import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ============================================================
# 1. LOAD DATA
# ============================================================

data_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ilpd_raw.csv"
)

df = pd.read_csv(data_path)

# Create directory for EDA plots
plot_dir = (
    Path(__file__).resolve().parent.parent
    / "eda_plots"
)

plot_dir.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. BASIC INFORMATION
# ============================================================

print("=" * 70)
print("MEDIMIND AI - EXPLORATORY DATA ANALYSIS")
print("=" * 70)

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ============================================================
# 3. TARGET DISTRIBUTION
# ============================================================

print("\nTarget Distribution:")
print(df["Selector"].value_counts())

print("\nTarget Percentage:")
print(df["Selector"].value_counts(normalize=True) * 100)

plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="Selector"
)

plt.title("Liver Disease Class Distribution")
plt.xlabel("Class")
plt.ylabel("Number of Patients")

plt.tight_layout()

plt.savefig(
    plot_dir / "target_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. GENDER DISTRIBUTION
# ============================================================

plt.figure(figsize=(7, 5))

sns.countplot(
    data=df,
    x="Gender"
)

plt.title("Gender Distribution")
plt.xlabel("Gender")
plt.ylabel("Number of Patients")

plt.tight_layout()

plt.savefig(
    plot_dir / "gender_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. NUMERICAL FEATURE DISTRIBUTIONS
# ============================================================

numerical_features = [
    "Age",
    "TB",
    "DB",
    "Alkphos",
    "Sgpt",
    "Sgot",
    "TP",
    "ALB",
    "A/G Ratio"
]

for feature in numerical_features:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x=feature,
        kde=True
    )

    plt.title(f"Distribution of {feature}")
    plt.xlabel(feature)
    plt.ylabel("Frequency")

    plt.tight_layout()

    safe_name = feature.replace("/", "_").replace(" ", "_")

    plt.savefig(
        plot_dir / f"{safe_name}_distribution.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 6. BOXPLOTS FOR OUTLIER ANALYSIS
# ============================================================

for feature in numerical_features:

    plt.figure(figsize=(8, 4))

    sns.boxplot(
        data=df,
        x=feature
    )

    plt.title(f"Outlier Analysis - {feature}")

    plt.tight_layout()

    safe_name = feature.replace("/", "_").replace(" ", "_")

    plt.savefig(
        plot_dir / f"{safe_name}_boxplot.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 7. CORRELATION MATRIX
# ============================================================

# Encode gender temporarily only for correlation analysis
correlation_df = df.copy()

correlation_df["Gender"] = correlation_df["Gender"].map({
    "Male": 1,
    "Female": 0
})

plt.figure(figsize=(12, 9))

sns.heatmap(
    correlation_df.corr(numeric_only=True),
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title("Feature Correlation Matrix")

plt.tight_layout()

plt.savefig(
    plot_dir / "correlation_matrix.png",
    dpi=300
)

plt.close()


# ============================================================
# 8. FEATURE VS TARGET ANALYSIS
# ============================================================

for feature in numerical_features:

    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="Selector",
        y=feature
    )

    plt.title(f"{feature} vs Liver Disease Class")
    plt.xlabel("Class")
    plt.ylabel(feature)

    plt.tight_layout()

    safe_name = feature.replace("/", "_").replace(" ", "_")

    plt.savefig(
        plot_dir / f"{safe_name}_vs_target.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 9. GENDER VS TARGET
# ============================================================

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="Gender",
    hue="Selector"
)

plt.title("Gender vs Liver Disease Class")
plt.xlabel("Gender")
plt.ylabel("Number of Patients")

plt.tight_layout()

plt.savefig(
    plot_dir / "gender_vs_target.png",
    dpi=300
)

plt.close()


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("EDA COMPLETE")
print("=" * 70)

print(f"\nPlots saved to:")
print(plot_dir)