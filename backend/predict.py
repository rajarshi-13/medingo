"""
===========================================================
Medingo Prediction Engine
===========================================================

Predicts Tomorrow's Patient Footfall
using the trained XGBoost model.
"""

import joblib
import pandas as pd


# ==========================================================
# Load Artifacts
# ==========================================================

print("Loading AI Model...")

model = joblib.load("patient_forecast_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
feature_columns = joblib.load("feature_columns.pkl")

print("Model Loaded Successfully!\n")


# ==========================================================
# Load Dataset
# ==========================================================

dataset = pd.read_csv("simulation/dataset.csv")


# ==========================================================
# Get Latest PHC Record
# ==========================================================

def get_latest_record(phc_id):

    phc = dataset[dataset["phc_id"] == phc_id]

    phc = phc.sort_values("date")

    return phc.iloc[-1].copy()


# ==========================================================
# Prepare Features
# ==========================================================

def prepare_features(record):

    record = record.copy()

    drop_columns = [

        "patients_tomorrow",
        "holiday_name",
        "festival_name",
        "month_name",
        "season",
        "date",
        "phc_id"

    ]

    record = record.drop(labels=drop_columns)

    # Encode categorical columns
    for column, encoder in label_encoders.items():

        record[column] = encoder.transform(
            [record[column]]
        )[0]

    # Maintain exact feature order used during training
    record = record[feature_columns]

    return pd.DataFrame([record])


# ==========================================================
# Predict Tomorrow
# ==========================================================

def predict_tomorrow(phc_id):

    latest = get_latest_record(phc_id)

    features = prepare_features(latest)

    prediction = model.predict(features)[0]

    doctor_capacity = int(latest["doctors"] * 45)

    predicted_patients = min(
        int(round(prediction)),
        doctor_capacity
    )

    # Medicine Estimation
    paracetamol_needed = int(predicted_patients * 0.70)

    amoxicillin_needed = int(predicted_patients * 0.18)

    total_medicine = paracetamol_needed + amoxicillin_needed

    remaining_stock = max(
        0,
        int(latest["stock_remaining"] - total_medicine)
    )

    # Doctor Utilization
    doctor_utilization = round(

        (predicted_patients / doctor_capacity) * 100,

        1

    )

    # Alerts
    alerts = []

    if remaining_stock < 1000:
        alerts.append("Medicine Stock Getting Low")

    if remaining_stock < 600:
        alerts.append("Urgent Stock Refill Needed")

    if predicted_patients > 120:
        alerts.append("High OPD Load Expected")

    if latest["viral_pressure"] > 50:
        alerts.append("Possible Viral Outbreak")

    if latest["aqi"] > 170:
        alerts.append("Poor Air Quality")

    if len(alerts) == 0:
        alerts.append("Operations Normal")


    risk_score = 0

    # Doctor utilization contributes up to 50 points
    risk_score += min(50, doctor_utilization * 0.5)

    # Medicine stock contributes up to 30 points
    if remaining_stock < 1000:
         risk_score += 15

    if remaining_stock < 600:
        risk_score += 15

    # Alerts contribute up to 20 points
    risk_score += min(20, len(alerts) * 5)

    risk_score = min(100, int(risk_score))
    
    return {

        "phc_id": phc_id,

        "predicted_patients": predicted_patients,

        "paracetamol_needed": paracetamol_needed,

        "amoxicillin_needed": amoxicillin_needed,

        "remaining_stock": remaining_stock,

        "doctor_utilization": doctor_utilization,

        "risk_score": risk_score,

        "alerts": alerts

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    result = predict_tomorrow("PHC_01")

    print(result)