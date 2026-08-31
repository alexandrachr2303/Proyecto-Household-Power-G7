import pandas as pd

from src.monitoring.data_monitor import calculate_psi, drift_status, monitor_data
from src.monitoring.model_monitor import forecasting_metrics, monitor_batches
from src.monitoring.system_monitor import SystemMonitor


def test_system_monitor_records_requests():
    """Comprueba que las solicitudes y los errores se registren correctamente."""
    # Se simula una solicitud exitosa y otra con error del servidor.
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
    # production_ok es igual a referencia; production_drift está desplazada.
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
    # En ambos registros el error absoluto es 2.
    metrics = forecasting_metrics(pd.Series([10, 20]), pd.Series([12, 18]))

    assert metrics == {"mae": 2.0, "rmse": 2.0, "observations": 2}


def test_model_monitor_separates_batches():
    """Comprueba que cada batch reciba sus propias métricas."""
    # El segundo batch tiene un error mayor que el primero.
    data = pd.DataFrame({
        "batch": ["batch_1", "batch_1", "batch_2"],
        "actual": [10, 20, 30],
        "forecast": [11, 19, 25],
    })

    report = monitor_batches(data)
    assert report["batch_1"]["mae"] == 1.0
    assert report["batch_2"]["mae"] == 5.0
