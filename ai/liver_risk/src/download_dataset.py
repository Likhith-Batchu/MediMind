from ucimlrepo import fetch_ucirepo
from pathlib import Path

# Fetch ILPD from UCI
dataset = fetch_ucirepo(id=225)

# Get features and target
X = dataset.data.features
y = dataset.data.targets

# Combine into one dataframe
df = X.copy()
df["Selector"] = y.iloc[:, 0]

# Create data directory
data_dir = Path(__file__).resolve().parent.parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)

# Save raw dataset
output_path = data_dir / "ilpd_raw.csv"
df.to_csv(output_path, index=False)

print("Dataset downloaded successfully!")
print(f"Saved to: {output_path}")
print(f"Shape: {df.shape}")
print("\nColumns:")
print(df.columns.tolist())