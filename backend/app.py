import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# ==============================
# CREATE FLASK APP
# ==============================

app = Flask(__name__)


# ==============================
# LOAD TRAINED MODEL
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "Models",
    "flood_model.pkl"
)

model = joblib.load(MODEL_PATH)

print("🔥 Flood model loaded successfully!")


# ==============================
# HOME ROUTE
# ==============================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Flash Flood Prediction API is running!",
        "status": "online"
    })


# ==============================
# HEALTH CHECK
# ==============================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "model": "flood_model.pkl",
        "features": [
            "rainfall_mm_hr",
            "rainfall_mm",
            "rainfall_1hr",
            "rainfall_3hr",
            "rainfall_6hr",
            "rainfall_24hr"
        ]
    })


# ==============================
# PREDICTION API
# ==============================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get JSON data
        data = request.get_json()

        # Check if JSON exists
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400


        # Required features
        features = [
            "rainfall_mm_hr",
            "rainfall_mm",
            "rainfall_1hr",
            "rainfall_3hr",
            "rainfall_6hr",
            "rainfall_24hr"
        ]


        # Check missing features
        missing_features = []

        for feature in features:

            if feature not in data:
                missing_features.append(feature)


        if missing_features:

            return jsonify({
                "error": "Missing required rainfall data",
                "missing_features": missing_features
            }), 400


        # Create DataFrame for ML model
        input_data = pd.DataFrame([{
            "rainfall_mm_hr": float(data["rainfall_mm_hr"]),
            "rainfall_mm": float(data["rainfall_mm"]),
            "rainfall_1hr": float(data["rainfall_1hr"]),
            "rainfall_3hr": float(data["rainfall_3hr"]),
            "rainfall_6hr": float(data["rainfall_6hr"]),
            "rainfall_24hr": float(data["rainfall_24hr"])
        }])


        # Get flood probability
        probability = model.predict_proba(
            input_data
        )[0][1]


        # ==============================
        # DETERMINE RISK LEVEL
        # ==============================

        if probability < 0.10:

            risk_level = "LOW"

        elif probability < 0.30:

            risk_level = "MODERATE"

        elif probability < 0.60:

            risk_level = "HIGH"

        else:

            risk_level = "SEVERE"


        # ==============================
        # RETURN RESULT
        # ==============================

        return jsonify({

            "flood_probability": round(
                float(probability * 100),
                2
            ),

            "risk_level": risk_level,

            "status": "success"

        })


    except ValueError:

        return jsonify({
            "error": "Rainfall values must be numbers"
        }), 400


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==============================
# START SERVER
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )