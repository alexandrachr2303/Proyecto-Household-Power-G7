import mlflow


TRACKING_URI = "http://127.0.0.1:5000"

EXPERIMENT_NAME = "household-power-forecasting"

DATA_VERSION = "uci_235_hourly_v1"

RANDOM_SEED = 42


def setup_mlflow():
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)