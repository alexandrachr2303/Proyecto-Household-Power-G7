##### LIBRERÍAS
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd


def forecasting_metrics(actual, forecast):
    """Calcula MAE y RMSE comparando valores reales contra pronósticos.""" # Los valores incorrectos se convierten en NaN para poder descartarlos.
    actual = pd.to_numeric(actual, errors="coerce")
    forecast = pd.to_numeric(forecast, errors="coerce")

    # Solo se utilizan filas que tienen valor real y predicción.
    valid = actual.notna() & forecast.notna()
    if not valid.any():
        raise ValueError("No existen pares válidos de actual y forecast")

    # El error es la diferencia entre lo que ocurrió y lo que predijo el modelo.
    errors = actual[valid] - forecast[valid]

    # MAE mide el error absoluto promedio y RMSE penaliza más los errores grandes.
    return {
        "mae": round(float(errors.abs().mean()), 4),
        "rmse": round(float(np.sqrt((errors ** 2).mean())), 4),
        "observations": int(valid.sum()),
    }

def monitor_batches(data, actual_column="actual", forecast_column="forecast", batch_column="batch"):
    """Calcula las métricas de cada batch y las compara con la referencia."""
    # El archivo necesita estas tres columnas para realizar el monitoreo.
    required = {actual_column, forecast_column, batch_column}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")

    # Aquí se irán almacenando los resultados de cada batch.
    report = {}
    reference_mae = None

    # Los registros se procesan por grupo o periodo de producción.
    for batch, group in data.groupby(batch_column, sort=False):
        metrics = forecasting_metrics(group[actual_column], group[forecast_column])

        # El primer batch funciona como punto de comparación.
        if reference_mae is None:
            reference_mae = metrics["mae"]
            metrics["mae_change_percent"] = 0.0
            metrics["status"] = "REFERENCE"
        else:
            # Se calcula cuánto aumentó o disminuyó el MAE frente a la referencia.
            change = ((metrics["mae"] - reference_mae) / max(reference_mae, 0.0001)) * 100
            metrics["mae_change_percent"] = round(change, 2)

            # Los estados ayudan a interpretar rápidamente el cambio del error.
            metrics["status"] = "ALERT" if change >= 50 else "WARNING" if change >= 20 else "OK"
        report[str(batch)] = metrics
    return report

def main():
    """Lee el CSV indicado en la terminal y genera el reporte del modelo."""
    # Las opciones permiten cambiar los nombres de columnas si fuera necesario.
    parser = argparse.ArgumentParser(description="Calcula MAE y RMSE por batch de producción")
    parser.add_argument("--input", required=True)
    parser.add_argument("--actual-column", default="actual")
    parser.add_argument("--forecast-column", default="forecast")
    parser.add_argument("--batch-column", default="batch")
    parser.add_argument("--output", default="reports/model_monitoring.json")
    args = parser.parse_args()

    # Se carga el archivo que contiene actual, forecast y batch.
    data = pd.read_csv(args.input)
    report = monitor_batches(data, args.actual_column, args.forecast_column, args.batch_column)

    # La carpeta de salida se crea automáticamente.
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    # El resultado queda guardado en JSON y también se imprime en la terminal.
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    # Ejecuta el programa cuando se llama con python -m.
    main()
