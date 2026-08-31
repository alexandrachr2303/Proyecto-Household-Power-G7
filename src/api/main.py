##### LIBRERÍAS

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow
import mlflow.sklearn
import os
import time
from src.monitoring.system_monitor import SystemMonitor


##### CONFIGURACIÓN

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:5000"
)

MODEL_NAME = "random_forest_feature_set_b"
MODEL_VERSION = "1"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


##### CARGA DEL MODELO

model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"
model = mlflow.sklearn.load_model(model_uri)


# API

app = FastAPI(
    title="Household Power Forecasting API",
    description="API para predicción de consumo eléctrico a una hora.",
    version="1.0.0"
)

# Se crea un objeto que conservará las métricas mientras la API esté activa.
system_monitor = SystemMonitor()


@app.middleware("http")
async def collect_system_metrics(request, call_next):
    """Mide cada request sin cambiar la respuesta de la API."""
    # Se guarda el momento exacto en que entra la solicitud.
    start = time.perf_counter()

    status_code = 500  # Se inicia en 500 para registrar un error si la solicitud falla inesperadamente.
    try:
        response = await call_next(request) # call_next permite que FastAPI procese normalmente la solicitud.
        status_code = response.status_code
        return response
    finally: # El bloque finally se ejecuta incluso si ocurre una excepción.
        latency_ms = (time.perf_counter() - start) * 1000
        system_monitor.record_request(latency_ms, status_code)  # Se envían el tiempo y el código HTTP al monitor del sistema.


##### INPUT

class PredictionInput(BaseModel):
    lag_1: float
    lag_168: float
    hour_sin: float
    hour_cos: float
    lag_24: float
    rolling_mean_3: float
    rolling_mean_24: float
    rolling_std_24: float
    month_cos: float
    day_of_week_sin: float
    month_sin: float
    day_of_week_cos: float
    is_weekend: int


##### ENDPOINT PRINCIPAL

@app.post("/predict")
def predict(data: PredictionInput):

    input_data = pd.DataFrame(
        [{
            "hour_sin": data.hour_sin,
            "hour_cos": data.hour_cos,
            "day_of_week_sin": data.day_of_week_sin,
            "day_of_week_cos": data.day_of_week_cos,
            "month_sin": data.month_sin,
            "month_cos": data.month_cos,
            "is_weekend": data.is_weekend,
            "lag_1": data.lag_1,
            "lag_24": data.lag_24,
            "lag_168": data.lag_168,
            "rolling_mean_3": data.rolling_mean_3,
            "rolling_mean_24": data.rolling_mean_24,
            "rolling_std_24": data.rolling_std_24
        }]
    )

    prediction = model.predict(input_data)[0]

    return {
        "forecast": float(prediction),
        "horizon": "t+1_hour",
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION
    }


##### HEALTH CHECK

@app.get("/")
def root():

    return {
        "status": "ok",
        "service": "Household Power Forecasting API",
        "model": MODEL_NAME,
        "model_version": MODEL_VERSION
    }

@app.get("/monitoring/system")
def monitoring_system():
    """Expone latency, throughput, error rate y disponibilidad."""
    # FastAPI convierte automáticamente este diccionario en una respuesta JSON.
    return system_monitor.get_metrics()
