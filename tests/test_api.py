from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


VALID_INPUT = {
    "lag_1": 1.0,
    "lag_168": 1.0,
    "hour_sin": 0.5,
    "hour_cos": 0.5,
    "lag_24": 1.0,
    "rolling_mean_3": 1.0,
    "rolling_mean_24": 1.0,
    "rolling_std_24": 0.1,
    "month_cos": 0.866,
    "day_of_week_sin": 0.0,
    "month_sin": 0.5,
    "day_of_week_cos": 1.0,
    "is_weekend": 0,
}


def test_predict_valid_request_returns_200():
    response = client.post("/predict", json=VALID_INPUT)

    assert response.status_code == 200


def test_predict_response_schema_is_valid():
    response = client.post("/predict", json=VALID_INPUT)

    assert response.status_code == 200

    data = response.json()

    assert "forecast" in data
    assert "horizon" in data
    assert "model_name" in data
    assert "model_version" in data

    assert isinstance(data["forecast"], (int, float))
    assert isinstance(data["horizon"], str)
    assert isinstance(data["model_name"], str)
    assert isinstance(data["model_version"], str)


def test_predict_invalid_request_returns_422():
    invalid_input = {
        "lag_1": 1.0,
        "hour_sin": 0.5,
    }

    response = client.post("/predict", json=invalid_input)

    assert response.status_code == 422