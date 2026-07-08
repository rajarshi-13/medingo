"""
===========================================================
Weather Engine
===========================================================

Generates realistic daily environmental conditions.

Input:
    Calendar DataFrame

Output:
    Weather DataFrame
"""

import numpy as np
import pandas as pd

# ----------------------------------------------------------
# Seasonal Weather Profiles
# ----------------------------------------------------------

WEATHER_PROFILE = {

    "Winter": {

        "temp_mean": 18,
        "temp_std": 4,

        "humidity_mean": 55,
        "humidity_std": 10,

        "aqi_mean": 145,
        "aqi_std": 25

    },

    "Summer": {

        "temp_mean": 39,
        "temp_std": 3,

        "humidity_mean": 38,
        "humidity_std": 8,

        "aqi_mean": 170,
        "aqi_std": 30

    },

    "Monsoon": {

        "temp_mean": 29,
        "temp_std": 2,

        "humidity_mean": 88,
        "humidity_std": 5,

        "aqi_mean": 110,
        "aqi_std": 20

    },

    "Post Monsoon": {

        "temp_mean": 26,
        "temp_std": 3,

        "humidity_mean": 70,
        "humidity_std": 8,

        "aqi_mean": 135,
        "aqi_std": 25

    }

}


# ----------------------------------------------------------
# Utility
# ----------------------------------------------------------

def clip(value, low, high):

    return max(low, min(high, value))


# ----------------------------------------------------------
# Weather Generator
# ----------------------------------------------------------

def generate_weather(calendar_df):

    weather = []

    previous_temp = None

    for _, row in calendar_df.iterrows():

        profile = WEATHER_PROFILE[row["season"]]

        # ------------------------------------------
        # Temperature with persistence
        # ------------------------------------------

        sampled_temp = np.random.normal(

            profile["temp_mean"],
            profile["temp_std"]

        )

        if previous_temp is None:

            temperature = sampled_temp

        else:

            temperature = (

                previous_temp * 0.80 +

                sampled_temp * 0.20

            )

        previous_temp = temperature

        temperature = round(

            clip(temperature, 5, 48),

            1

        )

        # ------------------------------------------
        # Humidity
        # ------------------------------------------

        humidity = round(

            clip(

                np.random.normal(

                    profile["humidity_mean"],
                    profile["humidity_std"]

                ),

                20,

                100

            ),

            1

        )

        # ------------------------------------------
        # Rainfall
        # Gamma Distribution
        # ------------------------------------------

        if row["season"] == "Monsoon":

            rainfall = np.random.gamma(3.5, 10)

        elif row["season"] == "Post Monsoon":

            rainfall = np.random.gamma(2.0, 5)

        else:

            rainfall = np.random.gamma(0.6, 1.5)

        rainfall = round(rainfall, 1)

        # ------------------------------------------
        # AQI
        # ------------------------------------------

        aqi = int(

            clip(

                np.random.normal(

                    profile["aqi_mean"],
                    profile["aqi_std"]

                ),

                20,

                450

            )

        )

        # ------------------------------------------
        # Weather Type
        # ------------------------------------------

        if rainfall > 40:

            weather_type = "Heavy Rain"

        elif rainfall > 10:

            weather_type = "Rain"

        elif humidity > 80:

            weather_type = "Cloudy"

        elif temperature > 37:

            weather_type = "Hot"

        else:

            weather_type = "Clear"

        
        weather.append({

            "date": row["date"],

            "temperature": temperature,

            "humidity": humidity,

            "rainfall": rainfall,

            "aqi": aqi,

            "weather_type": weather_type

            

        })

    return pd.DataFrame(weather)


# ----------------------------------------------------------
# Testing
# ----------------------------------------------------------

if __name__ == "__main__":

    from calendar_engine import generate_calendar

    calendar = generate_calendar()

    weather = generate_weather(calendar)

    print(weather.head(10))