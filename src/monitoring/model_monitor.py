import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def forecasting_metrics(actual, forecast):
    """Calcula MAE y RMSE comparando valores reales contra pronósticos."""
    actual = pd.to_numeric(actual, errors="coerce")
    forecast = pd.to_numeric(forecast, errors="coerce")

    valid = actual.notna() & forecast.notna()

    if not valid.any():
        raise ValueError("No existen pares válidos de actual y forecast")

    errors = actual[valid] - forecast[valid]

    return {
        "mae": round(float(errors.abs().mean()), 4),
        "rmse": round(float(np.sqrt((errors ** 2).mean())), 4),
        "observations": int(valid.sum()),
    }


def monitor_batches(
    data,
    actual_column="actual",
    forecast_column="forecast",
    batch_column="batch",
):
    """Calcula MAE y RMSE por batch y compara contra la referencia."""

    required = {actual_column, forecast_column, batch_column}
    missing = required - set(data.columns)

    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")

    report = {}
    reference_mae = None
    reference_rmse = None

    for batch, group in data.groupby(batch_column, sort=False):

        metrics = forecasting_metrics(
            group[actual_column],
            group[forecast_column],
        )

        if reference_mae is None:
            reference_mae = metrics["mae"]
            reference_rmse = metrics["rmse"]

            metrics["mae_change_percent"] = 0.0
            metrics["rmse_change_percent"] = 0.0
            metrics["status"] = "REFERENCE"

        else:
            mae_change = (
                (metrics["mae"] - reference_mae)
                / max(reference_mae, 0.0001)
            ) * 100

            rmse_change = (
                (metrics["rmse"] - reference_rmse)
                / max(reference_rmse, 0.0001)
            ) * 100

            metrics["mae_change_percent"] = round(mae_change, 2)
            metrics["rmse_change_percent"] = round(rmse_change, 2)

            # ALERT si cualquiera de las dos métricas empeora >= 50%
            # WARNING si cualquiera empeora >= 20%
            if mae_change >= 50 or rmse_change >= 50:
                metrics["status"] = "ALERT"
            elif mae_change >= 20 or rmse_change >= 20:
                metrics["status"] = "WARNING"
            else:
                metrics["status"] = "OK"

        report[str(batch)] = metrics

    return report


def main():
    """Lee el CSV indicado y genera el reporte de monitoreo del modelo."""

    parser = argparse.ArgumentParser(
        description="Calcula MAE y RMSE por batch de producción"
    )

    parser.add_argument("--input", required=True)
    parser.add_argument("--actual-column", default="actual")
    parser.add_argument("--forecast-column", default="forecast")
    parser.add_argument("--batch-column", default="batch")
    parser.add_argument(
        "--output",
        default="reports/model_monitoring.json",
    )

    args = parser.parse_args()

    data = pd.read_csv(args.input)

    report = monitor_batches(
        data,
        args.actual_column,
        args.forecast_column,
        args.batch_column,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()