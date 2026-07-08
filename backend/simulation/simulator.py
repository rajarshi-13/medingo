"""
===========================================================
Simulator
===========================================================

Builds the master dataframe.

No business logic is applied here.
"""

import pandas as pd

from phc import generate_phcs
from calendar_engine import generate_calendar
from weather import generate_weather
from disease import generate_disease


def build_master_dataframe():

    # ------------------------------------
    # Generate individual datasets
    # ------------------------------------

    phc_df = generate_phcs()

    calendar_df = generate_calendar()

    weather_df = generate_weather(calendar_df)

    disease_df = generate_disease(
        calendar_df,
        weather_df
    )

    # ------------------------------------
    # Merge Calendar + Weather + Disease
    # ------------------------------------

    daily_df = calendar_df.merge(
        weather_df,
        on="date"
    )

    daily_df = daily_df.merge(
        disease_df,
        on="date"
    )

    # ------------------------------------
    # Cartesian Product
    # Every PHC × Every Day
    # ------------------------------------

    phc_df["key"] = 1
    daily_df["key"] = 1

    master_df = phc_df.merge(
        daily_df,
        on="key"
    ).drop(
        columns="key"
    )

    return master_df


if __name__ == "__main__":

    master_df = build_master_dataframe()

    print()

    print(master_df.head())

    print()

    print("Rows :", len(master_df))

    print("Columns :", len(master_df.columns))