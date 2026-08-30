import pandas as pd
import joblib

# ==============================
# LOAD TRAINED MODEL
# ==============================

model = joblib.load("flood_model.pkl")

FINAL_THRESHOLD = 0.30

print("🔥 FLOOD PREDICTION SYSTEM READY!")

# ==============================
# ENTER RAINFALL DATA
# ==============================

rainfall_mm_hr = float(input("Rainfall intensity (mm/hr): "))
rainfall_mm = float(input("Rainfall amount (mm): "))
rainfall_1hr = float(input("Rainfall in last 1 hour (mm): "))
rainfall_3hr = float(input("Rainfall in last 3 hours (mm): "))
rainfall_6hr = float(input("Rainfall in last 6 hours (mm): "))
rainfall_24hr = float(input("Rainfall in last 24 hours (mm): "))

# ==============================
# CREATE INPUT DATA
# ==============================

input_data = pd.DataFrame([{
    "rainfall_mm_hr": rainfall_mm_hr,
    "rainfall_mm": rainfall_mm,
    "rainfall_1hr": rainfall_1hr,
    "rainfall_3hr": rainfall_3hr,
    "rainfall_6hr": rainfall_6hr,
    "rainfall_24hr": rainfall_24hr
}])

# ==============================
# PREDICT FLOOD PROBABILITY
# ==============================

probability = model.predict_proba(input_data)[0][1]

prediction = int(probability >= FINAL_THRESHOLD)

# ==============================
# SHOW RESULT
# ==============================

print("\n==============================")
print("       FLOOD RISK RESULT")
print("==============================")

print(f"Flood Probability: {probability * 100:.2f}%")

if prediction == 1:
    print("⚠️ HIGH FLOOD RISK!")
else:
    print("✅ LOW FLOOD RISK")

print("==============================")