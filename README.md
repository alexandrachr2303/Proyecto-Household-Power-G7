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
14 passed
```

| Área      | Pruebas | Resultado      |
| --------- | ------: | -------------- |
| Datos     |       5 | ✅ 5 passed     |
| Modelo    |       1 | ✅ 1 passed     |
| API       |       3 | ✅ 3 passed     |
| Monitoreo |       5 | ✅ 5 passed     |
| **Total** |  **14** | **✅ 14 passed** |

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

# O. Monitoreo

El monitoreo se separó en las tres dimensiones solicitadas. Los reportes se guardan
como JSON para que sea fácil revisarlos durante la demostración.

## Preparación después de clonar el repositorio

Los siguientes comandos deben ejecutarse desde PowerShell en la carpeta raíz del
proyecto, es decir, en la misma carpeta donde se encuentra `requirements.txt`.

```powershell
git clone <URL_DEL_REPOSITORIO>
cd Proyecto-Household-Power-G7
```

Se recomienda utilizar un entorno virtual para que las librerías del proyecto no se
mezclen con otras instalaciones de Python:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell no permite activar el entorno virtual, se puede habilitar únicamente
para la terminal actual y volver a intentarlo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Para comprobar que `pytest` quedó instalado:

```powershell
python -m pytest --version
```

Si aparece el mensaje `pytest no se reconoce` o `No module named pytest`, instalarlo
con el mismo Python que ejecutará las pruebas:

```powershell
python -m pip install pytest
```

Se recomienda usar `python -m pytest` en lugar de escribir solamente `pytest`. De
esta manera se utiliza el paquete instalado dentro del entorno virtual activo.

## O1. System Monitoring

La API mide automáticamente cada request mediante un middleware. Las métricas se
consultan en:

```text
GET /monitoring/system
```

Ejemplo:

```json
{
  "latency_avg_ms": 18.42,
  "throughput_requests_per_second": 0.031,
  "error_rate": 0.0,
  "availability": 1.0,
  "total_requests": 5,
  "uptime_seconds": 161.2
}
```

* **Latency:** promedio de milisegundos que tarda la API en responder.
* **Throughput:** cantidad de requests atendidos por segundo desde que inició el servicio.
* **Error rate:** proporción de requests que terminaron con error del servidor (HTTP 5xx).
* **Availability:** proporción de requests sin errores 5xx (`1 - error_rate`).

Estas métricas se almacenan en memoria y se reinician cuando se reinicia el
contenedor. Es una solución suficiente para la simulación académica; en producción
se enviarían a una herramienta persistente como Prometheus.

Para probarlo, primero se debe iniciar MLflow y la API siguiendo las secciones
anteriores del README. Con la API disponible en el puerto 8000, realizar algunas
predicciones desde Swagger o con `POST /predict` y consultar las métricas con:

```powershell
Invoke-RestMethod -Method Get -Uri http://localhost:8000/monitoring/system
```

También se puede abrir directamente en el navegador:

```text
http://localhost:8000/monitoring/system
```

## O2. Data Monitoring

`src/monitoring/data_monitor.py` compara una muestra de referencia contra un batch
de producción mediante **Population Stability Index (PSI)**. Los intervalos se
calculan solamente con referencia para evitar usar información futura.

```powershell
python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/production_batch.csv `
  --columns Global_active_power Voltage Global_intensity
```

El repositorio incluye dos archivos pequeños para que el comando pueda ejecutarse
sin descargar nuevamente el dataset completo:

```text
examples/monitoring/reference.csv
examples/monitoring/production_batch.csv
```

El segundo archivo contiene un cambio fuerte e intencional en las distribuciones,
por lo que el resultado esperado para las tres variables es `ALERT`. Al finalizar
se crea automáticamente:

```text
reports/data_monitoring.json
```

El resultado queda en `reports/data_monitoring.json`. La interpretación utilizada es:

| PSI | Estado | Interpretación para este proyecto |
| ---: | --- | --- |
| menor a 0.10 | OK | Cambio pequeño |
| 0.10 a 0.2499 | WARNING | Revisar el batch y su calidad |
| 0.25 o mayor | ALERT | Cambio importante en la distribución |

Los límites son reglas prácticas, no leyes universales. Se eligieron porque permiten
distinguir cambios leves, moderados y fuertes en la simulación. Antes de usarlos en
producción deberían calibrarse con varios periodos históricos. El cálculo también
considera cambios en la proporción de valores faltantes y reporta columnas ausentes.

## O3. Model Monitoring

Como el problema es forecasting, se monitorean **MAE** y **RMSE** por batch cuando
ya se conoce el consumo real. El CSV debe tener, como mínimo, las columnas `batch`,
`actual` y `forecast`.

```powershell
python -m src.monitoring.model_monitor --input examples/monitoring/predictions_by_batch.csv
```

El archivo `examples/monitoring/predictions_by_batch.csv` está incluido en el
repositorio. Contiene las columnas:

| Columna | Contenido |
| --- | --- |
| `batch` | Nombre del periodo de referencia o producción |
| `actual` | Consumo real observado |
| `forecast` | Pronóstico generado por el modelo |

El ejemplo simula un aumento progresivo del error. Al finalizar se crea:

```text
reports/model_monitoring.json
```

El resultado queda en `reports/model_monitoring.json`. El primer batch funciona
como referencia. Un aumento del MAE menor a 20% se marca `OK`, de 20% a 49.99%
se marca `WARNING` y desde 50% se marca `ALERT`. Estos porcentajes son iniciales y
deben ajustarse cuando exista más historial y se conozca el error aceptable para el
negocio. Un cambio en PSI no implica necesariamente que MAE o RMSE empeoren, por
eso datos y modelo se observan por separado.

## Pruebas de monitoreo

Después de instalar las dependencias, ejecutar únicamente las pruebas de monitoreo:

```powershell
python -m pytest tests/test_monitoring.py -v
```

El resultado esperado es:

```text
5 passed
```

Para ejecutar todas las pruebas del proyecto:

```powershell
python -m pytest tests/ -v
```

Las pruebas verifican las cuatro métricas del sistema, un caso con y sin drift,
una columna ausente, el cálculo de MAE/RMSE y la separación de resultados por batch.

## Recorrido corto para la demostración

Una vez instaladas las dependencias, el bloque de monitoreo se puede demostrar con
estos tres pasos:

```powershell
python -m pytest tests/test_monitoring.py -v

python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/production_batch.csv `
  --columns Global_active_power Voltage Global_intensity

python -m src.monitoring.model_monitor --input examples/monitoring/predictions_by_batch.csv
```

Los dos últimos comandos imprimen el resultado en la terminal y guardan una copia
en `reports/`. Los ejemplos son simulaciones y no modifican el dataset original.

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
| Pruebas automatizadas  | ✅ 14 |
| Monitoreo de sistema | ✅ |
| Monitoreo de datos (PSI) | ✅ |
| Monitoreo del modelo (MAE/RMSE) | ✅ |

---


```

