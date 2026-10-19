# Model Card · Fashion-MNIST CNN

## Modelo y versión
- **Nombre:** `small_cnn` (`models/best_cnn.keras`), paquete `lab07` v0.1.0.
- **Arquitectura:** Conv2D(32, 3×3) → MaxPool → Conv2D(64, 3×3) → MaxPool → GlobalAveragePooling → Dropout(0.25) → Dense(10, softmax). Tiene 19,466 parámetros.
- **Baseline de referencia:** `dense_baseline` (`models/best_dense.keras`): Flatten → Dense(64, ReLU) → Dense(10, softmax). Tiene 50,890 parámetros.
- **Entrenamiento:** Adam, `sparse_categorical_crossentropy`, batch 128, 8 épocas como máximo, EarlyStopping (patience=2, restaura los mejores pesos) y ModelCheckpoint por `val_loss`. Semilla 42 y `TF_DETERMINISTIC_OPS=1`.
- **Código:** `notebooks/lab07.ipynb` (función `run`), `src/lab07/models.py`.

## Uso previsto
Es un ejercicio didáctico del curso INF-8239 (Unidad 02, LAB07). Sirve para comparar un baseline denso con una CNN pequeña bajo la misma partición, para practicar la lectura de métricas por clase, la matriz de confusión y el análisis de errores, y para medir el costo computacional (Green AI). El modelo clasifica imágenes de 28×28 en escala de grises, centradas y con fondo negro, en las 10 categorías de Fashion-MNIST.

## Usos fuera de alcance
- Fotografías reales de prendas (con color, fondo, pose u otra resolución) o catálogos de comercio electrónico en producción.
- Cualquier otro dominio, como imágenes médicas, OCR, vigilancia o identificación de personas.
- Decisiones automáticas con impacto sobre personas (precios, inventario, moderación) sin revisión humana.
- Usar la probabilidad softmax como medida calibrada de confianza, porque no se evaluó la calibración.

## Dataset y particiones
Fashion-MNIST (Zalando Research) se descarga con `tf.keras.datasets.fashion_mnist`.

| Partición | Imágenes | Origen | Distribución por clase |
|---|---|---|---|
| Entrenamiento | 54,000 | primeras 54,000 de *train* | 5,367–5,445 por clase |
| Validación | 6,000 | últimas 6,000 de *train* | 555–633 por clase |
| Prueba | 10,000 | *test* oficial | 1,000 exactas por clase |

Las clases son T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag y Ankle boot. Todas están balanceadas. Ambos modelos usan exactamente la misma partición, y la prueba solo se usa para la evaluación final.

## Preprocesamiento
1. Conversión a `float32` y división entre 255, para llevar los valores a [0, 1].
2. Se añade el canal: (N, 28, 28) → (N, 28, 28, 1).
3. Validación por contrato (`validate_images`): forma, coincidencia entre imágenes y etiquetas, valores finitos y rango [0, 1].

No se aplica aumento de datos ni estandarización por media y desviación.

## Métricas globales y por clase
Las métricas se calcularon sobre las 10,000 imágenes de prueba. La fuente es `reports/cv_metrics.json`.

| Modelo | Accuracy | F1 macro |
|---|---|---|
| Dense baseline | **0.867** | **0.866** |
| CNN pequeña | 0.793 | 0.787 |

| Clase | Precisión CNN | Recall CNN | F1 CNN | F1 Dense |
|---|---|---|---|---|
| T-shirt/top | 0.651 | 0.812 | 0.723 | 0.820 |
| Trouser | 0.989 | 0.914 | 0.950 | 0.974 |
| Pullover | 0.736 | 0.712 | 0.724 | 0.759 |
| Dress | 0.716 | 0.858 | 0.780 | 0.871 |
| Coat | 0.640 | 0.657 | 0.648 | 0.778 |
| Sandal | 0.936 | 0.905 | 0.920 | 0.953 |
| **Shirt** | 0.494 | **0.303** | **0.376** | 0.656 |
| Sneaker | 0.879 | 0.930 | 0.904 | 0.934 |
| Bag | 0.929 | 0.930 | 0.930 | 0.963 |
| Ankle boot | 0.914 | 0.910 | 0.912 | 0.952 |

La CNN queda por debajo del baseline en las 10 clases. La clase más difícil para ambos modelos es **Shirt**. La CNN confunde 271 camisas con T-shirt/top, 196 con Coat y 123 con Pullover.

## Comparación de costo
- **Hardware:** Intel Core i7-11800H (8 núcleos, 16 hilos), 32 GB de RAM, Windows 11. El equipo tiene una RTX 3080, pero TensorFlow no la usó porque no soporta GPU en Windows nativo, así que todo corrió en CPU.
- **Entorno:** Python 3.13.14, TensorFlow 2.21.0, gestionado con `uv` (`uv.lock`).
- **Parámetros:** CNN 19,466 frente a Dense 50,890. La CNN tiene 2.6 veces menos.
- **Tamaño del archivo `.keras`:** CNN 262 KB frente a Dense 619 KB. El archivo incluye el estado del optimizador.
- **Tiempo de entrenamiento (8 épocas):** CNN 45.5 s frente a Dense 6.9 s. La CNN tarda unas 6.6 veces más.
- **Tiempo de inferencia:** CNN 0.136 ms/imagen (σ 0.021) frente a Dense 0.085 ms/imagen (σ 0.003). La CNN tarda unas 1.6 veces más. Es la mediana de 5 repeticiones sobre el mismo lote de 1,000 imágenes, después de una pasada de calentamiento.

## Limitaciones y riesgos
- **Subajuste.** En la época 8, la pérdida de entrenamiento de la CNN (0.702) sigue alta y la de validación (0.594) sigue bajando, así que el modelo no convergió. El resultado mide esta configuración con este presupuesto de épocas. No mide el potencial de las CNN en general.
- **Benchmark didáctico.** Fashion-MNIST tiene imágenes de baja resolución, centradas, sin fondo y en escala de grises. Su desempeño no se traslada a imágenes reales ni a otros dominios.
- **Clases semánticamente cercanas** (Shirt, T-shirt/top, Pullover y Coat): a 28×28 muchas siluetas son ambiguas incluso para una persona. Los errores en estas clases son sistemáticos.
- Solo se usó una semilla y una partición, sin intervalos de confianza. Diferencias de menos de 1 punto no deberían interpretarse.
- No se evaluó la calibración, la robustez ante ruido o rotación, ni el comportamiento con imágenes fuera de distribución. El modelo siempre asigna una de las 10 clases.

## Supervisión y monitoreo
- Si se usa, debe haber revisión humana, especialmente para las predicciones de Shirt, Pullover, Coat y T-shirt/top.
- Hay que vigilar la distribución de las clases predichas y de la confianza máxima, para detectar un cambio de dominio.
- Antes de cualquier uso fuera del aula, se debe reentrenar y evaluar con datos del dominio real, revisar por clase y repetir la medición de costo en el hardware de destino.
- Hay que reejecutar `uv run pytest -q` ante cualquier cambio de datos, preprocesamiento o arquitectura.
