import pandas as pd

# Load training data
df = pd.read_csv("Data/flood_training_data.csv")

# Convert time
df["time"] = pd.to_datetime(df["time"])

# Separate flood rows
floods = df[df["flood"] == 1].copy()

# Separate periods
training_floods = floods[floods["time"].dt.year < 2025]
test_floods = floods[floods["time"].dt.year == 2025]

features = [
    "rainfall_mm_hr",
    "rainfall_mm",
    "rainfall_1hr",
    "rainfall_3hr",
    "rainfall_6hr",
    "rainfall_24hr"
]

print("\n🔥 FLOOD DATA COMPARISON")

print("\n================ TRAINING FLOODS (Before 2025) ================")
print(training_floods[features].describe())

print("\n================ 2025 FLOODS ================")
print(test_floods[features].describe())

print("\nFlood rows before 2025:", len(training_floods))
print("Flood rows in 2025:", len(test_floods))