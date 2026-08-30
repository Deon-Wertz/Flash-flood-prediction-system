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
# Load verified flood events
events = pd.read_csv("Data/flood_events.csv")

# Remove "hrs" and clean the date text
events["Date"] = events["Date"].str.replace(" hrs", "", regex=False)

# Insert colon into times like 0138 -> 01:38
events["Date"] = events["Date"].str.replace(
    r"(\d{2}\.\d{2}\.\d{4}) (\d{2})(\d{2})",
    r"\1 \2:\3",
    regex=True
)

# Convert to datetime
# Convert flood event dates
events["Date"] = events["Date"].astype(str)

# Extract the first date from ranges
events["Date"] = events["Date"].str.replace(
    r"^(\d{1,2})-(\d{1,2}\.\d{1,2}\.\d{4})$",
    r"\1.\2",
    regex=True
)

# Convert dates safely
events["Date"] = pd.to_datetime(
    events["Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

# Remove rows where the date could not be understood
events = events.dropna(subset=["Date"])

print("\nVerified flood events:")
print(events)

print("\nVerified flood events:")
print(events)

# ==============================
# CREATE FLOOD LABELS
# ==============================

combined_df["flood"] = 0

for _, event in events.iterrows():

    event_date = event["Date"]

    # Skip invalid dates
    if pd.isna(event_date):
        continue

    # Label the entire event day
    start_time = event_date.normalize()
    end_time = start_time + pd.Timedelta(days=1)

    mask = (
        (combined_df["time"] >= start_time) &
        (combined_df["time"] < end_time)
    )

    combined_df.loc[mask, "flood"] = 1


# ==============================
# CHECK LABEL DISTRIBUTION
# ==============================

print("\nFlood label distribution:")
print(combined_df["flood"].value_counts())


# Show some flood-labelled rows
print("\nFlood event rows:")
print(
    combined_df[combined_df["flood"] == 1]
    .sort_values("time")
    .head(30)
)


# ==============================
# SAVE FINAL TRAINING DATA
# ==============================

combined_df.to_csv(
    "Data/flood_training_data.csv",
    index=False
)

print("\n🔥 FLOOD TRAINING DATA CREATED SUCCESSFULLY!")