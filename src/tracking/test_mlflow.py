import mlflow


mlflow.set_tracking_uri(
    "http://127.0.0.1:5000"
)

mlflow.set_experiment(
    "household-power-forecasting"
)


with mlflow.start_run(
    run_name="mlflow_setup_test"
):
    mlflow.log_param(
        "test_parameter",
        "ok"
    )

    mlflow.log_metric(
        "test_metric",
        1.0
    )


print("Prueba de MLflow completada.")