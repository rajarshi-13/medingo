"""
===========================================================
Hospital Operations Engine
===========================================================

Simulates day-to-day hospital operations.

Input
-----
Master DataFrame

Output
------
Operations DataFrame
"""

import numpy as np
import pandas as pd
from config import *

# ==========================================================
# Utility
# ==========================================================

def clip(value, low, high):

    return max(low, min(high, value))


# ==========================================================
# Simulate One PHC
# ==========================================================


def simulate_one_phc(phc_df):

    rows = []

    # ---------------------------------------------
    # Initial State
    # ---------------------------------------------

    stock = phc_df.iloc[0]["initial_stock"]

    for _, row in phc_df.iterrows():

        # =============================================
        # 1. Healthcare Demand
        # =============================================

        demand = row["base_patients"]

        demand += row["viral_pressure"] * 0.35
        demand += row["respiratory_pressure"] * 0.18
        demand += row["waterborne_pressure"] * 0.12

        if row["is_festival"] == 1:
            demand += 12

        if row["is_holiday"] == 1:
            demand += 8

        if row["is_weekend"] == 1:
            demand -= 8

        demand += np.random.normal(0, 4)

        demand = max(0, round(demand))

        # =============================================
        # 2. Doctor Capacity
        # =============================================

        doctor_capacity = row["doctors"] * 45

        # =============================================
        # 3. Medicine Usage Rate
        # (Different every day)
        # =============================================

        para_rate = np.random.normal(
            0.65 + row["viral_pressure"] / 500,
            0.04
        )

        para_rate = clip(para_rate, 0.50, 0.95)

        amox_rate = np.random.normal(
            0.15 + row["waterborne_pressure"] / 600,
            0.03
        )

        amox_rate = clip(amox_rate, 0.08, 0.35)

        # =============================================
        # 4. Expected Medicines
        # =============================================

        expected_para = round(demand * para_rate)

        expected_amox = round(demand * amox_rate)

        expected_total = expected_para + expected_amox

        # =============================================
        # 5. Final Patients Served
        # =============================================

        patients = min(

            demand,

            doctor_capacity

        )
        # =============================================
        # 7. Actual Medicines Used
        # =============================================

        paracetamol = round(

            patients *

            para_rate

        )

        amoxicillin = round(

            patients *

            amox_rate

        )

        total_used = paracetamol + amoxicillin

        # =============================================
        # 8. Update Stock
        # =============================================

        actual_used = min(

            total_used,

            stock

        )

        stock -= actual_used

        stock = max(stock, 0)

        # =============================================
        # Automatic Reorder
        # =============================================

        if stock < row["initial_stock"] * REORDER_LEVEL:

            stock += int(

                row["initial_stock"] *

                REORDER_QUANTITY

            )

        # =============================================
        # 9. Bed Occupancy
        # =============================================

        bed_occupancy = min(

            round(

                patients * 0.18

            ),

            row["beds"]

        )

        # =============================================
        # 10. Doctor Utilization
        # =============================================

        doctor_utilization = round(

            patients /

            doctor_capacity *

            100,

            1

        )

        # =============================================
        # 11. Patients Turned Away
        # =============================================

        unserved = max(

            demand - patients,

            0

        )

        # =============================================
        # 12. Stockout Flag
        # =============================================

        stockout_flag = int(

            stock < row["initial_stock"] * 0.20

        )

        rows.append({

            "phc_id": row["phc_id"],

            "date": row["date"],

            "patients_today": patients,

            "patients_unserved": unserved,

            "paracetamol_used": paracetamol,

            "amoxicillin_used": amoxicillin,

            "stock_remaining": stock,

            "stockout_flag": stockout_flag,

            "bed_occupancy": bed_occupancy,

            "doctor_utilization": doctor_utilization

        })

    return pd.DataFrame(rows)
# ==========================================================
# Main
# ==========================================================

def simulate_operations(master_df):

    all_operations = []

    # Process one PHC at a time
    for phc_id in master_df["phc_id"].unique():

        phc_history = (

            master_df[master_df["phc_id"] == phc_id]

            .sort_values("date")

            .reset_index(drop=True)

        )

        operations = simulate_one_phc(phc_history)

        all_operations.append(operations)

    operations_df = pd.concat(

        all_operations,

        ignore_index=True

    )

    return operations_df


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    from simulator import build_master_dataframe

    master_df = build_master_dataframe()

    operations_df = simulate_operations(master_df)

    print()

    print(operations_df.head())

    print()

    print("Rows :", len(operations_df))

    print("Columns :", len(operations_df.columns))