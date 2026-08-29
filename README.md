# Proyecto Household Power G7


Proyecto de Machine Learning para el pronóstico del consumo eléctrico utilizando el dataset **Household Electric Power Consumption**.

El proyecto implementa un flujo completo de Machine Learning que incluye:

* Ingesta y análisis de datos.
* Data Quality.
* Análisis exploratorio de datos (EDA).
* Feature Engineering para series temporales.
* Modelado predictivo.
* Tracking de experimentos con MLflow.
* Registro y versionado del modelo.
* API de inferencia con FastAPI.
* Contenerización mediante Docker.
* Pruebas automatizadas con pytest.

---

## Tecnologías utilizadas

* Python 3.13
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Statsmodels
* MLflow
* FastAPI
* Uvicorn
* Docker
* Pytest

---

## Estructura del proyecto

```text
Proyecto-Household-Power-G7/
│
├── data/
│
├── src/
│   ├── ingestion/
│   ├── tracking/
│   └── api/
│       └── main.py
│
├── 01_ingestion_data_quality_eda.ipynb
├── 02_timeseries_feature_engineering_modeling.ipynb
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── README.md
└── .gitignore
```

---

# MLflow

MLflow se utiliza para registrar los experimentos, métricas, artefactos y versiones del modelo.

El modelo registrado utilizado por la API es:

```text
random_forest_feature_set_b
```

Versión:

```text
1
```

Para levantar el servidor MLflow:

```powershell
Entrar al proyecto 
cd .\Proyecto-Household-Power-G7

Activar el entorno virtual 
.\.venv\Scripts\Activate.ps1

Levantar el servidor
mlflow server --host 127.0.0.1 --port 5000
```

MLflow queda disponible en:

```text
http://127.0.0.1:5000
```

---

# API de inferencia

La API fue implementada utilizando **FastAPI**.

El archivo principal se encuentra en:

```text
src/api/main.py
```

Para ejecutar la API directamente:

```powershell
uvicorn src.api.main:app --reload --port 8000
```

La documentación interactiva de FastAPI está disponible en:

```text
http://localhost:8000/docs
```

---

## Endpoint `/predict`

La API dispone del siguiente endpoint:

```text
POST /predict
```

El modelo realiza un pronóstico del consumo eléctrico para una hora futura.

Las variables utilizadas son:

```text
hour_sin
hour_cos
day_of_week_sin
day_of_week_cos
month_sin
month_cos
is_weekend
lag_1
lag_24
lag_168
rolling_mean_3
rolling_mean_24
rolling_std_24
```

### Ejemplo de entrada

```json
{
  "lag_1": 0,
  "lag_168": 0,
  "hour_sin": 0,
  "hour_cos": 0,
  "lag_24": 0,
  "rolling_mean_3": 0,
  "rolling_mean_24": 0,
  "rolling_std_24": 0,
  "month_cos": 0,
  "day_of_week_sin": 0,
  "month_sin": 0,
  "day_of_week_cos": 0,
  "is_weekend": 0
}
```

### Respuesta

```json
{
  "forecast": 0.2980160461835182,
  "horizon": "t+1_hour",
  "model_name": "random_forest_feature_set_b",
  "model_version": "1"
}
```

La prueba realizada obtuvo:

```text
HTTP 200 OK
```

---

# Docker

El modelo y la API pueden ejecutarse dentro de un contenedor Docker para garantizar la reproducibilidad del servicio.

## Comprobar Docker

```powershell
docker version
```

Docker Desktop debe estar ejecutándose.

## Construir la imagen

Desde la carpeta raíz del proyecto:

```powershell
docker build -t grupo7-mlops .
```

## Comprobar comunicación con el equipo anfitrión

```powershell
docker run --rm grupo7-mlops python -c "import socket; print(socket.gethostbyname('host.docker.internal'))"
```

## Ejecutar el servicio

```powershell
cd C:\Git\Household-power-g7\Proyecto-Household-Power-G7
```

```powershell
docker run --rm -p 8000:8000 -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 grupo7-mlops
```

La API queda disponible en:

```text
http://localhost:8000
```

La documentación Swagger:

```text
http://localhost:8000/docs
```

## . Pruebas

Se implementó una suite de pruebas automatizadas utilizando **pytest** para verificar la calidad de los datos, el funcionamiento del modelo y el comportamiento de la API de inferencia.

### .1 Pruebas de datos

Se realizaron pruebas para validar que los datos utilizados por el modelo cumplan con las condiciones esperadas:

* **Esquema:** verifica que la estructura del conjunto de datos sea la esperada.
* **Tipos:** verifica que las variables tengan los tipos de datos correctos.
* **Rangos:** verifica que los valores se encuentren dentro de los rangos permitidos.
* **Valores faltantes:** verifica que no existan valores `missing` en las variables correspondientes.
* **Variables obligatorias:** verifica que todas las variables requeridas estén presentes.

Archivo:

```text
tests/test_data.py
```

**Resultado:**

```text
5 passed
```

### N.2 Prueba del modelo

Se verificó que un conjunto de datos de entrada válido pueda ser procesado correctamente por el modelo registrado en MLflow.

La prueba comprueba:

```text
Input válido → Modelo → Prediction válida
```

Se valida que la predicción:

* exista;
* sea numérica;
* sea válida para el pronóstico.

Archivo:

```text
tests/test_model.py
```

**Resultado:**

```text
1 passed
```

### N.3 Pruebas de la API

Se realizaron pruebas sobre el endpoint:

```text
POST /predict
```

#### Request válido

Se comprueba que:

```text
Request válido → HTTP 200 → Response válida
```

Además, se verifica que la respuesta contenga los siguientes campos:

```text
forecast
horizon
model_name
model_version
```

#### Request inválido

Se envía un request incompleto para comprobar que la API rechace correctamente la entrada:

```text
Request inválido → HTTP 422
```

Archivo:

```text
tests/test_api.py
```

**Resultado:**

```text
3 passed
```

### N.4 Ejecución de las pruebas

Para ejecutar todas las pruebas desde la raíz del proyecto:

```powershell
pytest tests/ -v
```

### N.5 Resultado final

La suite completa de pruebas produjo el siguiente resultado:

```text
9 passed
```

| Área      | Pruebas | Resultado      |
| --------- | ------: | -------------- |
| Datos     |       5 | ✅ 5 passed     |
| Modelo    |       1 | ✅ 1 passed     |
| API       |       3 | ✅ 3 passed     |
| **Total** |   **9** | **✅ 9 passed** |

Con estas pruebas se verifica el cumplimiento de los requisitos de validación de datos, funcionamiento del modelo y consumo de la API de inferencia.


---

# Ejecución del proyecto

## Paso 1 — Entrar al proyecto

```powershell
cd .\Proyecto-Household-Power-G7
```

## Paso 2 — Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

## Paso 3 — Levantar MLflow

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

## Paso 4 — Construir la imagen Docker

En otra terminal:

```powershell
cd C:\Git\Household-power-g7\Proyecto-Household-Power-G7
```

```powershell
docker build -t grupo7-mlops .
```

## Paso 5 — Ejecutar la API mediante Docker

```powershell
docker run --rm -p 8000:8000 -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 grupo7-mlops
```

## Paso 6 — Abrir Swagger

Ingresar en:

```text
http://localhost:8000/docs
```

Seleccionar:

```text
POST /predict
```

Presionar **Try it out**, ingresar los datos y ejecutar la predicción.

---

# Comunicación Docker - MLflow

Cuando la API se ejecuta directamente en el equipo, MLflow puede utilizar:

```text
127.0.0.1:5000
```

Sin embargo, dentro de Docker `127.0.0.1` representa al propio contenedor.

Por esta razón, cuando la API se ejecuta dentro de Docker se utiliza:

```text
host.docker.internal:5000
```

Esto permite que el contenedor se comunique con el servidor MLflow ejecutándose en el equipo anfitrión.

---

# Comandos de referencia

### Entrar al proyecto

```powershell
cd .\Proyecto-Household-Power-G7
```

### Activar entorno

```powershell
.\.venv\Scripts\Activate.ps1
```

### MLflow

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

### FastAPI

```powershell
uvicorn src.api.main:app --reload --port 8000
```

### Docker

```powershell
docker version
```

```powershell
docker build -t grupo7-mlops .
```

```powershell
docker run --rm grupo7-mlops python -c "import socket; print(socket.gethostbyname('host.docker.internal'))"
```

```powershell
docker run --rm -p 8000:8000 -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 grupo7-mlops
```
### Pruebas

```powershell
cd .\Proyecto-Household-Power-G7
```
```Activar el entorno
.\.venv\Scripts\Activate.ps1
```
```prueba de datos
pytest tests/test_data.py -v
```
```prueba de modelos
pytest tests/test_model.py -v
```
```pruebas de API
pytest tests/test_api.py -v
```

```suite completa
pytest tests/ -v
```

---

# Estado del proyecto

| Componente           | Estado |
| -------------------- | ------ |
| Ingesta              | ✅      |
| Data Quality         | ✅      |
| EDA                  | ✅      |
| Feature Engineering  | ✅      |
| Modelado             | ✅      |
| MLflow Tracking      | ✅      |
| Model Registry       | ✅      |
| FastAPI              | ✅      |
| Endpoint `/predict`  | ✅      |
| Dockerfile           | ✅      |
| `.dockerignore`      | ✅      |
| Docker Build         | ✅      |
| Docker Run           | ✅      |
| Prueba de `/predict` | ✅      |
| Pruebas automatizadas  | ✅ 9/9 |

---


```

