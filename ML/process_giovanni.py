import pandas as pd
import os
import sys

# ==============================
# GET INPUT FROM TERMINAL
# ==============================

if len(sys.argv) != 3:
    print("\nUsage:")
    print("python process_giovanni.py <filename> <flood_date>")
    print("\nExample:")
    print("python process_giovanni.py event_2025_05_24_kullu.csv 2025-05-24")
    sys.exit()

filename = sys.argv[1]
flood_date = sys.argv[2]

# ==============================
# FILE PATH
# ==============================

file_path = os.path.join(
    "..",
    "Data",
    "raw_giovanni",
    filename
)

# Check if file exists
if not os.path.exists(file_path):
    print(f"\n❌ File not found: {file_path}")
    sys.exit()

# ==============================
# LOAD GIOVANNI CSV
# ==============================

with open(file_path, "r") as file:
    lines = file.readlines()

# Find where the actual CSV header starts
header_row = None

for i, line in enumerate(lines):
    if line.startswith("time,"):
        header_row = i
        break

if header_row is None:
    raise ValueError("❌ Could not find the data header!")

# Load actual data
df = pd.read_csv(
    file_path,
    skiprows=header_row
)

# ==============================
# CLEAN COLUMNS
# ==============================

df["time"] = pd.to_datetime(df["time"])

# Rename rainfall column
rainfall_column = df.columns[1]

df = df.rename(columns={
    rainfall_column: "rainfall_mm_hr"
})

# Convert rainfall to numeric
df["rainfall_mm_hr"] = pd.to_numeric(
    df["rainfall_mm_hr"],
    errors="coerce"
)

# Remove missing values
df = df.dropna()

# ==============================
# CALCULATE RAINFALL FEATURES
# ==============================

# Giovanni data is every 30 minutes

# Rainfall amount during one 30-minute period
df["rainfall_mm"] = df["rainfall_mm_hr"] * 0.5

# Rainfall in previous 1 hour
df["rainfall_1hr"] = (
    df["rainfall_mm"].rolling(2).sum()
)

# Rainfall in previous 3 hours
df["rainfall_3hr"] = (
    df["rainfall_mm"].rolling(6).sum()
)

# Rainfall in previous 6 hours
df["rainfall_6hr"] = (
    df["rainfall_mm"].rolling(12).sum()
)

# Rainfall in previous 24 hours
df["rainfall_24hr"] = (
    df["rainfall_mm"].rolling(48).sum()
)

# Remove rows created with NaN from rolling windows
df = df.dropna()

# ==============================
# ADD FLOOD LABEL
# ==============================

# Default = no flood
df["flood"] = 0

# Convert terminal date into timestamp
flood_start = pd.Timestamp(flood_date)

# Flood date ends at 23:59:59
flood_end = (
    flood_start
    + pd.Timedelta(days=1)
    - pd.Timedelta(seconds=1)
)

# Mark flood event rows as 1
df.loc[
    (df["time"] >= flood_start) &
    (df["time"] <= flood_end),
    "flood"
] = 1

# ==============================
# CREATE OUTPUT NAME AUTOMATICALLY
# ==============================

# Remove .csv from filename
base_name = os.path.splitext(filename)[0]

# Create processed filename automatically
output_filename = f"processed_{base_name}.csv"

output_path = os.path.join(
    "..",
    "Data",
    output_filename
)

# ==============================
# SAVE DATA
# ==============================

df.to_csv(output_path, index=False)

# ==============================
# SHOW RESULTS
# ==============================

print("\n🔥 PROCESSING COMPLETE!")

print("\nInput file:")
print(filename)

print("\nFlood date:")
print(flood_date)

print("\nTotal rows:", len(df))

print(
    "Flood rows:",
    (df["flood"] == 1).sum()
)

print(
    "Non-flood rows:",
    (df["flood"] == 0).sum()
)

print("\nFirst rows:")
print(df.head())

print(f"\n🔥 Saved to: {output_path}")