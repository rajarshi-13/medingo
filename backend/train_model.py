"""
===========================================================
Train Patient Forecast Model
===========================================================

Trains an XGBoost Regressor to predict
Tomorrow's Patient Count.
"""

import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from xgboost import XGBRegressor


# ==========================================================
# Load Dataset
# ==========================================================

print("\nLoading dataset...")

df = pd.read_csv("simulation/dataset.csv")

print(df.shape)


# ==========================================================
# Drop Unnecessary Columns
# ==========================================================

DROP_COLUMNS = [

    "phc_id",
    "date",
    "holiday_name",
    "festival_name",
    "month_name",
    "season"

]

df = df.drop(columns=DROP_COLUMNS)


# ==========================================================
# Encode Categorical Features
# ==========================================================

label_encoders = {}

categorical_columns = [

    "type",
    "region",
    "weather_type"

]

for column in categorical_columns:

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(df[column])

    label_encoders[column] = encoder


# ==========================================================
# Features / Target
# ==========================================================

TARGET = "patients_tomorrow"

X = df.drop(columns=[TARGET])

y = df[TARGET]


print("\nFeatures :", X.shape)
print("Target   :", y.shape)


# ==========================================================
# Train Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42

)


# ==========================================================
# Model
# ==========================================================

print("\nTraining XGBoost...\n")

model = XGBRegressor(

    n_estimators=300,

    learning_rate=0.05,

    max_depth=6,

    subsample=0.85,

    colsample_bytree=0.85,

    random_state=42,

    objective="reg:squarederror"

)

model.fit(

    X_train,

    y_train

)


# ==========================================================
# Prediction
# ==========================================================

predictions = model.predict(

    X_test

)


# ==========================================================
# Evaluation
# ==========================================================

mae = mean_absolute_error(

    y_test,

    predictions

)

rmse = np.sqrt(

    mean_squared_error(

        y_test,

        predictions

    )

)

r2 = r2_score(

    y_test,

    predictions

)


print("\n==========================")
print("MODEL PERFORMANCE")
print("==========================")

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")


# ==========================================================
# Feature Importance
# ==========================================================

importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print("\nTop 15 Features\n")

print(

    importance.head(15)

)


# ==========================================================
# Save Model
# ==========================================================

joblib.dump(

    model,

    "patient_forecast_model.pkl"

)

joblib.dump(

    label_encoders,

    "label_encoders.pkl"

)

joblib.dump(

    list(X.columns),

    "feature_columns.pkl"

)


print("\nModel Saved Successfully!")