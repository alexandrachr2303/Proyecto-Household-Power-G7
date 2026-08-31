##### LIBRERÍAS
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd


def calculate_psi(reference, production, bins=10):     # Convierte los valores a #. Los incorrectos pasan a NaN.
    """Calcula PSI usando los cortes definidos únicamente con referencia."""
    reference = pd.to_numeric(reference, errors="coerce")
    production = pd.to_numeric(production, errors="coerce")

    # Para construir los intervalos se trabaja primero con valores no faltantes.
    clean_reference = reference.dropna()
    clean_production = production.dropna()

    # El cálculo no se puede realizar si uno de los grupos quedó vacío.
    if clean_reference.empty or clean_production.empty:
        raise ValueError("PSI necesita valores numéricos válidos en ambos grupos")

    # Los límites de los intervalos se calculan solo con los datos de referencia.
    cuts = np.unique(clean_reference.quantile(np.linspace(0, 1, bins + 1)).to_numpy())
    if len(cuts) < 2:
        return 0.0 if clean_production.eq(clean_reference.iloc[0]).all() else 1.0    # Una variable constante no presenta drift si conserva el mismo valor.

    # Los extremos infinitos permiten incluir valores nuevos muy bajos o muy altos.
    cuts[0], cuts[-1] = -np.inf, np.inf

    # Se cuenta cuántos valores caen dentro de cada intervalo.
    reference_counts = pd.cut(clean_reference, cuts, include_lowest=True).value_counts(sort=False)
    production_counts = pd.cut(clean_production, cuts, include_lowest=True).value_counts(sort=False)

    # Los conteos se convierten a % para poder comparar ambos grupos.
    reference_pct = reference_counts / len(clean_reference)
    production_pct = production_counts / len(clean_production)

    # Epsilon evita calcular logaritmos de cero cuando un intervalo está vacío.
    epsilon = 0.0001

    # Fórmula del Population Stability Index para todos los intervalos.
    psi = ((production_pct.clip(lower=epsilon) - reference_pct.clip(lower=epsilon)) *
           np.log(production_pct.clip(lower=epsilon) / reference_pct.clip(lower=epsilon))).sum()

    # También se observa si cambió la proporción de datos faltantes.
    ref_missing = max(reference.isna().mean(), epsilon)
    prod_missing = max(production.isna().mean(), epsilon)
    psi += (prod_missing - ref_missing) * np.log(prod_missing / ref_missing)
    return float(psi)


def drift_status(psi):  # Los límites son reglas prácticas elegidas para la simulación del proyecto.
    """Convierte el resultado PSI en un estado fácil de interpretar."""
    if psi >= 0.25:
        return "ALERT"
    if psi >= 0.10:
        return "WARNING"
    return "OK"

def monitor_data(reference, production, columns):
    """Calcula PSI para cada columna solicitada y construye el reporte."""
    report = {}
    for column in columns:
        if column not in reference or column not in production:  # Una columna ausente se reporta como error sin detener todo el análisis.
            report[column] = {"status": "ERROR", "message": "Columna ausente"}
            continue
        psi = calculate_psi(reference[column], production[column])
        report[column] = {"psi": round(psi, 4), "status": drift_status(psi)}
    return report


def main():
    """Recibe los archivos desde la terminal y guarda el resultado en JSON."""
    # argparse permite utilizar opciones como --reference y --production.
    parser = argparse.ArgumentParser(description="Compara datos de referencia y producción con PSI")
    parser.add_argument("--reference", required=True)
    parser.add_argument("--production", required=True)
    parser.add_argument("--columns", nargs="+", required=True)
    parser.add_argument("--output", default="reports/data_monitoring.json")
    args = parser.parse_args()

    # Se cargan los dos CSV indicados por la persona que ejecuta el comando.
    reference = pd.read_csv(args.reference)
    production = pd.read_csv(args.production)

    # Se ejecuta el monitoreo solamente para las columnas seleccionadas.
    report = monitor_data(reference, production, args.columns)

    # La carpeta reports se crea automáticamente si todavía no existe.
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    # El reporte se guarda y también se muestra en la terminal.
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    # Esta condición ejecuta main únicamente cuando se llama el módulo directamente.
    main()
