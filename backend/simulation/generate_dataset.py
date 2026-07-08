"""
===========================================================
Generate Final Dataset
===========================================================

Creates the final ML dataset for XGBoost.
"""


from simulator import build_master_dataframe
from hospital_operations import simulate_operations


def generate_dataset():

    print("Generating master dataframe...")

    master_df = build_master_dataframe()

    print("Simulating hospital operations...")

    operations_df = simulate_operations(master_df)

    print("Merging datasets...")

    dataset = master_df.merge(

        operations_df,

        on=["phc_id", "date"],

        how="left"

    )

    print("Creating target column...")

    dataset = dataset.sort_values(

        ["phc_id", "date"]

    )

    dataset["patients_tomorrow"] = (

        dataset

        .groupby("phc_id")["patients_today"]

        .shift(-1)

    )
    dataset.reset_index(
    drop=True,
    inplace=True
)

    # Only remove rows where the target is missing
    dataset = dataset.dropna(
        subset=["patients_tomorrow"]
    )

    dataset["patients_tomorrow"] = dataset[
        "patients_tomorrow"
    ].astype(int)

    print()

    print(dataset.head())

    print()

    print("Rows :", len(dataset))
    print("Columns :", len(dataset.columns))

    dataset.to_csv(

        "dataset.csv",

        index=False

    )

    print()

    print("✅ dataset.csv generated successfully!")


if __name__ == "__main__":

    generate_dataset()