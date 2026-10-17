# INF-8239-C2
> Manual laboratorios guiados.
> Unidad 02 · Texto, embeddings y redes

## Unidad 02 - LAB04 y LAB05
> ### LAB04 · Desde cero: localizar, aprobar y auditar un corpus público
> ### LAB05 · Clasificación de texto: TF-IDF, Naive Bayes y modelo lineal

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 2304 Mhz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:***	GS66 Stealth 11UH
- ***Physical Memory (RAM):***	32.0 GB
- ***GPU:*** NVIDIA GeForce RTX 3080
- ***Sistema operativo:*** Windows 11 con WSL habilitado con Ubuntu 24

## Dataset

**Sentiment Labelled Sentences** (Kotzias, D., 2015, UCI Machine Learning Repository,
[doi:10.24432/C57604](https://doi.org/10.24432/C57604)), licencia CC BY 4.0.
Contiene 3,000 oraciones en inglés de Amazon, IMDb y Yelp (1,000 por sitio, 50 % positivas
y 50 % negativas). Etiqueta `label`: `1` = positivo, `0` = negativo.

En LAB05 se usa el subconjunto **Amazon (Celulares y Accesorios)**.

- Ficha técnica: [docs/ficha-tecnica.md](docs/ficha-tecnica.md)
- Dataset card: [docs/DATASET_CARD.md](docs/DATASET_CARD.md)

## Estructura del proyecto

```
LAB04-05/
├── app/main.py                  # Aplicación local (Streamlit) para clasificar texto
├── data/
│   ├── raw/                     # .txt originales de UCI (separados por tab)
│   └── processed/               # .csv convertidos (separador "|")
├── docs/
│   ├── ficha-tecnica.md
│   ├── DATASET_CARD.md
│   └── REDACCION_ESTUDIANTE.md  # Campos de redacción y conclusión (400–600 palabras)
├── models/
│   ├── text_model.joblib        # Pipeline TF-IDF + regresión logística (LAB05)
│   └── word2vec.model           # Embeddings Word2Vec (LAB04)
├── notebooks/
│   ├── LAB04.ipynb              # Auditoría, Word2Vec y red social
│   └── LAB05.ipynb              # Entrenamiento y evaluación de clasificadores
├── reports/
│   ├── text_metrics.csv         # F1 macro por modelo
│   ├── confusion_text.png       # Matriz de confusión del modelo seleccionado
│   ├── error_analysis.csv       # 42 errores categorizados y justificados
│   ├── test_results.txt         # Salida de pytest
│   ├── centralities.csv         # Centralidades de la red (LAB04)
│   ├── network.png              # Visualización de la red (LAB04)
│   └── social_network.graphml
├── src/lab04_05/
│   ├── data.py                  # Carga, conversión y contrato de datos
│   ├── audit.py                 # Auditoría del DataFrame
│   └── modeling.py              # Pipelines: dummy, Naive Bayes, logística
├── tests/                       # Pruebas unitarias (pytest)
```

## Cómo ejecutar el proyecto

### Prerrequisitos
- [uv](https://docs.astral.sh/uv/) como gestor de proyecto de Python.
- Python 3.12 (uv lo instala automáticamente según `.python-version`).
- El proyecto se desarrolló en WSL con Ubuntu 24, pero LAB04-05 **no** requiere dependencias
  del sistema operativo, así que también funciona en Windows o macOS.

### Instalación
Desde la carpeta `uasd-ds-2/unidad02/LAB04-05`:

```bash
uv sync
```

uv crea el entorno virtual `.venv` con las dependencias de [pyproject.toml](pyproject.toml).

### Notebooks
1. Abrir la carpeta en VS Code (con WSL: ejecutar `code .` dentro de la carpeta). Se necesitan las
   extensiones **Python** y **Jupyter** de Microsoft (y **WSL** si aplica).
2. Abrir el notebook y seleccionar como kernel el entorno `.venv` creado por `uv sync`.
3. Ejecutar en orden:
   - [notebooks/LAB04.ipynb](notebooks/LAB04.ipynb): conversión de datos, auditoría, Word2Vec y red social.
   - [notebooks/LAB05.ipynb](notebooks/LAB05.ipynb): entrenamiento, métricas, matriz de confusión,
     errores y guardado del modelo en `models/text_model.joblib`.

> ⚠️ La última celda de LAB05 sobrescribe `reports/error_analysis.csv` con `category = REVISAR`.
> Haz una copia del archivo categorizado antes de volver a ejecutarla.

### Pruebas unitarias
```bash
uv run pytest -v
```
Resultado actual: **5 pruebas aprobadas** (ver [reports/test_results.txt](reports/test_results.txt)).
Las pruebas validan el contrato de datos (columnas requeridas, textos vacíos), que cada pipeline
tenga los pasos `tfidf` y `model` y prediga una etiqueta, y que la red tenga un PageRank válido.

### Aplicación local
```bash
uv run streamlit run app/main.py
```
Abrir http://localhost:8501, escribir una oración en inglés y pulsar **Clasificar**. La app muestra
`Positivo (1)` o `Negativo (0)`. Es una demostración académica: la predicción no es una decisión
automática.

## Resultados (LAB05)

| Modelo | F1 macro |
|---|---|
| **Regresión logística** (seleccionado) | **0.832** |
| Naive Bayes (Complement) | 0.824 |
| Dummy (most frequent) | 0.333 |

- Partición: 75 % entrenamiento (750) / 25 % prueba (250), estratificada, `random_state=42`.
- Matriz de confusión (logística): 108 VN, 17 FP, 25 FN, 100 VP → exactitud 0.832.
- Clase más difícil: **positiva** (recall 0.80 frente a 0.864 de la negativa).
- Errores más frecuentes: positivos implícitos sin vocabulario de sentimiento (13/42) y negaciones (10/42).
- Decisión: **no desplegar** para decisiones automáticas sin validación cruzada, evaluación fuera
  de dominio (IMDb, Yelp) y revisión humana.

Análisis completo y conclusión: [docs/RESUMEN.md](docs/RESUMEN.md).
