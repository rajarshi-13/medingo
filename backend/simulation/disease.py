"""
===========================================================
Disease Engine
===========================================================

Generates disease pressure from weather conditions.

Input:
    calendar_df
    weather_df

Output:
    disease_df
"""

import numpy as np
import pandas as pd

# ----------------------------------------------------------
# Utility
# ----------------------------------------------------------

def clip(value):

    return max(0, min(100, value))


# ----------------------------------------------------------
# Disease Generator
# ----------------------------------------------------------

def generate_disease(calendar_df, weather_df):

    merged_df = calendar_df.merge(weather_df, on="date")

    disease = []

    previous_viral = None
    previous_respiratory = None
    previous_waterborne = None

    for _, row in merged_df.iterrows():

        # ==================================================
        # Viral Pressure
        # ==================================================

        viral = (

            row["humidity"] * 0.45 +

            row["rainfall"] * 0.40 +

            np.random.normal(0, 5)

        )

        if row["season"] in ["Winter", "Monsoon"]:

            viral += 18

        # Disease persistence
        if previous_viral is not None:

            viral = previous_viral * 0.80 + viral * 0.20

        viral = clip(viral)

        previous_viral = viral

        # ==================================================
        # Respiratory Pressure
        # ==================================================

        respiratory = (

            row["aqi"] * 0.35 +

            np.random.normal(0, 4)

        )

        if row["temperature"] < 20:

            respiratory += 15

        if previous_respiratory is not None:

            respiratory = previous_respiratory * 0.80 + respiratory * 0.20

        respiratory = clip(respiratory)

        previous_respiratory = respiratory

        # ==================================================
        # Waterborne Pressure
        # ==================================================

        waterborne = (

            row["rainfall"] * 0.70 +

            row["humidity"] * 0.20 +

            np.random.normal(0, 4)

        )

        if row["season"] == "Monsoon":

            waterborne += 20

        if previous_waterborne is not None:

            waterborne = previous_waterborne * 0.80 + waterborne * 0.20

        waterborne = clip(waterborne)

        previous_waterborne = waterborne

        disease.append({

            "date": row["date"],

            "viral_pressure": round(viral, 1),

            "respiratory_pressure": round(respiratory, 1),

            "waterborne_pressure": round(waterborne, 1)

        })

    return pd.DataFrame(disease)


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    from calendar_engine import generate_calendar
    from weather import generate_weather

    calendar_df = generate_calendar()

    weather_df = generate_weather(calendar_df)

    disease_df = generate_disease(
        calendar_df,
        weather_df
    )

    print(disease_df.head(10))