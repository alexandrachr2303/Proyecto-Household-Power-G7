# Proyecto Household Power G7

## 1. Business Problem

El proyecto tiene como objetivo desarrollar un modelo de Machine Learning para realizar el pronóstico del consumo eléctrico de un hogar utilizan (TERMINAR)

---

## 2. Dataset

(REVISAR)
El proyecto utiliza el dataset **Household Electric Power Consumption**, correspondiente al consumo eléctrico de un hogar registrado a una frecuencia original de un minuto.

El dataset contiene las siguientes variables principales:

* `Date`
* `Time`
* `Global_active_power`
* `Global_reactive_power`
* `Voltage`
* `Global_intensity`
* `Sub_metering_1`
* `Sub_metering_2`
* `Sub_metering_3`

El periodo de los datos utilizados comprende desde:

```text
2006-12-16 17:24:00
```

hasta:

```text
2010-11-26 21:02:00
```

Para el modelado, los datos originales fueron agregados de una frecuencia de 1 minuto a 1 hora.

Después de la agregación temporal se obtuvo un conjunto de datos horario de:

```text
33,195 observaciones
```

La variable objetivo corresponde a:

```text
Global_active_power
```

El modelado utiliza una división cronológica:

```text
Train       → 70%
Validation  → 15%
Test        → 15%
```

Cantidad de observaciones:

```text
Train       → 23,236
Validation  → 4,979
Test        → 4,980
```

La división cronológica permite evitar el uso de información futura durante el entrenamiento.

Los datos originales no forman parte del control de versiones debido a su tamaño.

---
# 3. Architecture

El proyecto implementa un flujo de Machine Learning para forecasting de consumo eléctrico, desde la ingesta y preparación de los datos hasta el despliegue, monitoreo y estrategia de reentrenamiento.

Cada componente representado en la arquitectura corresponde a un componente implementado dentro del repositorio.

## Technical Architecture

```
Dataset
    ↓
Data Ingestion
src/ingestion/ingest.py
    ↓
Data Quality
01_ingestion_data_quality_eda.ipynb
    ↓
EDA
01_ingestion_data_quality_eda.ipynb
    ↓
Feature Engineering
02_timeseries_feature_engineering_modeling.ipynb
    ↓
Training Quality Gate
src/monitoring/quality_monitor.py
    ↓
Train / Validation / Test
    ↓
Model Training
02_timeseries_feature_engineering_modeling.ipynb
    ↓
MLflow Experiment Tracking
src/tracking/mlflow_config.py
    ↓
MLflow Model Registry
random_forest_feature_set_b
    ↓
FastAPI
src/api/main.py
    ↓
Docker
Dockerfile
    ↓
Monitoring
    ├── System Monitoring
    │   src/monitoring/system_monitor.py
    │
    ├── Data Monitoring
    │   src/monitoring/data_monitor.py
    │
    ├── Model Monitoring
    │   src/monitoring/model_monitor.py
    │
    └── Data Quality Monitoring
        src/monitoring/quality_monitor.py
                ↓
        Retraining Strategy
        src/monitoring/retraining_strategy.py

```

---

## 4. Repository Structure

La estructura implementada incluye los siguientes componentes principales:

```text
Proyecto-Household-Power-G7/
│
├── data/
│   └── raw/
│
├── examples/
│   └── monitoring/
│       ├── predictions_by_batch.csv
│       ├── production_batch.csv
│       ├── reference.csv
│       ├── drift_simulation/
│       │   ├── batch_1.csv
│       │   └── batch_2.csv
│       └── quality_simulation/
│           └── contaminated_batch.csv
│
├── reports/
│   ├── data_monitoring.json
│   ├── drift_batch_1.json
│   ├── drift_batch_2.json
│   ├── model_monitoring.json
│   ├── quality_contamination.json
│   ├── retraining_decision.json
│   ├── retraining_monitor.json
│   └── retraining_no_drift.json
│
├── src/
│   ├── api/
│   │   └── main.py
│   │
│   ├── ingestion/
│   │   └── ingest.py
│   │
│   ├── monitoring/
│   │   ├── data_monitor.py
│   │   ├── model_monitor.py
│   │   ├── quality_monitor.py
│   │   ├── retraining_strategy.py
│   │   └── system_monitor.py
│   │
│   └── tracking/
│       ├── mlflow_config.py
│       └── test_mlflow.py
│
├── tests/
│   ├── test_api.py
│   ├── test_data.py
│   ├── test_model.py
│   └── test_monitoring.py
│
├── 01_ingestion_data_quality_eda.ipynb
├── 02_timeseries_feature_engineering_modeling.ipynb
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .python-version
├── requirements.txt
└── README.md
```

Los datos originales se mantienen fuera del control de versiones mediante `.gitignore`.

Descripción de los componentes principales:

* `data/`: contiene los datos utilizados por el proyecto. Los datos originales no se versionan.
* `examples/monitoring/`: contiene datasets pequeños utilizados para demostrar el funcionamiento del monitoreo, drift y contaminación de calidad.
* `reports/`: contiene los resultados estructurados generados por los diferentes módulos de monitoreo y la estrategia de reentrenamiento.
* `src/ingestion/`: contiene el proceso reproducible de ingestión de datos.
* `src/monitoring/`: contiene los componentes de monitoreo de sistema, datos, modelo, calidad y estrategia de reentrenamiento.
* `src/api/`: contiene la API de inferencia desarrollada con FastAPI.
* `src/tracking/`: contiene la configuración y pruebas relacionadas con MLflow.
* `tests/`: contiene las pruebas automatizadas del proyecto.
* `01_ingestion_data_quality_eda.ipynb`: notebook correspondiente a ingestión, calidad de datos y análisis exploratorio.
* `02_timeseries_feature_engineering_modeling.ipynb`: notebook correspondiente al análisis de series temporales, ingeniería de características, entrenamiento, evaluación y selección del modelo.
* `Dockerfile`: define la imagen Docker utilizada para ejecutar la aplicación.
* `requirements.txt`: contiene las dependencias Python necesarias para reproducir el proyecto.
* `.gitignore`: excluye datos, entornos virtuales, cachés y artefactos locales que no deben formar parte del repositorio.

---

## 5. Installation

### Clonar el repositorio

```powershell
git clone <URL_DEL_REPOSITORIO>
```

Entrar al proyecto:

```powershell
cd Proyecto-Household-Power-G7
```

### Crear el entorno virtual

```powershell
python -m venv .venv
```

### Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell no permite activar el entorno:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar dependencias

```powershell
python -m pip install --upgrade pip
```

```powershell
python -m pip install -r requirements.txt
```

Las dependencias utilizadas por el proyecto se encuentran en:

```text
requirements.txt
```

No se requieren dependencias adicionales para los módulos de monitoreo implementados.

---

## 6. Data Ingestion

La ingesta reproducible se encuentra en:

```text
src/ingestion/ingest.py
```

La ejecución se realiza mediante:

```powershell
python src/ingestion/ingest.py
```

El proceso de ingesta mantiene separado el proceso reproducible de carga y preparación inicial de datos del análisis realizado posteriormente en los notebooks.

El primer notebook:

```text
01_ingestion_data_quality_eda.ipynb
```

contiene el análisis de ingestión, calidad de datos y EDA.

Los datos originales se mantienen fuera del control de versiones debido a su tamaño.

---

## 7. Training

El segundo notebook:

```text
02_timeseries_feature_engineering_modeling.ipynb
```

contiene el proceso de preparación de la serie temporal, ingeniería de características, división cronológica, entrenamiento y evaluación de los modelos.

El problema se aborda mediante un pronóstico **one-step ahead**, es decir, se predice el consumo correspondiente a:

```text
t + 1 hora
```

La división de los datos se realiza cronológicamente para evitar utilizar información futura durante el entrenamiento.

### Baseline

Se utilizó **Naive Persistence** como baseline:

```text
ŷ_t = y_(t-1)
```

Resultados de validación:

```text
MAE  = 0.4669
RMSE = 0.6947
```

### Modelos evaluados

Se evaluaron diferentes configuraciones utilizando Feature Set A y Feature Set B.

El criterio principal de selección fue:

```text
RMSE
```

utilizando:

```text
MAE
```

como métrica complementaria.

El modelo seleccionado fue:

```text
RandomForestRegressor
Feature Set B
```

con la siguiente configuración:

```text
n_estimators = 200
max_depth = 10
min_samples_leaf = 2
random_state = 42
```

El modelo final fue posteriormente registrado en MLflow.

---

## 8. MLflow

MLflow se utiliza para registrar los experimentos, parámetros, métricas, artefactos y versiones de los modelos.

### Experimento principal

El experimento principal utilizado en el proyecto es:

```text
household-power-forecasting
```

### Modelo final

El modelo final seleccionado y registrado en MLflow es:

```text
random_forest_feature_set_b
```

Versión registrada:

```text
1
```

El modelo final corresponde a un `RandomForestRegressor` utilizando **Feature Set B**.

### Levantar el servidor MLflow

Desde la carpeta raíz del proyecto:

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

MLflow queda disponible en:

```text
http://127.0.0.1:5000
```

### Información registrada

Para el modelo final se registran, entre otros:

* Algoritmo utilizado.
* Feature Set.
* Número de variables.
* Hiperparámetros.
* Semilla aleatoria.
* Versión de los datos.
* Cantidad de observaciones de entrenamiento y prueba.
* Horizonte de predicción.
* Frecuencia temporal.
* MAE.
* RMSE.
* Mejora respecto al baseline.
* Configuración del modelo.
* Variables utilizadas.
* Modelo entrenado.

### Artefactos registrados

También se registran como artefactos:

* Gráfico de pronóstico.
* Gráfico de residuales.
* Importancia de variables.
* Configuración de features.
* Configuración del modelo.

### Criterio de selección del modelo

El criterio principal de selección fue **RMSE**, utilizando **MAE** como métrica complementaria.

### Resultados del modelo final

El modelo final obtuvo en el conjunto de prueba:

```text
MAE  = 0.3254
RMSE = 0.4709
```

Frente al baseline de persistencia:

```text
MAE  = 0.3859
RMSE = 0.5843
```

La mejora obtenida fue aproximadamente:

```text
MAE  = 15.67%
RMSE = 19.42%
```

### MLflow Model Registry

El modelo seleccionado fue registrado en MLflow Model Registry con el nombre:

```text
random_forest_feature_set_b
```

Versión:

```text
1
```

Para representar el ciclo de vida solicitado por el proyecto se utilizaron aliases:

| Alias        | Versión |
| ------------ | ------: |
| `candidate`  |       1 |
| `validation` |       1 |
| `production` |       1 |

Los tres aliases apuntan actualmente a la versión 1.

Esto representa el estado actual del modelo dentro del Registry. No se presentan como transiciones históricas independientes, sino como aliases utilizados para representar las etapas:

```text
Candidate → Validation → Production
```

La API consume el modelo registrado en MLflow.

---

## 9. Docker

El modelo y la API pueden ejecutarse dentro de un contenedor Docker para garantizar la reproducibilidad del servicio y aislar las dependencias de ejecución.

### Comprobar Docker

```powershell
docker version
```

Docker Desktop debe estar ejecutándose.

### Construir la imagen

Desde la carpeta raíz del proyecto:

```powershell
docker build -t household-power-g7 .
```

La imagen utilizada en el proyecto es:

```text
household-power-g7:latest
```

### Comprobar comunicación con el equipo anfitrión

Para verificar que el contenedor puede resolver el host utilizado para comunicarse con MLflow:

```powershell
docker run --rm household-power-g7 python -c "import socket; print(socket.gethostbyname('host.docker.internal'))"
```

### Ejecutar el servicio

Desde la carpeta del proyecto:

```powershell
docker run --rm -p 8000:8000 -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 household-power-g7
```

La API queda disponible en:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

### Comunicación Docker - MLflow

Cuando la API se ejecuta directamente en el equipo anfitrión, MLflow puede utilizar:

```text
127.0.0.1:5000
```

Sin embargo, dentro de Docker:

```text
127.0.0.1
```

representa al propio contenedor.

Por esta razón, cuando la API se ejecuta dentro de Docker se utiliza:

```text
host.docker.internal:5000
```

Esto permite que el contenedor se comunique con el servidor MLflow que se encuentra ejecutándose en el equipo anfitrión.

---

## 10. API

La API fue implementada utilizando **FastAPI**.

### Archivo principal

```text
src/api/main.py
```

### Ejecutar la API

Para ejecutar la API directamente desde el entorno virtual:

```powershell
uvicorn src.api.main:app --reload --port 8000
```

La API queda disponible en:

```text
http://localhost:8000
```

La documentación interactiva de FastAPI está disponible en:

```text
http://localhost:8000/docs
```

### Endpoint `/predict`

La API dispone del siguiente endpoint:

```text
POST /predict
```

El modelo realiza un pronóstico del consumo eléctrico para una hora futura:

```text
t+1 hour
```

### Variables utilizadas por Feature Set B

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

### Ejemplo de respuesta

```json
{
  "forecast": 0.2980160461835182,
  "horizon": "t+1_hour",
  "model_name": "random_forest_feature_set_b",
  "model_version": "1"
}
```

La prueba realizada sobre el endpoint obtuvo:

```text
HTTP 200 OK
```

---

## 11. Monitoring

El monitoreo del sistema se implementó en las tres dimensiones solicitadas:

* **O1 — System Monitoring**
* **O2 — Data Monitoring**
* **O3 — Model Monitoring**

Los resultados de los procesos de monitoreo se almacenan en archivos JSON dentro de:

```text
reports/
```

### 11.1 Automated Tests

Se implementó una suite de pruebas automatizadas utilizando `pytest` para verificar la calidad de los datos, el funcionamiento del modelo, la API y los componentes de monitoreo.

#### Pruebas de datos

Las pruebas de datos verifican:

* Esquema: estructura esperada del conjunto de datos.
* Tipos: tipos de datos correctos.
* Rangos: valores dentro de los rangos permitidos.
* Valores faltantes: ausencia de valores missing donde corresponde.
* Variables obligatorias: presencia de las variables requeridas.

Archivo:

```text
tests/test_data.py
```

Resultado:

```text
5 passed
```

#### Prueba del modelo

Se verifica que un conjunto de datos de entrada válido pueda ser procesado correctamente por el modelo.

Se comprueba que la predicción:

* Exista.
* Sea numérica.
* Sea válida para el pronóstico.

Archivo:

```text
tests/test_model.py
```

Resultado:

```text
1 passed
```

#### Pruebas de la API

Se realizaron pruebas sobre:

```text
POST /predict
```

Para un request válido se comprueba:

```text
Request válido
     ↓
HTTP 200
     ↓
Response válida
```

La respuesta debe contener:

* `forecast`
* `horizon`
* `model_name`
* `model_version`

También se envía un request incompleto para verificar que la API rechace correctamente la entrada:

```text
Request inválido
     ↓
HTTP 422
```

Archivo:

```text
tests/test_api.py
```

Resultado:

```text
3 passed
```

#### Pruebas de monitoreo

Las pruebas de monitoreo verifican:

* Métricas de system monitoring.
* Detección de data drift.
* Comportamiento ante columnas faltantes.
* Cálculo de MAE y RMSE.
* Separación de resultados por batch.
* Comportamiento del Quality Gate.
* Aceptación de datos válidos para entrenamiento.
* Bloqueo de datos inválidos para entrenamiento.
* Estados de la estrategia de retraining.

Archivo:

```text
tests/test_monitoring.py
```

Resultado actual:

```text
10 passed
```

Ejecutar:

```powershell
python -m pytest tests\test_monitoring.py -v
```

#### Suite completa

Desde la raíz del proyecto:

```powershell
python -m pytest tests\ -v
```

Las pruebas implementadas actualmente se distribuyen de la siguiente manera:

| Área                   | Pruebas |
| ---------------------- | ------: |
| Datos                  |       5 |
| Modelo                 |       1 |
| API                    |       3 |
| Monitoreo              |      10 |
| **Total implementado** |  **19** |

El resultado final de la ejecución completa debe verificarse ejecutando el comando anterior antes de realizar una entrega.

### 11.2 Data Quality Gate

Se implementó un Quality Gate automático para evitar que datos inválidos lleguen al entrenamiento del modelo.

Módulo:

```text
src/monitoring/quality_monitor.py
```

La función `training_quality_gate()` valida como mínimo:

1. Dataset no vacío.
2. Presencia de las variables requeridas.
3. Ausencia de valores faltantes.
4. Tipos de datos numéricos correctos.
5. Ausencia de filas duplicadas.
6. Ausencia de valores infinitos.

Si se detecta una condición inválida, el proceso se bloquea mediante una excepción `ValueError`.

#### Flujo utilizado antes del entrenamiento

```text
Datos procesados
      ↓
Selección de variables de modelado
      ↓
Eliminación controlada de registros incompletos
      ↓
Training Data Quality Gate
      ↓
Train / Validation / Test
      ↓
Entrenamiento
```

La validación utilizada en el notebook produjo:

```text
Training Data Quality Gate: OK
```

El Quality Gate permite diferenciar la validación de los datos de entrenamiento de la validación de batches de producción utilizados para monitoreo.

### 11.3 O1 — System Monitoring

La API mide automáticamente cada request mediante un middleware.

#### Métricas

Las métricas pueden consultarse mediante:

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

Las métricas representan:

* **Latency:** tiempo promedio de respuesta de la API en milisegundos.
* **Throughput:** cantidad de requests procesados por segundo.
* **Error rate:** proporción de requests que terminaron con errores HTTP 5xx.
* **Availability:** proporción de requests procesados sin errores HTTP 5xx.

Estas métricas se almacenan en memoria y se reinician cuando se reinicia el servicio.

Esta implementación es suficiente para la simulación académica. En un ambiente productivo se podría utilizar una solución persistente como Prometheus.

#### Prueba

Con la API ejecutándose en el puerto 8000:

```powershell
Invoke-RestMethod -Method Get -Uri http://localhost:8000/monitoring/system
```

También puede consultarse desde el navegador:

```text
http://localhost:8000/monitoring/system
```

Antes de consultar las métricas se recomienda realizar algunas solicitudes al endpoint `/predict`, por ejemplo desde Swagger.

### 11.4 O2 — Data Monitoring

Módulo:

```text
src/monitoring/data_monitor.py
```

El módulo compara la distribución de una muestra de referencia con un batch de producción utilizando **Population Stability Index (PSI)**.

Los intervalos utilizados para calcular el PSI se construyen únicamente a partir de los datos de referencia, evitando utilizar información del batch de producción para definir los cortes.

#### Datos utilizados

El repositorio contiene archivos pequeños destinados a la demostración:

```text
examples/monitoring/reference.csv
examples/monitoring/drift_simulation/batch_1.csv
examples/monitoring/drift_simulation/batch_2.csv
```

`reference.csv` representa la distribución de referencia.

`batch_1.csv` representa un batch de producción sin cambio significativo respecto a la referencia.

`batch_2.csv` representa un batch de producción al que se aplicó una modificación controlada para simular drift.

#### Prueba de un batch estable

```powershell
python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_1.csv `
  --columns Global_active_power `
  --output reports/data_monitoring.json
```

Resultado:

```json
{
  "Global_active_power": {
    "psi": 0.0,
    "status": "OK"
  }
}
```

#### Prueba de drift

```powershell
python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_2.csv `
  --columns Global_active_power `
  --output reports/drift_batch_2.json
```

Resultado:

```json
{
  "Global_active_power": {
    "psi": 8.2831,
    "status": "ALERT"
  }
}
```

Estos resultados demuestran que el sistema puede diferenciar un batch estable de otro con un cambio importante en la distribución.

#### Interpretación del PSI

| PSI             | Estado  | Interpretación                       |
| --------------- | ------- | ------------------------------------ |
| `< 0.10`        | OK      | Cambio pequeño                       |
| `0.10 a < 0.25` | WARNING | Cambio moderado; requiere revisión   |
| `≥ 0.25`        | ALERT   | Cambio importante; requiere atención |

Estos límites son reglas prácticas definidas para la simulación académica y no valores universales.

En un ambiente productivo deberían calibrarse utilizando datos históricos, comportamiento del modelo y conocimiento del negocio.

El cálculo también considera la proporción de valores faltantes y reporta errores cuando una columna requerida no está presente.

### 11.5 O3 — Model Monitoring

Debido a que el problema corresponde a un modelo de forecasting, el monitoreo del modelo utiliza:

* **MAE (Mean Absolute Error)**
* **RMSE (Root Mean Squared Error)**

Las métricas se calculan por batch cuando ya se dispone del valor real observado.

Módulo:

```text
src/monitoring/model_monitor.py
```

#### Archivo de entrada

El archivo debe contener como mínimo:

| Columna    | Descripción                       |
| ---------- | --------------------------------- |
| `batch`    | Identificador del periodo o batch |
| `actual`   | Consumo eléctrico real observado  |
| `forecast` | Pronóstico generado por el modelo |

#### Ejecución

```powershell
python -m src.monitoring.model_monitor `
  --input examples/monitoring/predictions_by_batch.csv `
  --output reports/model_monitoring.json
```

El primer batch del archivo se utiliza como referencia de desempeño.

El reporte generado se almacena en:

```text
reports/model_monitoring.json
```

#### Resultados de la simulación

La simulación utiliza datos controlados para demostrar el comportamiento del monitoreo:

| Batch     |  MAE | RMSE | Cambio MAE | Cambio RMSE | Estado    |
| --------- | ---: | ---: | ---------: | ----------: | --------- |
| Reference | 0.05 | 0.05 |         0% |          0% | REFERENCE |
| Batch 1   | 0.08 | 0.08 |       +60% |        +60% | ALERT     |
| Batch 2   | 0.20 | 0.20 |      +300% |       +300% | ALERT     |

#### Reglas de clasificación

La decisión del estado considera ambas métricas:

* Si MAE o RMSE aumenta **≥ 50%** → `ALERT`
* Si MAE o RMSE aumenta **≥ 20% y < 50%** → `WARNING`
* Si ninguna métrica alcanza el **20% de aumento** → `OK`

Estos porcentajes son umbrales iniciales definidos para la simulación y deberán calibrarse posteriormente con historial real de desempeño y con el error aceptable para el negocio.

#### Validación de los estados

Además del escenario principal, se realizaron pruebas controladas para comprobar los diferentes estados:

| Caso                    | Resultado |
| ----------------------- | --------- |
| Desempeño estable       | OK        |
| Deterioro moderado      | WARNING   |
| Deterioro significativo | ALERT     |

Por ejemplo:

```text
Referencia: MAE/RMSE = 0.05
Batch:      MAE/RMSE = 0.01
Resultado:  OK
```

Un batch con:

```text
MAE/RMSE = 0.07
```

produce un aumento del 40% y es clasificado como:

```text
WARNING
```

Los batches utilizados en `predictions_by_batch.csv` producen estados `ALERT` debido al deterioro controlado del error.

Estas pruebas son una simulación de monitoreo y no representan métricas reales de producción. Su objetivo es demostrar que el mecanismo de detección funciona correctamente.

### 11.6 P — Simulación de Data Drift

Para demostrar la capacidad de detección de cambios en la distribución de los datos se construyó una simulación progresiva:

```text
REFERENCE
    ↓
BATCH 1 — sin drift significativo
    ↓
BATCH 2 — drift introducido intencionalmente
```

Resultado:

```text
Batch 1 → PSI 0.0000 → OK
Batch 2 → PSI 8.2831 → ALERT
```

Esto demuestra que el sistema es capaz de identificar un cambio importante entre la distribución de referencia y una distribución de producción modificada.

La simulación utiliza archivos pequeños y controlados, por lo que no modifica permanentemente el dataset original.

#### Data Drift ≠ Model Degradation

Es importante distinguir:

```text
Data Drift ≠ Model Degradation
```

Un cambio en la distribución de las variables de entrada no significa automáticamente que el modelo haya perdido desempeño.

Por esta razón, el proyecto monitorea de forma independiente:

```text
Distribución de los datos
        ↓
       PSI

Desempeño del modelo
        ↓
     MAE / RMSE
```

Los umbrales utilizados para PSI y deterioro del modelo son criterios definidos para la demostración académica y deben calibrarse en un ambiente productivo.

### 11.7 Q — Simulación de contaminación de Data Quality

Debido a que un dataset real no necesariamente contiene todos los problemas de calidad posibles, se implementó una simulación controlada de contaminación sobre un batch de producción.

El objetivo es comprobar que el sistema de validación sea capaz de:

```text
Detectar → Bloquear → Registrar el incidente
```

La contaminación se realizó únicamente sobre una copia de prueba, sin modificar permanentemente los datasets originales.

#### Batch contaminado

Archivo utilizado:

```text
examples/monitoring/quality_simulation/contaminated_batch.csv
```

Archivo original de producción:

```text
examples/monitoring/production_batch.csv
```

El archivo original no fue modificado.

#### Problemas simulados

El batch contaminado incorpora los seis tipos de problemas requeridos:

| Problema            | Simulación                                  | Resultado |
| ------------------- | ------------------------------------------- | --------- |
| Missing values      | `Voltage` contiene un valor vacío           | Detectado |
| Duplicated rows     | Se duplicó una fila                         | Detectado |
| Extreme outlier     | `Global_active_power = 9999`                | Detectado |
| Incorrect datatype  | `Voltage = "INVALID"`                       | Detectado |
| Unknown category    | `quality_category = "UNKNOWN_NEW_CATEGORY"` | Detectado |
| Schema modification | Se agregó la columna `quality_category`     | Detectado |

#### Ejecución

```powershell
python -m src.monitoring.quality_monitor `
  --input examples/monitoring/quality_simulation/contaminated_batch.csv `
  --output reports/quality_contamination.json
```

#### Resultado

El sistema clasificó el batch como:

```json
{
  "status": "BLOCKED",
  "incident_count": 6
}
```

Se detectaron los siguientes incidentes:

```text
schema_modification
missing_values
incorrect_datatype
duplicated_rows
extreme_outlier
unknown_category
```

El resultado queda registrado automáticamente en:

```text
reports/quality_contamination.json
```

#### Flujo implementado

```text
Batch contaminado
       ↓
    Detecta
       ↓
    Bloquea
       ↓
Registra incidente
```

#### Integridad del dataset original

La simulación se realizó sobre:

```text
examples/monitoring/quality_simulation/contaminated_batch.csv
```

El archivo:

```text
examples/monitoring/production_batch.csv
```

permanece sin modificaciones.

De esta manera, la contaminación constituye únicamente una prueba del pipeline de Data Quality y no altera permanentemente los datos utilizados por el proyecto.

### 11.8 R — Estrategia de Retraining

El proyecto implementa una estrategia para decidir cuándo debe considerarse un nuevo entrenamiento del modelo.

Módulo:

```text
src/monitoring/retraining_strategy.py
```

La estrategia distingue entre:

```text
Data Drift
    ≠
Model Degradation
```

Por lo tanto, detectar drift no provoca automáticamente un reentrenamiento.

#### Variables consideradas

La decisión considera conjuntamente:

* PSI
* Cambio porcentual del MAE
* Cambio porcentual del RMSE

#### Reglas utilizadas

El proyecto utiliza inicialmente:

```text
PSI ≥ 0.25
```

como indicador de drift significativo.

Para el desempeño:

```text
MAE o RMSE ≥ 50% de aumento

→ Model Degradation significativa
```

#### Decisión

| Drift | Degradación | Decisión     |
| ----- | ----------- | ------------ |
| No    | No          | `NO_RETRAIN` |
| No    | Sí          | `NO_RETRAIN` |
| Sí    | No          | `MONITOR`    |
| Sí    | Sí          | `RETRAIN`    |

#### Ejemplo: reentrenamiento

```powershell
python -m src.monitoring.retraining_strategy `
  --psi 0.30 `
  --mae-change 60 `
  --rmse-change 60
```

Resultado:

```text
RETRAIN
```

#### Ejemplo: drift sin degradación

```powershell
python -m src.monitoring.retraining_strategy `
  --psi 0.30 `
  --mae-change 10 `
  --rmse-change 10
```

Resultado:

```text
MONITOR
```

#### Ejemplo: degradación sin drift

```powershell
python -m src.monitoring.retraining_strategy `
  --psi 0.05 `
  --mae-change 60 `
  --rmse-change 60
```

Resultado:

```text
NO_RETRAIN
```

Estos umbrales son criterios iniciales para la simulación académica. En producción deberían calibrarse utilizando datos históricos, frecuencia de cambio de los datos y tolerancia de error del negocio.

### 11.9 S — Git Workflow

El proyecto utiliza un flujo de trabajo basado en ramas individuales y Pull Requests.

#### Ramas principales

Las ramas principales utilizadas son:

```text
main
Alexandra
Alejandro
Evelyn
```

#### Flujo utilizado

```text
Rama individual
      ↓
Desarrollo
      ↓
Commit descriptivo
      ↓
Push
      ↓
Pull Request
      ↓
Revisión / Merge
      ↓
main
```

#### Comandos utilizados

Ver ramas:

```powershell
git branch -a
```

Ver historial:

```powershell
git log --oneline --all --decorate -20
```

Crear una rama:

```powershell
git checkout -b nombre-rama
```

Ver estado:

```powershell
git status
```

Agregar cambios:

```powershell
git add .
```

Crear commit:

```powershell
git commit -m "Descripción del cambio"
```

Subir la rama:

```powershell
git push -u origin nombre-rama
```

El historial del proyecto contiene commits descriptivos, ramas individuales, Pull Requests y merges hacia `main`.

Esto permite mantener un historial progresivo y trazable del desarrollo.

---

## 12. Results

### Modelo seleccionado

El mejor modelo seleccionado fue:

```text
RandomForestRegressor
Feature Set B
```

### Configuración

```text
n_estimators = 200
max_depth = 10
min_samples_leaf = 2
random_state = 42
```

### Evaluación final sobre el conjunto de prueba

```text
MAE  = 0.3254
RMSE = 0.4709
```

### Comparación contra el baseline

```text
Baseline MAE  = 0.3859
Modelo MAE    = 0.3254

Baseline RMSE = 0.5843
Modelo RMSE   = 0.4709
```

### Mejoras

```text
MAE  → 15.67%
RMSE → 19.42%
```

El modelo final fue registrado en MLflow como:

```text
random_forest_feature_set_b
```

Versión:

```text
1
```

---

## 13. Team

**AGREGAR**

---

# Ejecución completa del proyecto

## Paso 1 — Clonar el repositorio

```powershell
git clone <URL_DEL_REPOSITORIO>
```

Entrar al proyecto:

```powershell
cd Proyecto-Household-Power-G7
```

## Paso 2 — Crear el entorno virtual

```powershell
python -m venv .venv
```

## Paso 3 — Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell no permite activar el entorno:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Paso 4 — Actualizar pip

```powershell
python -m pip install --upgrade pip
```

## Paso 5 — Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

Para comprobar `pytest`:

```powershell
python -m pytest --version
```

No se requieren dependencias adicionales para los módulos de monitoreo implementados.

---

# Comandos de referencia rápida

## Proyecto

```powershell
cd .\Proyecto-Household-Power-G7
```

## Entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

## Dependencias

```powershell
python -m pip install -r requirements.txt
```

## Ingesta

```powershell
python src/ingestion/ingest.py
```

## MLflow

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

## FastAPI

```powershell
uvicorn src.api.main:app --reload --port 8000
```

## Docker

```powershell
docker version
```

```powershell
docker build -t household-power-g7 .
```

```powershell
docker run --rm household-power-g7 python -c "import socket; print(socket.gethostbyname('host.docker.internal'))"
```

```powershell
docker run --rm -p 8000:8000 -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 household-power-g7
```

## Pruebas

```powershell
python -m pytest tests\test_data.py -v
```

```powershell
python -m pytest tests\test_model.py -v
```

```powershell
python -m pytest tests\test_api.py -v
```

```powershell
python -m pytest tests\test_monitoring.py -v
```

```powershell
python -m pytest tests\ -v
```

## Git

```powershell
git status
```

```powershell
git branch -a
```

```powershell
git log --oneline --all --decorate -20
```

```powershell
git add .
```

```powershell
git commit -m "Descripción del cambio"
```

```powershell
git push -u origin nombre-rama
```

---

# Recorrido corto para la demostración

Para una demostración rápida del proyecto se recomienda:

### 1. Levantar MLflow

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

### 2. Ejecutar la API

En otra terminal:

```powershell
uvicorn src.api.main:app --reload --port 8000
```

### 3. Abrir Swagger

```text
http://localhost:8000/docs
```

### 4. Probar `/predict`

Seleccionar:

```text
POST /predict
```

Presionar:

```text
Try it out
```

Ingresar un request válido y ejecutar.

Resultado esperado:

```text
HTTP 200
```

### 5. Consultar System Monitoring

```powershell
Invoke-RestMethod -Method Get -Uri http://localhost:8000/monitoring/system
```

### 6. Ejecutar Data Monitoring estable

```powershell
python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_1.csv `
  --columns Global_active_power `
  --output reports/data_monitoring.json
```

Resultado:

```text
PSI = 0.0000
STATUS = OK
```

### 7. Ejecutar Data Monitoring con drift

```powershell
python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_2.csv `
  --columns Global_active_power `
  --output reports/drift_batch_2.json
```

Resultado:

```text
PSI = 8.2831
STATUS = ALERT
```

### 8. Ejecutar Model Monitoring

```powershell
python -m src.monitoring.model_monitor `
  --input examples/monitoring/predictions_by_batch.csv `
  --output reports/model_monitoring.json
```

Resultado:

```text
reference → REFERENCE
batch_1   → ALERT
batch_2   → ALERT
```

### 9. Ejecutar Quality Monitoring

```powershell
python -m src.monitoring.quality_monitor `
  --input examples/monitoring/quality_simulation/contaminated_batch.csv `
  --output reports/quality_contamination.json
```

Resultado:

```text
BLOCKED
6 incident(s)
```

### 10. Ejecutar estrategia de retraining

```powershell
python -m src.monitoring.retraining_strategy `
  --psi 0.30 `
  --mae-change 60 `
  --rmse-change 60
```

Resultado:

```text
RETRAIN
```

---

# Estado del proyecto

| Componente                                    | Estado                    |
| --------------------------------------------- | ------------------------- |
| Ingesta                                       | ✅                         |
| Data Quality                                  | ✅                         |
| Data Quality Gate                             | ✅                         |
| EDA                                           | ✅                         |
| Feature Engineering                           | ✅                         |
| Modelado                                      | ✅                         |
| Baseline                                      | ✅                         |
| MLflow Tracking                               | ✅                         |
| MLflow Artifacts                              | ✅                         |
| Model Registry                                | ✅                         |
| Lifecycle Candidate / Validation / Production | ✅                         |
| FastAPI                                       | ✅                         |
| Endpoint `/predict`                           | ✅                         |
| Dockerfile                                    | ✅                         |
| `.dockerignore`                               | ✅                         |
| Docker Build                                  | ✅                         |
| Docker Run                                    | ✅                         |
| Prueba de `/predict`                          | ✅                         |
| System Monitoring                             | ✅                         |
| Data Monitoring — PSI                         | ✅                         |
| Model Monitoring — MAE/RMSE                   | ✅                         |
| Data Drift Simulation                         | ✅                         |
| Data Quality Contamination                    | ✅                         |
| Retraining Strategy                           | ✅                         |
| Git Workflow                                  | ✅                         |
| Pruebas automatizadas                         | ✅                         |
| Arquitectura técnica                          | ⏳ Documentar con diagrama |
| Team                                          | ⏳ AGREGAR                 |

---

# Consideraciones de reproducibilidad

Para reproducir el proyecto:

1. Clonar el repositorio.
2. Crear el entorno virtual.
3. Instalar `requirements.txt`.
4. Ejecutar la ingesta mediante el script correspondiente.
5. Ejecutar los notebooks para reproducir el análisis y modelado.
6. Levantar MLflow.
7. Registrar y consultar los experimentos.
8. Ejecutar la API.
9. Ejecutar las pruebas automatizadas.
10. Ejecutar los módulos de monitoreo.
11. Construir y ejecutar el contenedor Docker.

Los datasets grandes no forman parte directamente del repositorio.

Los archivos pequeños incluidos en:

```text
examples/monitoring/
```

corresponden únicamente a simulaciones controladas para demostrar los mecanismos de monitoreo y calidad.

---

# Conclusión

El proyecto implementa un flujo completo de Machine Learning orientado a forecasting de consumo eléctrico, incluyendo:

```text
Ingesta
   ↓
Data Quality
   ↓
Quality Gate
   ↓
EDA
   ↓
Feature Engineering
   ↓
Modelado
   ↓
Evaluación
   ↓
MLflow Tracking
   ↓
Model Registry
   ↓
FastAPI
   ↓
Docker
   ↓
Monitoring
   ├── System Monitoring
   ├── Data Monitoring
   └── Model Monitoring
   ↓
Retraining Strategy
```

El flujo permite llevar el modelo desde la preparación y validación de los datos hasta su experimentación, registro, despliegue mediante API y Docker, pruebas automatizadas y monitoreo posterior al despliegue.

---

## Comprobación completa del proyecto

Esta sección permite verificar de forma ordenada los principales componentes implementados en el proyecto, desde la instalación de las dependencias hasta el monitoreo y la ejecución mediante Docker.

1. # Crear y activar el entorno virtual

Desde la carpeta raíz del proyecto:

python -m venv .venv

Activar el entorno:

.\.venv\Scripts\Activate.ps1

Si PowerShell bloquea la ejecución:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Luego:

.\.venv\Scripts\Activate.ps1

2. # Instalar las dependencias

Actualizar pip:

python -m pip install --upgrade pip

Instalar las dependencias del proyecto:

python -m pip install -r requirements.txt

3. # Ejecutar las pruebas automatizadas

Ejecutar toda la suite:

python -m pytest tests\ -v

Resultado esperado:

19 passed

Actualmente, el proyecto cuenta con pruebas para:

Data Quality.
Modelo.
API.
System Monitoring.
Data Monitoring.
Model Monitoring.
Quality Gate.
Estrategia de Retraining.

4. # Ejecutar la ingesta de datos

La ingesta reproducible se ejecuta mediante:

python src/ingestion/ingest.py
5. Ejecutar los notebooks del proyecto

El primer notebook corresponde a:

01_ingestion_data_quality_eda.ipynb

Contiene:

Ingesta.
Data Quality.
Tratamiento de datos.
EDA.
Análisis temporal.

El segundo notebook corresponde a:

02_timeseries_feature_engineering_modeling.ipynb

Contiene:

Preparación de la serie temporal.
Feature Engineering.
División Train / Validation / Test.
Baseline.
Entrenamiento de modelos.
Evaluación.
Selección del modelo final.
Registro de experimentos en MLflow.

6. # Levantar MLflow

Abrir una nueva terminal desde la carpeta raíz del proyecto y activar el entorno virtual.

Ejecutar:

mlflow server --host 127.0.0.1 --port 5000

MLflow estará disponible en:

MLflow local

Se puede verificar el experimento:

household-power-forecasting

Y el modelo registrado:

random_forest_feature_set_b

Versión:

1

7. # Ejecutar la API

Con MLflow ejecutándose, abrir otra terminal y ejecutar:

uvicorn src.api.main:app --reload --port 8000

La API estará disponible en:

API local

La documentación interactiva estará disponible en:

Swagger UI

8. # Probar el endpoint /predict

Desde Swagger, seleccionar:

POST /predict

Utilizar un request válido con las variables requeridas por Feature Set B.

El resultado esperado es:

HTTP 200 OK

La respuesta incluye:

forecast
horizon
model_name
model_version

9. # Probar System Monitoring

Con la API ejecutándose:

Invoke-RestMethod -Method Get -Uri http://localhost:8000/monitoring/system

El endpoint devuelve métricas relacionadas con:

Latency.
Throughput.
Error rate.
Availability.
Total requests.
Uptime.

10. # Probar Data Monitoring con un batch estable

Ejecutar:

python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_1.csv `
  --columns Global_active_power `
  --output reports/data_monitoring.json

Resultado esperado:

PSI = 0.0000
STATUS = OK

11. # Probar Data Monitoring con Data Drift

Ejecutar:

python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_2.csv `
  --columns Global_active_power `
  --output reports/drift_batch_2.json

Resultado esperado:

PSI = 8.2831
STATUS = ALERT

Esto demuestra la detección de un cambio significativo en la distribución de los datos.

12. # Probar Model Monitoring

Ejecutar:

python -m src.monitoring.model_monitor `
  --input examples/monitoring/predictions_by_batch.csv `
  --output reports/model_monitoring.json

El monitoreo evalúa:

MAE.
RMSE.
Cambio porcentual respecto al desempeño de referencia.

Los resultados esperados de la simulación incluyen:

Reference → REFERENCE
Batch 1  → ALERT
Batch 2  → ALERT

13. # Probar Quality Monitoring

Ejecutar la simulación de contaminación:

python -m src.monitoring.quality_monitor `
  --input examples/monitoring/quality_simulation/contaminated_batch.csv `
  --output reports/quality_contamination.json

Resultado esperado:

STATUS = BLOCKED
INCIDENTS = 6

Esto demuestra que el sistema puede detectar problemas de calidad y bloquear un batch inválido.

14. # Probar la estrategia de Retraining

Ejecutar un escenario con Data Drift y degradación significativa del modelo:

python -m src.monitoring.retraining_strategy `
  --psi 0.30 `
  --mae-change 60 `
  --rmse-change 60

Resultado esperado:

RETRAIN
Drift sin degradación significativa
python -m src.monitoring.retraining_strategy `
  --psi 0.30 `
  --mae-change 10 `
  --rmse-change 10

Resultado esperado:

MONITOR
Degradación sin Data Drift significativo
python -m src.monitoring.retraining_strategy `
  --psi 0.05 `
  --mae-change 60 `
  --rmse-change 60

Resultado esperado:

NO_RETRAIN

15. # Verificar Docker

Comprobar que Docker está instalado y ejecutándose:

docker version

Construir la imagen:

docker build -t household-power-g7 .

Verificar la comunicación con el equipo anfitrión:

docker run --rm household-power-g7 python -c "import socket; print(socket.gethostbyname('host.docker.internal'))"

16. # Ejecutar la API mediante Docker

Con el servidor MLflow ejecutándose en el equipo anfitrión:

docker run --rm -p 8000:8000 -e MLFLOW_TRACKING_URI=http://host.docker.internal:5000 household-power-g7

Abrir:

Swagger UI en Docker

Probar nuevamente:

POST /predict

Resultado esperado:

HTTP 200 OK
17. # Verificación final

Finalmente, ejecutar nuevamente toda la suite de pruebas:

python -m pytest tests\ -v

Resultado esperado:

19 passed

Nota: pueden aparecer warnings relacionados con dependencias o compatibilidad de versiones, pero la ejecución actual del proyecto debe completar correctamente las 19 pruebas automatizadas.


# Team

El proyecto fue desarrollado por los siguientes integrantes:

* Evelyn Calderón
* Alejandro Alfaro
* Alexandra Chacaltana

El equipo trabajó de manera colaborativa utilizando un repositorio compartido y un flujo de trabajo basado en ramas individuales y Pull Requests.

La estructura de ramas utilizada durante el desarrollo del proyecto fue:

main
├── alexandra
├── alejandro
└── eve

Cada integrante realizó cambios en su rama correspondiente antes de integrarlos progresivamente a la rama principal (main) mediante Pull Requests y procesos de merge.

