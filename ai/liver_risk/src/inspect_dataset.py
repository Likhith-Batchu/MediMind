import pandas as pd
from pathlib import Path

# Locate dataset
data_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ilpd_raw.csv"
)

df = pd.read_csv(data_path)

print("=" * 60)
print("MEDIMIND AI - ILPD DATASET INSPECTION")
print("=" * 60)

print("\n1. Shape")
print(df.shape)

print("\n2. First 5 rows")
print(df.head())

print("\n3. Dataset information")
print(df.info())

print("\n4. Statistical summary")
print(df.describe())

print("\n5. Missing values")
print(df.isnull().sum())

print("\n6. Duplicate rows")
print(df.duplicated().sum())

print("\n7. Target distribution")
print(df["Selector"].value_counts())

print("\n8. Target percentages")
print(df["Selector"].value_counts(normalize=True) * 100)

print("\n9. Gender distribution")
print(df["Gender"].value_counts())

print("\n10. Data types")
print(df.dtypes)