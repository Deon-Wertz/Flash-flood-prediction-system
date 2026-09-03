import pandas as pd
import joblib

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv("../Data/flood_training_data.csv")

df["time"] = pd.to_datetime(df["time"])

# ==============================
# LOAD MODEL
# ==============================

model = joblib.load("../Models/flood_model.pkl")

print("🔥 MODEL LOADED SUCCESSFULLY!")
# SELECT FEATURES
# ==============================

features = [
    "rainfall_mm_hr",
    "rainfall_mm",
    "rainfall_1hr",
    "rainfall_3hr",
    "rainfall_6hr",
    "rainfall_24hr"
]

# ==============================
# GET FLOOD PROBABILITIES
# ==============================

df["probability"] = model.predict_proba(df[features])[:, 1]

# ==============================
# LOOK ONLY AT 2025 FLOOD EVENTS
# ==============================

floods_2025 = df[
    (df["flood"] == 1) &
    (df["time"].dt.year == 2025)
].copy()

print("\n🔥 2025 VERIFIED FLOOD EVENTS")
print("Total flood rows:", len(floods_2025))

# ==============================
# PROBABILITY STATISTICS
# ==============================

print("\nProbability statistics:")

print("Average probability:",
      floods_2025["probability"].mean())

print("Maximum probability:",
      floods_2025["probability"].max())

print("Minimum probability:",
      floods_2025["probability"].min())

# ==============================
# THRESHOLD TEST
# ==============================

thresholds = [0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01]

print("\n==============================")
print("2025 FLOOD DETECTION")
print("==============================")

for threshold in thresholds:

    detected = (
        floods_2025["probability"] >= threshold
    ).sum()

    missed = (
        floods_2025["probability"] < threshold
    ).sum()

    print(f"\nThreshold: {threshold}")
    print("Detected:", detected)
    print("Missed:", missed)

# ==============================
# SHOW LOWEST PROBABILITY FLOODS
# ==============================

print("\n==============================")
print("FLOODS THE MODEL MISSES")
print("==============================")

missed_floods = floods_2025.sort_values(
    "probability"
)

print(
    missed_floods[
        [
            "time",
            "rainfall_mm_hr",
            "rainfall_1hr",
            "rainfall_3hr",
            "rainfall_6hr",
            "rainfall_24hr",
            "probability"
        ]
    ].head(30)
)

print("\n🔥 ANALYSIS COMPLETE!")