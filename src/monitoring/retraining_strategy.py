import json
from pathlib import Path


PSI_THRESHOLD = 0.25
PERFORMANCE_DEGRADATION_THRESHOLD = 50.0


def evaluate_retraining(psi, mae_change_percent, rmse_change_percent):
    """Determina si se debe activar el reentrenamiento."""

    drift_detected = psi >= PSI_THRESHOLD

    performance_degraded = (
        mae_change_percent >= PERFORMANCE_DEGRADATION_THRESHOLD
        or rmse_change_percent >= PERFORMANCE_DEGRADATION_THRESHOLD
    )

    if drift_detected and performance_degraded:
        return {
            "retrain": True,
            "status": "RETRAIN",
            "reason": "Data drift and model degradation detected",
        }

    if drift_detected and not performance_degraded:
        return {
            "retrain": False,
            "status": "MONITOR",
            "reason": "Data drift detected but model performance remains acceptable",
        }

    return {
        "retrain": False,
        "status": "NO_RETRAIN",
        "reason": "No significant data drift detected",
    }


def main():
    """Evalua la estrategia de reentrenamiento desde la terminal."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate retraining strategy"
    )

    parser.add_argument("--psi", type=float, required=True)
    parser.add_argument("--mae-change", type=float, required=True)
    parser.add_argument("--rmse-change", type=float, required=True)
    parser.add_argument(
        "--output",
        default="reports/retraining_decision.json",
    )

    args = parser.parse_args()

    result = evaluate_retraining(
        psi=args.psi,
        mae_change_percent=args.mae_change,
        rmse_change_percent=args.rmse_change,
    )

    result["inputs"] = {
        "psi": args.psi,
        "mae_change_percent": args.mae_change,
        "rmse_change_percent": args.rmse_change,
    }

    result["thresholds"] = {
        "psi": PSI_THRESHOLD,
        "performance_degradation_percent": PERFORMANCE_DEGRADATION_THRESHOLD,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
