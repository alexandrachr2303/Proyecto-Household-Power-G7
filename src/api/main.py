from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow
import mlflow.sklearn


# ==========================================
# CONFIGURACIÓN
# ==========================================

MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"

MODEL_NAME = "random_forest_feature_set_b"
MODEL_VERSION = "1"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


# ==========================================
# CARGAR MODELO
# ==========================================

model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"

model = mlflow.sklearn.load_model(model_uri)


# ==========================================
# API
# ==========================================

app = FastAPI(
    title="Household Power Forecasting API",
    description="API para predicción de consumo eléctrico a una hora.",
    version="1.0.0"
)


# ==========================================
# INPUT
# ==========================================

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


# ==========================================
# ENDPOINT PRINCIPAL
# ==========================================

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


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def root():

    return {
        "status": "ok",
        "service": "Household Power Forecasting API",
        "model": MODEL_NAME,
        "model_version": MODEL_VERSION
    }