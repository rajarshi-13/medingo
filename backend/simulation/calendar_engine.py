"""
===========================================================
Calendar Generator
===========================================================

Generates the simulation timeline.

This module ONLY generates calendar information.

It does NOT know anything about:
- Weather
- Diseases
- Patients
- Medicines
"""

import pandas as pd
from datetime import datetime, timedelta
from config import START_YEAR, END_YEAR, SEASONS


# ===========================================================
# FIXED NATIONAL HOLIDAYS
# ===========================================================

FIXED_HOLIDAYS = {

    (1, 26): "Republic Day",

    (8, 15): "Independence Day",

    (10, 2): "Gandhi Jayanti"

}


# ===========================================================
# APPROXIMATE FESTIVALS
# (Prototype Version)
# ===========================================================

FESTIVALS = {

    (3, 15): "Holi",

    (10, 20): "Dussehra",

    (11, 5): "Diwali"

}


# ===========================================================
# CALENDAR GENERATOR
# ===========================================================

def generate_calendar():

    start = datetime(START_YEAR, 1, 1)

    end = datetime(END_YEAR, 12, 31)

    calendar = []

    current = start

    while current <= end:

        month = current.month

        season = SEASONS[month]

        holiday_name = FIXED_HOLIDAYS.get(
            (month, current.day),
            None
        )

        festival_name = FESTIVALS.get(
            (month, current.day),
            None
        )

        calendar.append({

            "date": current.date(),

            "year": current.year,

            "quarter": (month - 1) // 3 + 1,

            "month": month,

            "month_name": current.strftime("%B"),

            "day": current.day,

            "day_of_year": current.timetuple().tm_yday,

            "week_of_year": current.isocalendar().week,

            "day_of_week": current.weekday(),

            "is_weekend": int(current.weekday() >= 5),

            "season": season,

            "season_code": {

                "Winter": 0,

                "Summer": 1,

                "Monsoon": 2,

                "Post Monsoon": 3

            }[season],

            "is_holiday": int(holiday_name is not None),

            "holiday_name": holiday_name,

            "is_festival": int(festival_name is not None),

            "festival_name": festival_name

        })

        current += timedelta(days=1)

    return pd.DataFrame(calendar)


# ===========================================================
# TEST
# ===========================================================

if __name__ == "__main__":

    calendar_df = generate_calendar()

    print("\nTotal Days :", len(calendar_df))
    print()

    print(calendar_df.head(10))