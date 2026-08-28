import pandas as pd

# Load the raw rainfall data
df = pd.read_csv("Data/raw/rainfall data.csv", skiprows=8)

# Clean column names
df.columns = df.columns.str.strip()

# Convert time column
df["time"] = pd.to_datetime(df["time"])

# Rename rainfall column
df.rename(
    columns={
        "mean_GPM_3IMERGHH_07_precipitation": "rainfall_mm_hr"
    },
    inplace=True
)

# Convert rainfall rate to rainfall amount for each 30-minute period
df["rainfall_mm"] = df["rainfall_mm_hr"] * 0.5

# Create rainfall accumulation features
df["rainfall_1hr"] = df["rainfall_mm"].rolling(2).sum()
df["rainfall_3hr"] = df["rainfall_mm"].rolling(6).sum()
df["rainfall_6hr"] = df["rainfall_mm"].rolling(12).sum()
df["rainfall_24hr"] = df["rainfall_mm"].rolling(48).sum()

# Remove rows with incomplete rolling windows
df = df.dropna()

# Save processed data
df.to_csv("Data/processed_rainfall.csv", index=False)

print("Cleaned data saved successfully!")
print(df.head())