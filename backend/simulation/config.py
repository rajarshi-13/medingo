"""
===========================================================
Medingo PHC Simulator Configuration
===========================================================

This file contains every configurable parameter used
throughout the simulator.

No simulation logic should be written here.
"""

import numpy as np

# ===========================================================
# RANDOM SEED
# ===========================================================

# Makes the generated dataset reproducible.
# Remove this later if you want different datasets every run.
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)

# ===========================================================
# SIMULATION PERIOD
# ===========================================================

START_YEAR = 2023
END_YEAR = 2025

# ===========================================================
# NUMBER OF PHCs
# ===========================================================

NUM_PHCS = 25

# ===========================================================
# PHC DISTRIBUTION
# ===========================================================

PHC_TYPE_DISTRIBUTION = {

    "Rural": 0.40,
    "Semi Urban": 0.35,
    "Urban": 0.25

}

# ===========================================================
# POPULATION DISTRIBUTIONS
# Mean and Standard Deviation
# ===========================================================

POPULATION = {

    "Rural": {

        "mean": 12000,
        "std": 2500

    },

    "Semi Urban": {

        "mean": 22000,
        "std": 3500

    },

    "Urban": {

        "mean": 35000,
        "std": 4500

    }

}

# ===========================================================
# HEALTHCARE CONSTANTS
# ===========================================================

PATIENTS_PER_DOCTOR = 35

BED_OCCUPANCY_RATIO = 0.18

MONTHLY_STOCK_BUFFER = 40

# ===========================================================
# OPD RATE
# Percentage of population visiting PHC daily
# ===========================================================

OPD_RATE_MEAN = 0.0048

OPD_RATE_STD = 0.0004

# ===========================================================
# WEATHER
# ===========================================================

SEASONS = {

    12: "Winter",
    1: "Winter",
    2: "Winter",

    3: "Summer",
    4: "Summer",
    5: "Summer",

    6: "Monsoon",
    7: "Monsoon",
    8: "Monsoon",
    9: "Monsoon",

    10: "Post Monsoon",
    11: "Post Monsoon"

}

# ===========================================================
# MEDICINE CONSUMPTION
# ===========================================================

PARACETAMOL_USAGE = {

    "mean": 0.72,
    "std": 0.08

}

AMOXICILLIN_USAGE = {

    "mean": 0.22,
    "std": 0.05

}

# ==========================
# INVENTORY
# ==========================

REORDER_LEVEL = 0.30        # 30%

REORDER_QUANTITY = 0.80     # 80% of initial stock

DELIVERY_DELAY = 5          # days