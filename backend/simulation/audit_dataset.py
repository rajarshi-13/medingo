"""
===========================================================
Dataset Audit
===========================================================

Checks dataset quality before training.
"""

import pandas as pd

# ----------------------------------------------------------

df = pd.read_csv("dataset.csv")

print("\n==============================")
print("DATASET SHAPE")
print("==============================")
print(df.shape)

print("\n==============================")
print("COLUMN NAMES")
print("==============================")
print(df.columns.tolist())

print("\n==============================")
print("DATA TYPES")
print("==============================")
print(df.dtypes)

print("\n==============================")
print("MISSING VALUES")
print("==============================")
print(df.isnull().sum())

print("\n==============================")
print("DUPLICATE ROWS")
print("==============================")
print(df.duplicated().sum())

print("\n==============================")
print("NUMERIC SUMMARY")
print("==============================")
print(df.describe())

print("\n==============================")
print("TARGET SUMMARY")
print("==============================")
print(df["patients_tomorrow"].describe())

print("\n==============================")
print("TARGET DISTRIBUTION")
print("==============================")
print(df["patients_tomorrow"].value_counts().sort_index())

print("\n==============================")
print("UNIQUE VALUES")
print("==============================")

for col in df.columns:
    print(f"{col:25} {df[col].nunique()}")

print("\nAudit Complete ✅")