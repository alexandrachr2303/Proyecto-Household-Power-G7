import json
from pathlib import Path

import numpy as np
import pandas as pd


EXPECTED_COLUMNS = [
    "Global_active_power",
    "Voltage",
    "Global_intensity",
]

NUMERIC_COLUMNS = [
    "Global_active_power",
    "Voltage",
    "Global_intensity",
]

ALLOWED_CATEGORIES = ["NORMAL"]

OUTLIER_LIMITS = {
    "Global_active_power": 10.0,
    "Voltage": (200.0, 260.0),
    "Global_intensity": 50.0,
}


def validate_quality(df):
    """Validate quality problems in a production batch."""
    incidents = []

    # 1. Schema modification
    actual_columns = list(df.columns)

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]

    extra_columns = [
        column
        for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    if missing_columns or extra_columns:
        incidents.append({
            "type": "schema_modification",
            "status": "BLOCKED",
            "missing_columns": missing_columns,
            "extra_columns": extra_columns,
        })

    # 2. Missing values
    for column in EXPECTED_COLUMNS:
        if column in df.columns:
            count = int(df[column].isna().sum())

            if count > 0:
                incidents.append({
                    "type": "missing_values",
                    "status": "BLOCKED",
                    "column": column,
                    "count": count,
                })

    # 3. Incorrect datatype
    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            if not pd.api.types.is_numeric_dtype(df[column]):
                incidents.append({
                    "type": "incorrect_datatype",
                    "status": "BLOCKED",
                    "column": column,
                    "expected": "numeric",
                    "actual": str(df[column].dtype),
                })

    # 4. Duplicated rows
    duplicated_count = int(df.duplicated().sum())

    if duplicated_count > 0:
        incidents.append({
            "type": "duplicated_rows",
            "status": "BLOCKED",
            "count": duplicated_count,
        })

    # 5. Extreme outliers
    for column, limit in OUTLIER_LIMITS.items():
        if column not in df.columns:
            continue

        numeric_values = pd.to_numeric(df[column], errors="coerce")

        if isinstance(limit, tuple):
            low, high = limit
            count = int(
                (
                    (numeric_values < low)
                    | (numeric_values > high)
                )
                .fillna(False)
                .sum()
            )
        else:
            count = int(
                (numeric_values > limit)
                .fillna(False)
                .sum()
            )

        if count > 0:
            incidents.append({
                "type": "extreme_outlier",
                "status": "BLOCKED",
                "column": column,
                "count": count,
            })

    # 6. Unknown category
    if "quality_category" in df.columns:
        unknown_categories = sorted(
            set(df["quality_category"].dropna())
            - set(ALLOWED_CATEGORIES)
        )

        if unknown_categories:
            incidents.append({
                "type": "unknown_category",
                "status": "BLOCKED",
                "column": "quality_category",
                "unknown_categories": unknown_categories,
            })

    status = "BLOCKED" if incidents else "OK"

    return {
        "status": status,
        "incidents": incidents,
        "incident_count": len(incidents),
    }


def quality_gate(df):
    """Validate production data and block processing when incidents are found."""
    report = validate_quality(df)

    if report["status"] == "BLOCKED":
        raise ValueError(
            f"Data Quality Gate BLOCKED: "
            f"{report['incident_count']} incident(s) detected."
        )

    return report


def training_quality_gate(df):
    """Validate the final modeling dataset before training."""
    incidents = []

    # Columns expected by the final modeling dataset.
    required_columns = [
        "Global_active_power",
        "hour_sin",
        "hour_cos",
        "day_of_week_sin",
        "day_of_week_cos",
        "month_sin",
        "month_cos",
        "is_weekend",
        "lag_1",
        "lag_24",
        "lag_168",
        "rolling_mean_3",
        "rolling_mean_24",
        "rolling_std_24",
    ]

    # 1. Dataset no vacío
    if df.empty:
        incidents.append({
            "type": "empty_dataset",
            "status": "BLOCKED",
        })

    # 2. Required schema
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        incidents.append({
            "type": "missing_required_columns",
            "status": "BLOCKED",
            "columns": missing_columns,
        })

    # 3. Missing values
    missing_values = int(df.isna().sum().sum())

    if missing_values > 0:
        incidents.append({
            "type": "missing_values",
            "status": "BLOCKED",
            "count": missing_values,
        })

    # 4. Incorrect datatype
    non_numeric_columns = [
        column
        for column in required_columns
        if column in df.columns
        and not pd.api.types.is_numeric_dtype(df[column])
    ]

    if non_numeric_columns:
        incidents.append({
            "type": "incorrect_datatype",
            "status": "BLOCKED",
            "columns": non_numeric_columns,
        })

    # 5. Duplicated rows
    duplicated_count = int(df.duplicated().sum())

    if duplicated_count > 0:
        incidents.append({
            "type": "duplicated_rows",
            "status": "BLOCKED",
            "count": duplicated_count,
        })

    # 6. Infinite values
    numeric_df = df.select_dtypes(include="number")

    infinite_count = int(
        np.isinf(numeric_df.to_numpy()).sum()
    )

    if infinite_count > 0:
        incidents.append({
            "type": "infinite_values",
            "status": "BLOCKED",
            "count": infinite_count,
        })

    status = "BLOCKED" if incidents else "OK"

    report = {
        "status": status,
        "incidents": incidents,
        "incident_count": len(incidents),
    }

    if status == "BLOCKED":
        raise ValueError(
            f"Training Data Quality Gate BLOCKED: "
            f"{report['incident_count']} incident(s) detected."
        )

    return report


def main():
    """Run validation and register the incident."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate production batch quality"
    )

    parser.add_argument("--input", required=True)
    parser.add_argument(
        "--output",
        default="reports/quality_contamination.json",
    )

    args = parser.parse_args()

    df = pd.read_csv(args.input)

    report = validate_quality(df)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()