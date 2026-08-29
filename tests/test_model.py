import mlflow
import mlflow.sklearn
import pandas as pd


MLFLOW_TRACKING_URI = "http://127.0.0.1:5000"
MODEL_NAME = "random_forest_feature_set_b"
MODEL_VERSION = "1"


def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    model_uri = f"models:/{MODEL_NAME}/{MODEL_VERSION}"

    return mlflow.sklearn.load_model(model_uri)


def create_valid_input():
    return pd.DataFrame([{
        "hour_sin": 0.5,
        "hour_cos": 0.5,
        "day_of_week_sin": 0.0,
        "day_of_week_cos": 1.0,
        "month_sin": 0.5,
        "month_cos": 0.866,
        "is_weekend": 0,
        "lag_1": 1.0,
        "lag_24": 1.0,
        "lag_168": 1.0,
        "rolling_mean_3": 1.0,
        "rolling_mean_24": 1.0,
        "rolling_std_24": 0.1,
    }])


def test_valid_input_returns_valid_prediction():
    model = load_model()
    input_data = create_valid_input()

    prediction = model.predict(input_data)[0]

    assert prediction is not None
    assert isinstance(prediction, (int, float))
    assert prediction >= 0