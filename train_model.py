import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# ==============================
# LOAD TRAINING DATA
# ==============================

df = pd.read_csv("Data/flood_training_data.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# ==============================
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

X = df[features]
y = df["flood"]

# ==============================
# TRAIN / TEST SPLIT
# ==============================
# ==============================
# TIME-BASED TRAIN / TEST SPLIT
# ==============================

# Make sure time is datetime
df["time"] = pd.to_datetime(df["time"])

# Train on older data
train_df = df[df["time"] < "2025-01-01"]

# Test on newer unseen data
test_df = df[df["time"] >= "2025-01-01"]

X_train = train_df[features]
y_train = train_df["flood"]

X_test = test_df[features]
y_test = test_df["flood"]

print("\nTIME-BASED TRAIN / TEST SPLIT")
print("Training period:", train_df["time"].min(), "to", train_df["time"].max())
print("Testing period:", test_df["time"].min(), "to", test_df["time"].max())

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nTraining floods:", y_train.sum())
print("Testing floods:", y_test.sum())

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# ==============================
# CREATE MODEL
# ==============================

model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

# ==============================
# TRAIN MODEL
# ==============================

print("\nTraining Random Forest model...")

model.fit(X_train, y_train)
# Get flood probabilities
probabilities = model.predict_proba(X_test)[:, 1]

# Test different flood warning thresholds
thresholds = [0.50, 0.40, 0.30, 0.20, 0.10]

print("\nTHRESHOLD COMPARISON")

for threshold in thresholds:

    y_pred = (probabilities >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    print(f"\nThreshold: {threshold}")
    print(f"Floods detected: {tp}")
    print(f"Floods missed: {fn}")
    print(f"False alarms: {fp}")

# ==============================
# MAKE PREDICTIONS
# ==============================

# Get flood probabilities for test data
probabilities = model.predict_proba(X_test)[:, 1]

# Flood warning threshold
threshold = 0.30

# Convert probabilities into predictions
y_pred = (probabilities >= threshold).astype(int)

print("🔥 MODEL TRAINED SUCCESSFULLY!")

# ==============================
# EVALUATE MODEL
# ==============================

print("\nThreshold used:", threshold)

print("\nAccuracy:")
print(accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ==============================
# FEATURE IMPORTANCE
# ==============================

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print("\nFeature Importance:")
print(importance)

# ==============================
# SAVE TRAINED MODEL
# ==============================

joblib.dump(model, "flood_model.pkl")

print("\n🔥 MODEL SAVED SUCCESSFULLY!")
print("Saved as: flood_model.pkl")
print("Flood warning threshold:", threshold)