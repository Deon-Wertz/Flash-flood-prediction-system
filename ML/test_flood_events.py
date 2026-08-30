import pandas as pd
import joblib

# Load data
df = pd.read_csv("Data/flood_training_data.csv")

# Load model
model = joblib.load("flood_model.pkl")

features = [
    "rainfall_mm_hr",
    "rainfall_mm",
    "rainfall_1hr",
    "rainfall_3hr",
    "rainfall_6hr",
    "rainfall_24hr"
]

# Get only known flood rows
flood_rows = df[df["flood"] == 1].copy()

# Calculate probabilities
flood_rows["probability"] = model.predict_proba(
    flood_rows[features]
)[:, 1]

# Sort by probability
flood_rows = flood_rows.sort_values(
    "probability",
    ascending=False
)

print("\nTOP 20 KNOWN FLOOD ROWS\n")

print(
    flood_rows[
        [
            "time",
            "rainfall_mm_hr",
            "rainfall_1hr",
            "rainfall_3hr",
            "rainfall_6hr",
            "rainfall_24hr",
            "probability"
        ]
    ].head(20)
)

print("\nAverage flood probability:")
print(flood_rows["probability"].mean())

print("\nMaximum flood probability:")
print(flood_rows["probability"].max())

print("\nMinimum flood probability:")
print(flood_rows["probability"].min())