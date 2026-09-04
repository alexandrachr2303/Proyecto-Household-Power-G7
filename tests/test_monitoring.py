import pandas as pd
import pytest

from src.monitoring.data_monitor import calculate_psi, drift_status, monitor_data
from src.monitoring.model_monitor import forecasting_metrics, monitor_batches
from src.monitoring.system_monitor import SystemMonitor
from src.monitoring.retraining_strategy import evaluate_retraining
from src.monitoring.quality_monitor import training_quality_gate


def test_system_monitor_records_requests():
    """Comprueba que las solicitudes y los errores se registren correctamente."""
    monitor = SystemMonitor()
    monitor.record_request(20, 200)
    monitor.record_request(40, 500)
    metrics = monitor.get_metrics()

    assert metrics["latency_avg_ms"] == 30
    assert metrics["error_rate"] == 0.5
    assert metrics["availability"] == 0.5
    assert metrics["throughput_requests_per_second"] > 0


def test_psi_detects_distribution_change():
    """Comprueba que PSI diferencie datos estables de un drift fuerte."""
    reference = pd.Series(range(1, 101))
    production_ok = pd.Series(range(1, 101))
    production_drift = pd.Series(range(201, 301))

    assert calculate_psi(reference, production_ok) < 0.10
    assert drift_status(calculate_psi(reference, production_drift)) == "ALERT"


def test_data_monitor_reports_missing_column():
    """Comprueba que el reporte avise cuando falta una columna requerida."""
    reference = pd.DataFrame({"power": [1, 2, 3]})
    production = pd.DataFrame({"other": [1, 2, 3]})

    assert monitor_data(reference, production, ["power"])["power"]["status"] == "ERROR"


def test_forecasting_metrics_are_correct():
    """Comprueba el resultado conocido de MAE y RMSE."""
    metrics = forecasting_metrics(
        pd.Series([10, 20]),
        pd.Series([12, 18]),
    )

    assert metrics == {"mae": 2.0, "rmse": 2.0, "observations": 2}


def test_model_monitor_separates_batches():
    """Comprueba que cada batch reciba sus propias métricas."""
    data = pd.DataFrame({
        "batch": ["batch_1", "batch_1", "batch_2"],
        "actual": [10, 20, 30],
        "forecast": [11, 19, 25],
    })

    report = monitor_batches(data)

    assert report["batch_1"]["mae"] == 1.0
    assert report["batch_2"]["mae"] == 5.0


def test_retraining_when_drift_and_performance_degradation():
    result = evaluate_retraining(
        psi=8.2831,
        mae_change_percent=300.0,
        rmse_change_percent=300.0,
    )

    assert result["retrain"] is True
    assert result["status"] == "RETRAIN"


def test_monitor_when_drift_without_strong_performance_degradation():
    result = evaluate_retraining(
        psi=8.2831,
        mae_change_percent=20.0,
        rmse_change_percent=20.0,
    )

    assert result["retrain"] is False
    assert result["status"] == "MONITOR"


def test_no_retrain_when_there_is_no_significant_drift():
    result = evaluate_retraining(
        psi=0.05,
        mae_change_percent=10.0,
        rmse_change_percent=10.0,
    )

    assert result["retrain"] is False
    assert result["status"] == "NO_RETRAIN"


def test_training_quality_gate_accepts_clean_dataset():
    """Comprueba que el Quality Gate permita datos limpios antes del entrenamiento."""
    data = pd.DataFrame({
        "Global_active_power": [1.1, 1.2, 1.3],
        "hour_sin": [0.0, 0.5, 0.8],
        "hour_cos": [1.0, 0.8, 0.6],
        "day_of_week_sin": [0.0, 0.7, 1.0],
        "day_of_week_cos": [1.0, 0.7, 0.0],
        "month_sin": [0.0, 0.5, 0.9],
        "month_cos": [1.0, 0.8, 0.4],
        "is_weekend": [0, 0, 1],
        "lag_1": [1.0, 1.1, 1.2],
        "lag_24": [1.0, 1.1, 1.2],
        "lag_168": [1.0, 1.1, 1.2],
        "rolling_mean_3": [1.0, 1.1, 1.2],
        "rolling_mean_24": [1.0, 1.1, 1.2],
        "rolling_std_24": [0.1, 0.1, 0.1],
    })

    report = training_quality_gate(data)

    assert report["status"] == "OK"
    assert report["incident_count"] == 0


def test_training_quality_gate_blocks_invalid_dataset():
    """Comprueba que el Quality Gate bloquee datos con valores faltantes."""
    data = pd.DataFrame({
        "Global_active_power": [1.1, None, 1.3],
        "hour_sin": [0.0, 0.5, 0.8],
        "hour_cos": [1.0, 0.8, 0.6],
        "day_of_week_sin": [0.0, 0.7, 1.0],
        "day_of_week_cos": [1.0, 0.7, 0.0],
        "month_sin": [0.0, 0.5, 0.9],
        "month_cos": [1.0, 0.8, 0.4],
        "is_weekend": [0, 0, 1],
        "lag_1": [1.0, 1.1, 1.2],
        "lag_24": [1.0, 1.1, 1.2],
        "lag_168": [1.0, 1.1, 1.2],
        "rolling_mean_3": [1.0, 1.1, 1.2],
        "rolling_mean_24": [1.0, 1.1, 1.2],
        "rolling_std_24": [0.1, 0.1, 0.1],
    })

    with pytest.raises(ValueError, match="Training Data Quality Gate BLOCKED"):
        training_quality_gate(data)