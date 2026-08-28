import pandas as pd
from pathlib import Path

# Folder containing raw rainfall files
data_folder = Path("Data/raw")

# Find all rainfall CSV files
files = sorted(data_folder.glob("rainfall_*.csv"))

all_data = []

for file in files:
    print(f"Processing: {file.name}")

    # Read NASA Giovanni CSV and skip metadata
    df = pd.read_csv(file, skiprows=8)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert time
    df["time"] = pd.to_datetime(df["time"])

    # Rename precipitation column
    df.rename(
        columns={
            "mean_GPM_3IMERGHH_07_precipitation": "rainfall_mm_hr"
        },
        inplace=True
    )

    # Each record is 30 minutes, so convert mm/hr to mm
    df["rainfall_mm"] = df["rainfall_mm_hr"] * 0.5

    # Rainfall accumulation features
    df["rainfall_1hr"] = df["rainfall_mm"].rolling(2).sum()
    df["rainfall_3hr"] = df["rainfall_mm"].rolling(6).sum()
    df["rainfall_6hr"] = df["rainfall_mm"].rolling(12).sum()
    df["rainfall_24hr"] = df["rainfall_mm"].rolling(48).sum()

    # Remove incomplete rows
    df = df.dropna()

    all_data.append(df)

# Combine all years
combined_df = pd.concat(all_data, ignore_index=True)

# Sort by time
combined_df = combined_df.sort_values("time")

# Save combined dataset
output_file = "Data/processed_rainfall_all.csv"
combined_df.to_csv(output_file, index=False)

print("\n🔥 ALL DATA PROCESSED SUCCESSFULLY!")
print("Files processed:", len(files))
print("Dataset shape:", combined_df.shape)

print("\nFirst 5 rows:")
print(combined_df.head())

print("\nLast 5 rows:")
print(combined_df.tail())

print("\nMissing values:")
print(combined_df.isnull().sum())

print("\nDataset statistics:")
print(combined_df.describe())