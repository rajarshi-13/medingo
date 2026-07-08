"""
===========================================================
PHC Generator
===========================================================

Generates realistic Primary Health Centres (PHCs)
using Gaussian distributions.

No daily simulation happens here.
"""

import math
import numpy as np
import pandas as pd

from config import *

# ===========================================================
# Utility
# ===========================================================

def clip(value, low, high):
    return max(low, min(high, value))


# ===========================================================
# PHC TYPE
# ===========================================================

def generate_phc_type():

    return str(np.random.choice(
    list(PHC_TYPE_DISTRIBUTION.keys()),
    p=list(PHC_TYPE_DISTRIBUTION.values())
))

# ===========================================================
# REGION
# ===========================================================

def generate_region(phc_type):

    regions = {

        "Rural": [

            "North Plains",
            "Central India",
            "Hilly"

        ],

        "Semi Urban": [

            "North Plains",
            "Central India",
            "Coastal"

        ],

        "Urban": [

            "North Plains",
            "Central India",
            "Coastal"

        ]

    }

    return str(np.random.choice(regions[phc_type]))


# ===========================================================
# POPULATION
# ===========================================================

def generate_population(phc_type):

    info = POPULATION[phc_type]

    population = int(

        np.random.normal(

            info["mean"],
            info["std"]

        )

    )

    return clip(population, 5000, 50000)


# ===========================================================
# BASE DAILY OPD
# ===========================================================

def generate_base_patients(population):

    opd_rate = np.random.normal(

        OPD_RATE_MEAN,

        OPD_RATE_STD

    )

    opd_rate = clip(opd_rate, 0.0035, 0.0065)

    patients = int(population * opd_rate)

    return clip(patients, 30, 220)


# ===========================================================
# DOCTORS
# ===========================================================

def generate_doctors(base_patients):

    doctors = math.ceil(

        base_patients / PATIENTS_PER_DOCTOR

    )

    return clip(doctors, 2, 8)


# ===========================================================
# BEDS
# ===========================================================

def generate_beds(base_patients):

    beds = round(

        base_patients * BED_OCCUPANCY_RATIO

    )

    return clip(beds, 6, 30)


# ===========================================================
# INITIAL STOCK
# ===========================================================

def generate_initial_stock(base_patients):

    daily_usage = base_patients * PARACETAMOL_USAGE["mean"]

    stock = int(

        daily_usage *

        MONTHLY_STOCK_BUFFER *

        np.random.normal(1.0, 0.08)

    )

    return max(stock, 800)


# ===========================================================
# MAIN
# ===========================================================

def generate_phcs():

    phcs = []

    for i in range(NUM_PHCS):

        phc_type = generate_phc_type()

        region = generate_region(phc_type)

        population = generate_population(phc_type)

        base_patients = generate_base_patients(population)

        doctors = generate_doctors(base_patients)

        beds = generate_beds(base_patients)

        stock = generate_initial_stock(base_patients)

        phcs.append({

            "phc_id": f"PHC_{i+1:02d}",

            "type": phc_type,

            "region": region,

            "population": population,

            "base_patients": base_patients,

            "doctors": doctors,

            "beds": beds,

            "initial_stock": stock

        })

    return pd.DataFrame(phcs)


# ===========================================================
# TEST
# ===========================================================

if __name__ == "__main__":

    phcs = generate_phcs()

    print(phcs.head())