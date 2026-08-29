import pandas as pd


# Variables que utiliza el modelo
REQUIRED_COLUMNS = [
    "hour_sin",
    "hour_cos",
    "day_of_week_sin",
    "day_of_week_cos",
    "month_sin",
    "month_cos",
    "is_weekend",
    "lag_1",
    "lag_24",
    "lag_168",
    "rolling_mean_3",
    "rolling_mean_24",
    "rolling_std_24",
]


def create_valid_dataframe():
    """Crea un registro válido para las pruebas."""
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


def test_schema():
    """Verifica que estén todas las variables requeridas."""
    df = create_valid_dataframe()

    assert list(df.columns) == REQUIRED_COLUMNS


def test_types():
    """Verifica que las variables sean numéricas."""
    df = create_valid_dataframe()

    for column in REQUIRED_COLUMNS:
        assert pd.api.types.is_numeric_dtype(df[column])


def test_ranges():
    """Verifica rangos de las variables transformadas."""
    df = create_valid_dataframe()

    # Variables seno/coseno deben estar entre -1 y 1
    cyclical_columns = [
        "hour_sin",
        "hour_cos",
        "day_of_week_sin",
        "day_of_week_cos",
        "month_sin",
        "month_cos",
    ]

    for column in cyclical_columns:
        assert df[column].between(-1, 1).all()

    # is_weekend debe ser 0 o 1
    assert df["is_weekend"].isin([0, 1]).all()

    # Variables de consumo no deben ser negativas
    consumption_columns = [
        "lag_1",
        "lag_24",
        "lag_168",
        "rolling_mean_3",
        "rolling_mean_24",
        "rolling_std_24",
    ]

    for column in consumption_columns:
        assert (df[column] >= 0).all()


def test_missing_values():
    """Verifica que no existan valores missing."""
    df = create_valid_dataframe()

    assert not df[REQUIRED_COLUMNS].isnull().any().any()


def test_required_variables():
    """Verifica que todas las variables obligatorias estén presentes."""
    df = create_valid_dataframe()

    for column in REQUIRED_COLUMNS:
        assert column in df.columns