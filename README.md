# Household Power G7 — MLOps de Pronóstico de Consumo Eléctrico

Proyecto académico de Machine Learning y MLOps para el pronóstico del consumo eléctrico de un hogar, desarrollado como parte del curso de Ciencia de Datos.

El proyecto implementa un flujo reproducible que incluye ingestión y validación de datos, análisis exploratorio, ingeniería de características, entrenamiento y evaluación de modelos, experiment tracking con MLflow, Model Registry, API de inferencia con FastAPI, Docker y monitoreo de datos, modelo, calidad y sistema.

---

# 1. Business Problem

El proyecto tiene como objetivo desarrollar un modelo de Machine Learning para realizar el pronóstico del consumo eléctrico de un hogar utilizando datos históricos de consumo registrados a intervalos de un minuto.

El objetivo es predecir el consumo correspondiente a la siguiente hora (**t+1**) y demostrar un flujo MLOps reproducible que incluya:

* Validación de datos.
* Análisis exploratorio.
* Ingeniería de características.
* Entrenamiento y evaluación del modelo.
* Tracking de experimentos con MLflow.
* Registro y versionado del modelo.
* Despliegue mediante FastAPI.
* Contenerización mediante Docker.
* Monitoreo de datos, modelo y sistema.
* Detección de Data Drift.
* Quality Gate.
* Estrategia de decisión para reentrenamiento.

El problema se aborda como un problema de **regresión y pronóstico de series temporales**.

---

# 2. Dataset

Se utilizó el dataset **Individual Household Electric Power Consumption**, que contiene mediciones del consumo eléctrico de un hogar.

Los datos originales tienen una frecuencia de aproximadamente un minuto y contienen las siguientes variables:

* `Date`
* `Time`
* `Global_active_power`
* `Global_reactive_power`
* `Voltage`
* `Global_intensity`
* `Sub_metering_1`
* `Sub_metering_2`
* `Sub_metering_3`

El período original de los datos utilizado en el proyecto comprende:

```text
2006-12-16 17:24:00
        a
2010-11-26 21:02:00
```

Para el modelado, los datos fueron agregados a una frecuencia **horaria**.

Dataset final utilizado para el modelado:

```text
33,195 observaciones horarias
```

Variable objetivo:

```text
Global_active_power
```

La variable objetivo representa el consumo de potencia activa global y se utiliza para realizar el pronóstico de la siguiente hora.

Los datos originales no se incluyen en el repositorio debido a su tamaño y se mantienen fuera del control de versiones.

---

# 3. Architecture

El proyecto sigue una arquitectura MLOps de extremo a extremo, que cubre el ciclo completo desde la ingesta y validación de los datos hasta el entrenamiento, despliegue, predicción, monitoreo y reentrenamiento del modelo.

La arquitectura incluye las siguientes etapas principales:

1. **Ingesta de datos:** incorporación y preparación del conjunto de datos *Household Power Consumption*.
2. **Calidad de datos y EDA:** validación, limpieza y análisis exploratorio de los datos.
3. **Ingeniería de características:** creación de variables temporales, rezagos (*lags*) y ventanas móviles (*rolling windows*).
4. **Entrenamiento:** entrenamiento y evaluación de los modelos de pronóstico.
5. **Seguimiento de experimentos con MLflow:** registro de parámetros, métricas, artefactos y experimentos.
6. **Model Registry:** versionamiento y gestión del modelo seleccionado.
7. **Docker:** contenedorización de la aplicación y del entorno utilizado para servir el modelo.
8. **FastAPI:** API REST utilizada para exponer el modelo y realizar predicciones.
9. **Monitoreo:** supervisión del *data drift*, rendimiento del modelo, calidad de los datos y métricas del sistema.
10. **Estrategia de reentrenamiento:** proceso de decisión para determinar cuándo es necesario reentrenar el modelo.

### Diagrama de Arquitectura MLOps

![Arquitectura MLOps](Docs/arquitecture_mlops.png)

# 4. Repository Structure

La estructura principal del repositorio es:

```text
Proyecto-Household-Power-G7/
│
├── data/
│   └── raw/
│
├── examples/
│   └── monitoring/
│       ├── predictions/
│       ├── production/
│       ├── reference.csv
│       │
│       ├── drift_simulation/
│       │   ├── batch_1.csv
│       │   └── batch_2.csv
│       │
│       └── quality_simulation/
│           └── contaminated_batch.csv
│
├── reports/
│   ├── drift_report.json
│   ├── model_monitoring.json
│   ├── quality_report.json
│   └── system_monitoring.json
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
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .python-version
├── requirements.txt
└── README.md
```

Descripción de los componentes principales:

* `data/`: contiene los datos utilizados por el proyecto.
* `examples/monitoring/`: contiene datasets pequeños utilizados para demostrar las funcionalidades de monitoreo.
* `reports/`: contiene los resultados generados por los módulos de monitoreo.
* `src/ingestion/`: contiene el proceso reproducible de ingestión.
* `src/monitoring/`: contiene los componentes de monitoreo.
* `src/api/`: contiene la API desarrollada con FastAPI.
* `src/tracking/`: contiene la configuración relacionada con MLflow.
* `tests/`: contiene las pruebas automatizadas.
* `01_ingestion_data_quality_eda.ipynb`: notebook de ingestión, calidad de datos y EDA.
* `02_timeseries_feature_engineering_modeling.ipynb`: notebook de series temporales, ingeniería de características, entrenamiento y evaluación.
* `Dockerfile`: define la imagen Docker.
* `requirements.txt`: contiene las dependencias Python.
* `.gitignore`: excluye datos, entornos virtuales y artefactos locales.

---

# 5. Installation

## Clonar el repositorio

```powershell
git clone <URL_DEL_REPOSITORIO>
```

Entrar al proyecto:

```powershell
cd Proyecto-Household-Power-G7
```

## Crear entorno virtual

```powershell
python -m venv .venv
```

## Activar entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Instalar dependencias

```powershell
python -m pip install --upgrade pip
```

```powershell
python -m pip install -r requirements.txt
```

Las dependencias necesarias para reproducir el proyecto se encuentran en:

```text
requirements.txt
```

---

# 6. Data Ingestion

El proceso reproducible de ingestión se encuentra en:

```text
src/ingestion/ingest.py
```

Para ejecutarlo:

```powershell
python src/ingestion/ingest.py
```

El primer notebook contiene el proceso complementario de ingestión, calidad y EDA:

```text
01_ingestion_data_quality_eda.ipynb
```

Los datos originales se mantienen fuera del control de versiones debido a su tamaño.

---

# 7. Training

El proceso de preparación de la serie temporal, ingeniería de características, entrenamiento y evaluación se encuentra en:

```text
02_timeseries_feature_engineering_modeling.ipynb
```

El notebook debe ejecutarse en orden para reproducir el proceso de modelado.

## Forecasting

Se implementó un pronóstico **one-step ahead**, donde se predice el consumo correspondiente a la siguiente hora:

```text
t + 1 hora
```

La división de los datos se realizó cronológicamente para evitar utilizar información futura durante el entrenamiento.

```text
Train       70% → 23,236 observaciones
Validation  15% → 4,979 observaciones
Test        15% → 4,980 observaciones
```

## Baseline

Se utilizó **Naive Persistence** como modelo baseline:

```text
ŷ_t = y_(t-1)
```

Resultados del baseline en validación:

```text
MAE  = 0.4669
RMSE = 0.6947
```

## Feature Set B

El conjunto de características utilizado por el modelo final contiene:

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

## Modelo final

El modelo seleccionado fue:

```text
RandomForestRegressor
```

Configuración:

```text
n_estimators = 200
max_depth = 10
min_samples_leaf = 2
random_state = 42
```

El criterio principal utilizado para seleccionar el modelo fue **RMSE**, utilizando **MAE** como métrica complementaria.

---

# 8. MLflow

MLflow se utiliza para realizar el tracking de experimentos y el registro de modelos.

## Levantar servidor MLflow

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

Tracking URI:

```text
http://127.0.0.1:5000
```

## Experimento

El experimento principal es:

```text
household-power-forecasting
```

El proyecto registra información relacionada con:

### Parameters

* Algoritmo.
* Hiperparámetros.
* Feature Set.
* Random seed.
* Data version.

### Metrics

* MAE.
* RMSE.

### Artifacts

* Modelo entrenado.
* Gráficos relevantes.
* Resultados de evaluación.

## Model Registry

El modelo final registrado es:

```text
random_forest_feature_set_b
```

Versión:

```text
Version 1
```

Aliases utilizados:

```text
candidate
validation
production
```

Estos aliases representan los estados/roles utilizados durante el flujo de gestión del modelo.

---

# 9. Docker

El proyecto incluye un `Dockerfile` para ejecutar la API dentro de un contenedor.

## Verificar Docker

```powershell
docker version
```

Durante el desarrollo se utilizó Docker Desktop.

## Construir imagen

```powershell
docker build -t household-power-g7 .
```

## Verificar comunicación con el host

```powershell
docker run --rm household-power-g7 python -c "import socket; print(socket.gethostbyname('host.docker.internal'))"
```

## Ejecutar API mediante Docker

Primero debe estar ejecutándose MLflow en el equipo anfitrión:

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

Luego ejecutar el contenedor:

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

---

# 10. API

La API fue desarrollada utilizando **FastAPI**.

Archivo principal:

```text
src/api/main.py
```

## Ejecutar API localmente

```powershell
uvicorn src.api.main:app --reload --port 8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## Endpoint de predicción

```text
POST /predict
```

El endpoint recibe las características requeridas por el modelo y devuelve el pronóstico correspondiente a la siguiente hora.

Ejemplo de respuesta:

```json
{
  "forecast": 0.523,
  "horizon": "t+1_hour",
  "model_name": "random_forest_feature_set_b",
  "model_version": "1"
}
```

La API permite demostrar la inferencia del modelo registrado.

---

# 11. Monitoring

El proyecto implementa diferentes mecanismos de monitoreo.

## 11.1 System Monitoring

La API mide automáticamente métricas relacionadas con las solicitudes.

Endpoint:

```text
GET /monitoring/system
```

Se puede consultar mediante:

```powershell
Invoke-RestMethod -Method Get -Uri http://localhost:8000/monitoring/system
```

Las métricas incluyen:

* Latency.
* Throughput.
* Error rate.
* Availability.
* Total requests.
* Uptime.

Las métricas se mantienen en memoria y se reinician al reiniciar el servicio.

---

## 11.2 Data Quality Gate

El Quality Gate se encuentra en:

```text
src/monitoring/quality_monitor.py
```

Antes del entrenamiento se validan condiciones como:

1. Dataset no vacío.
2. Presencia de variables requeridas.
3. Ausencia de valores faltantes.
4. Tipos de datos correctos.
5. Ausencia de duplicados.
6. Ausencia de valores infinitos.

Si los datos no cumplen las condiciones requeridas, el proceso se bloquea.

Resultado de la validación utilizada:

```text
Training Data Quality Gate: OK
```

---

## 11.3 Data Drift Monitoring

El monitoreo de Data Drift se encuentra en:

```text
src/monitoring/data_monitor.py
```

Se utiliza **Population Stability Index (PSI)**.

Archivos de referencia:

```text
examples/monitoring/reference.csv
examples/monitoring/drift_simulation/batch_1.csv
examples/monitoring/drift_simulation/batch_2.csv
```

Para un batch estable:

```powershell
python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_1.csv `
  --columns Global_active_power `
  --output reports/data_monitoring.json
```

Resultado esperado:

```text
PSI = 0.0000
STATUS = OK
```

Para simular Data Drift:

```powershell
python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_2.csv `
  --columns Global_active_power `
  --output reports/drift_batch_2.json
```

Resultado esperado:

```text
PSI = 8.2831
STATUS = ALERT
```

Umbrales utilizados:

```text
PSI < 0.10          → OK
0.10 ≤ PSI < 0.25  → WARNING
PSI ≥ 0.25          → ALERT
```

Estos valores se utilizan como criterios prácticos para la simulación académica.

---

## 11.4 Model Monitoring

El monitoreo del modelo se encuentra en:

```text
src/monitoring/model_monitor.py
```

Se monitorean:

* MAE.
* RMSE.
* Cambio porcentual respecto al desempeño de referencia.

Ejecutar:

```powershell
python -m src.monitoring.model_monitor `
  --input examples/monitoring/predictions_by_batch.csv `
  --output reports/model_monitoring.json
```

Resultados de la simulación:

```text
Reference → REFERENCE
Batch 1   → ALERT
Batch 2   → ALERT
```

La lógica considera una degradación significativa cuando MAE o RMSE aumenta en un 50% o más respecto al valor de referencia.

---

## 11.5 Quality Monitoring

El monitoreo de calidad se encuentra en:

```text
src/monitoring/quality_monitor.py
```

Se utiliza un batch contaminado para simular diferentes problemas de calidad.

Archivo:

```text
examples/monitoring/quality_simulation/contaminated_batch.csv
```

Ejecutar:

```powershell
python -m src.monitoring.quality_monitor `
  --input examples/monitoring/quality_simulation/contaminated_batch.csv `
  --output reports/quality_contamination.json
```

Se simulan seis incidentes:

1. Missing value.
2. Duplicate.
3. Extreme outlier.
4. Incorrect datatype.
5. Unknown category.
6. Schema modification.

Resultado esperado:

```text
STATUS = BLOCKED
INCIDENTS = 6
```

Esto demuestra que un batch inválido puede ser detectado y bloqueado antes de continuar con el flujo.

---

## 11.6 Retraining Strategy

La estrategia de reentrenamiento se encuentra en:

```text
src/monitoring/retraining_strategy.py
```

La decisión considera conjuntamente:

```text
PSI
MAE change %
RMSE change %
```

Reglas principales:

```text
PSI ≥ 0.25
        ↓
Data Drift significativo
```

y:

```text
MAE o RMSE ≥ 50% de aumento
        ↓
Model Degradation significativa
```

La decisión es:

| Drift | Degradación | Decisión     |
| ----- | ----------- | ------------ |
| No    | No          | `NO_RETRAIN` |
| No    | Sí          | `NO_RETRAIN` |
| Sí    | No          | `MONITOR`    |
| Sí    | Sí          | `RETRAIN`    |

### Ejemplo: Drift + degradación

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

### Ejemplo: Drift sin degradación

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

### Ejemplo: Degradación sin Drift

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

Los umbrales utilizados corresponden a criterios definidos para la simulación académica y podrían calibrarse posteriormente con datos históricos en un ambiente productivo.

---

# 12. Results

## Modelo seleccionado

```text
RandomForestRegressor
Feature Set B
```

## Configuración

```text
n_estimators = 200
max_depth = 10
min_samples_leaf = 2
random_state = 42
```

## Evaluación final sobre Test

```text
MAE  = 0.3254
RMSE = 0.4709
```

## Comparación contra el baseline

| Modelo            |    MAE |   RMSE |
| ----------------- | -----: | -----: |
| Naive Persistence | 0.3859 | 0.5843 |
| Random Forest     | 0.3254 | 0.4709 |

## Mejora obtenida

```text
MAE improvement  = 15.67%
RMSE improvement = 19.42%
```

El modelo final presenta una mejora respecto al baseline tanto en MAE como en RMSE.

El RMSE fue utilizado como criterio principal de selección debido a que penaliza con mayor fuerza los errores grandes, mientras que MAE se utilizó como métrica complementaria.

---

# 13. Team

El proyecto fue desarrollado por:

| Integrante               | Responsabilidades                                                       |
| ------------------------ | ----------------------------------------------------------------------- |
| **Alexandra Chacaltana** | Modeling, MLflow Tracking, Model Registry, FastAPI, Docker y Monitoring |
| **Alejandro Alfaro**     | Feature Engineering y Baseline Modeling . PPT                           |
| **Evelyn Calderón**      | Data Ingestion, Data Quality y EDA, Revisión final                      |

El equipo utilizó un repositorio compartido con ramas individuales y Pull Requests.

Ramas principales:

```text
main
├── alexandra
├── alejandro
└── eve
```

Flujo de trabajo:

```text
Rama individual
      ↓
Desarrollo
      ↓
Commit
      ↓
Push
      ↓
Pull Request
      ↓
Revisión / Merge
      ↓
main
```

---

# Reproducibility

Para reproducir el proyecto desde cero:

## 1. Clonar repositorio

```powershell
git clone <URL_DEL_REPOSITORIO>
cd Proyecto-Household-Power-G7
```

## 2. Crear y activar entorno

```powershell
python -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Instalar dependencias

```powershell
python -m pip install --upgrade pip
```

```powershell
python -m pip install -r requirements.txt
```

## 4. Ejecutar ingestión

```powershell
python src/ingestion/ingest.py
```

## 5. Ejecutar notebook de análisis y modelado

Abrir y ejecutar en orden:

```text
01_ingestion_data_quality_eda.ipynb
```

y posteriormente:

```text
02_timeseries_feature_engineering_modeling.ipynb
```

El segundo notebook contiene el proceso de ingeniería de características, entrenamiento y evaluación del modelo.

## 6. Levantar MLflow

```powershell
mlflow server --host 127.0.0.1 --port 5000
```

## 7. Ejecutar API

En otra terminal:

```powershell
uvicorn src.api.main:app --reload --port 8000
```

## 8. Abrir Swagger

```text
http://localhost:8000/docs
```

## 9. Ejecutar pruebas

```powershell
python -m pytest tests\ -v
```

Resultado esperado:

```text
19 passed
```

---

# Automated Tests

El proyecto cuenta con 19 pruebas automatizadas distribuidas de la siguiente manera:

| Archivo              | Pruebas |
| -------------------- | ------: |
| `test_data.py`       |       5 |
| `test_model.py`      |       1 |
| `test_api.py`        |       3 |
| `test_monitoring.py` |      10 |
| **Total**            |  **19** |

Para ejecutar toda la suite:

```powershell
python -m pytest tests\ -v
```

Resultado esperado:

```text
19 passed
```

---

# Complete MLOps Flow

El recorrido completo utilizado para la demostración es:

```text
Raw Data
   ↓
Data Ingestion
   ↓
Data Validation / Quality Gate
   ↓
EDA
   ↓
Feature Engineering
   ↓
Train / Validation / Test
   ↓
Model Training
   ↓
MLflow Experiment Tracking
   ↓
Model Registry
   ↓
Docker Image
   ↓
FastAPI
   ↓
Prediction
   ↓
System Monitoring
   ↓
Data Drift Monitoring
   ↓
Model Monitoring
   ↓
Quality Monitoring
   ↓
Retraining Decision
```

---

# Quick Commands

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

## Ingestión

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

## Tests

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

# Demo Final

Para realizar una demostración rápida del proyecto:

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

### 6. Probar Data Drift

```powershell
python -m src.monitoring.data_monitor `
  --reference examples/monitoring/reference.csv `
  --production examples/monitoring/drift_simulation/batch_2.csv `
  --columns Global_active_power `
  --output reports/drift_batch_2.json
```

Resultado esperado:

```text
PSI = 8.2831
STATUS = ALERT
```

### 7. Probar Model Monitoring

```powershell
python -m src.monitoring.model_monitor `
  --input examples/monitoring/predictions_by_batch.csv `
  --output reports/model_monitoring.json
```

### 8. Probar Quality Monitoring

```powershell
python -m src.monitoring.quality_monitor `
  --input examples/monitoring/quality_simulation/contaminated_batch.csv `
  --output reports/quality_contamination.json
```

Resultado esperado:

```text
STATUS = BLOCKED
INCIDENTS = 6
```

### 9. Probar Retraining Strategy

```powershell
python -m src.monitoring.retraining_strategy `
  --psi 0.30 `
  --mae-change 60 `
  --rmse-change 60
```

Resultado esperado:

```text
RETRAIN
```

### 10. Ejecutar pruebas finales

```powershell
python -m pytest tests\ -v
```

Resultado esperado:

```text
19 passed
```

---

# Project Status

| Componente            | Estado      |
| --------------------- | ----------- |
| Business Problem      | ✅           |
| Dataset               | ✅           |
| Data Ingestion        | ✅           |
| Data Quality          | ✅           |
| EDA                   | ✅           |
| Feature Engineering   | ✅           |
| Model Training        | ✅           |
| Model Evaluation      | ✅           |
| MLflow Tracking       | ✅           |
| Model Registry        | ✅           |
| Docker                | ✅           |
| FastAPI               | ✅           |
| System Monitoring     | ✅           |
| Data Drift Monitoring | ✅           |
| Model Monitoring      | ✅           |
| Quality Monitoring    | ✅           |
| Retraining Strategy   | ✅           |
| Automated Tests       | ✅ 19 passed |
| Team                  | ✅           |
| README                | ✅           |

---

# Conclusion

El proyecto implementa un flujo completo de MLOps para el pronóstico del consumo eléctrico de un hogar.

El modelo final, **RandomForestRegressor con Feature Set B**, obtuvo:

```text
MAE  = 0.3254
RMSE = 0.4709
```

sobre el conjunto de prueba, mejorando respecto al baseline de persistencia.

Además del modelado, el proyecto integra experiment tracking y Model Registry mediante MLflow, despliegue de inferencia mediante FastAPI y Docker, y mecanismos de monitoreo para sistema, datos, calidad y desempeño del modelo.

La implementación también incluye una estrategia de decisión de reentrenamiento que diferencia entre Data Drift y degradación del modelo, permitiendo determinar si corresponde monitorear, no reentrenar o ejecutar un nuevo entrenamiento.

La suite automatizada final cuenta con:

```text
19 pruebas
19 passed
```



