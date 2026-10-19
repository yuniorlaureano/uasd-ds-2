# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 02 - LAB07 Visión por computadora con Fashion-MNIST.
### Baseline denso frente a CNN: desempeño, costo e interpretación responsable.

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:*** GS66 Stealth 11UH
- ***Physical Memory (RAM):*** 32.0 GB
- ***GPU:*** NVIDIA GeForce RTX 3080. TensorFlow no la usó: desde la versión 2.11 TensorFlow no soporta GPU en Windows nativo (`GPU: []`), así que todo corrió en CPU.
- ***Entorno:*** Windows 11, Python 3.13.14, TensorFlow 2.21.0, gestionado con `uv`.

## Resumen
Hice el proyecto desde cero en el notebook [`notebooks/lab07.ipynb`](notebooks/lab07.ipynb), con el código reutilizable separado en `src/lab07` (datos, modelos y entorno) y pruebas en `tests/`. Entrené un baseline denso y una CNN pequeña con la misma partición, la misma semilla y el mismo hardware, y los comparé por desempeño y por costo.

**Resultado principal:** con 8 épocas, el baseline denso (F1 macro 0.866) superó a la CNN (0.787), que quedó subajustada.

## Cómo ejecutar
```bash
uv sync
```
1. Abrir `notebooks/lab07.ipynb` con el kernel de `.venv` y ejecutar todas las celdas. La celda `run()` entrena ambos modelos con 8 épocas.
2. Ejecutar las pruebas con `uv run pytest -q`.

## Resultados

### 3. Descarga del dataset
El notebook registra la forma, las clases y la distribución de cada partición antes de entrenar:

| Partición | Forma | Clases | Imágenes por clase |
|---|---|---|---|
| train | (54000, 28, 28, 1) | 10 | 5,367 – 5,445 |
| valid | (6000, 28, 28, 1) | 10 | 555 – 633 |
| test | (10000, 28, 28, 1) | 10 | 1,000 exactas |

Las particiones están balanceadas. La validación son las últimas 6,000 imágenes del conjunto oficial de entrenamiento. La prueba es el conjunto oficial de *test* y solo se usa para evaluar al final.

**Entregables generados:** `reports/cv_metrics.json`, `reports/confusion_cnn.png`, `reports/cnn_errors.png`, `models/best_cnn.keras` y `models/best_dense.keras`.

### 4. Entrenamiento y validación

| Época | Dense `loss` / `val_loss` | CNN `loss` / `val_loss` |
|---|---|---|
| 1 | 0.612 / 0.449 | 1.580 / 1.126 |
| 4 | 0.368 / 0.374 | 0.876 / 0.731 |
| 8 | 0.313 / 0.345 | 0.702 / 0.594 |

- **Dense:** ambas pérdidas disminuyen y la brecha final es pequeña (0.032), así que aprende patrones útiles sin señales de sobreajuste. Su `val_accuracy` se estabiliza en 0.874 en las épocas 7 y 8.
- **CNN:** ambas pérdidas disminuyen, pero siguen **altas** (el doble que las de la red densa) y no se han aplanado en la época 8. Lo leo como **subajuste**: no le alcanzaron las épocas para converger. Su pérdida de validación queda por debajo de la de entrenamiento porque el Dropout solo actúa al entrenar.
- **Accuracy alta, pero una clase con recall bajo:** la CNN tiene accuracy de 0.793, pero el recall de Shirt es de solo 0.303. El promedio oculta esa debilidad.
- `EarlyStopping` no se activó en ningún modelo, porque `val_loss` mejoró en todas las épocas.

### 5. Comparación del baseline y la CNN
Los dos modelos usan la misma partición, el mismo preprocesamiento, la misma semilla (42), el optimizador Adam, batch de 128, 8 épocas y el mismo equipo.

| Criterio | Dense | CNN |
|---|---|---|
| F1 macro (prueba) | **0.866** | 0.787 |
| Accuracy (prueba) | **0.867** | 0.793 |
| Parámetros | 50,890 | **19,466** |
| Tamaño de `.keras` | 619 KB | **262 KB** |
| Tiempo de entrenamiento | **6.9 s** | 45.5 s |
| Inferencia (mediana de 5 repeticiones, mismo lote de 1,000 imágenes) | **0.085 ms/img** (σ 0.003) | 0.136 ms/img (σ 0.021) |

F1 por clase (prueba):

| Clase | Dense | CNN | Diferencia |
|---|---|---|---|
| T-shirt/top | 0.820 | 0.723 | −0.097 |
| Trouser | 0.974 | 0.950 | −0.024 |
| Pullover | 0.759 | 0.724 | −0.035 |
| Dress | 0.871 | 0.780 | −0.091 |
| Coat | 0.778 | 0.648 | −0.130 |
| Sandal | 0.953 | 0.920 | −0.033 |
| **Shirt** | 0.656 | **0.376** | **−0.280** |
| Sneaker | 0.934 | 0.904 | −0.030 |
| Bag | 0.963 | 0.930 | −0.033 |
| Ankle boot | 0.952 | 0.912 | −0.040 |

**Mejora marginal de la CNN:** −8.0 puntos de F1 macro, es decir, no mejora y pierde en las 10 clases. A cambio, tardó unas **6.6 veces más en entrenar** y unas **1.6 veces más en inferir**. Solo gana en almacenamiento: tiene 2.6 veces menos parámetros y su archivo es 2.4 veces más pequeño. Tener menos parámetros no implica menos cómputo, porque cada filtro convolucional se aplica en todas las posiciones de la imagen.

> **Green AI:** no concluyo que el modelo con mayor accuracy sea automáticamente el mejor. En este caso, el modelo más simple es a la vez el más preciso y el más barato.

### 6. Errores visuales ([`reports/cnn_errors.png`](reports/cnn_errors.png))

| Índice | Real → Predicha | Comentario |
|---|---|---|
| #0, #43 | Ankle boot ↔ Sneaker | Botín bajo y zapatilla alta tienen una caña de altura parecida. Son pares visualmente semejantes. |
| #21 | Sandal → Sneaker | Sandalia cerrada con muchas tiras, que se ve como una zapatilla perforada. |
| #23 | Ankle boot → Sandal | Bota con aberturas grandes. Es un caso ambiguo. |
| #6 | Coat → Trouser | Abrigo oscuro y abierto: las dos franjas claras verticales parecen las piernas de un pantalón. Es el único error entre familias (prenda superior → pantalón). |
| #17, #51 | Coat → Shirt | Estampados de alto contraste: la textura domina sobre la silueta. |
| #25, #54 | Coat ↔ Pullover | Manga larga sin cierre visible. A 28×28 la silueta es idéntica a la de un suéter. |
| #26, #44 | Shirt → Coat | Camisas de manga larga con botonadura, parecidas a un abrigo. |
| #40 | Shirt → T-shirt/top | Camisa de manga corta. Solo el cuello y los botones la distinguen, y son pocos píxeles. |
| #27 | T-shirt/top → Dress | Top largo sin mangas con proporción de vestido. Es ambiguo incluso para una persona. |
| #42 | Dress → T-shirt/top | Vestido recto sin cintura marcada. |
| #48, #49 | Pullover → Shirt | #48 está en perspectiva, una vista atípica. #49 tiene cuello en V, como una camisa. |

**Patrón:** casi todos los errores ocurren dentro de dos familias de forma: prendas superiores (Shirt, T-shirt/top, Pullover, Coat y Dress) y calzado (Sandal, Sneaker y Ankle boot). La [matriz de confusión](reports/confusion_cnn.png) lo confirma. Las 1,000 imágenes de Shirt se reparten así: 303 aciertos, 271 como T-shirt/top, 196 como Coat y 123 como Pullover. Otros pares frecuentes son Pullover → Coat (137), Coat → Shirt (128), Pullover → Shirt (102) y Sandal → Sneaker (70).

> **Interpretación responsable:** Fashion-MNIST es un benchmark didáctico. Un buen resultado aquí no demuestra que el modelo sirva para imágenes médicas, OCR, vigilancia ni ningún otro dominio.

### 7. Pruebas
```
uv run pytest -q
.......                                                                  [100%]
7 passed
```

| Contrato | Prueba |
|---|---|
| Forma (N, 28, 28, 1) y rango [0, 1] | `test_normalize_adds_channel_and_scales`, `test_validate_rejects_wrong_shape`, `test_validate_rejects_out_of_range`, `test_validate_rejects_label_mismatch` |
| Número de clases igual a 10 | `test_ten_classes` |
| Salida del modelo con forma (N, 10) | `test_output_contract[build_cnn]`, `test_output_contract[build_dense]` |
| Probabilidades finitas, no negativas y con suma ≈ 1 | `test_output_contract[...]` |

### 8. Model Card
Ver [`MODEL_CARD.md`](MODEL_CARD.md).

### 9. Colab y publicación
En Colab se instalan las dependencias desde [`requirements-colab.txt`](requirements-colab.txt):
```python
%pip install -r requirements-colab.txt
```
El dataset se descarga al iniciar porque es público y pequeño. El modelo se carga desde la ruta relativa `models/best_cnn.keras`. Nunca se sube `.venv`, que ya está en el `.gitignore` del repositorio.

## Cierre interpretativo

- **Resultado principal:** Con 8 épocas en CPU, el baseline denso (F1 macro 0.866) superó a la CNN pequeña (0.787), que quedó subajustada.
- **Evidencia predictiva:** La CNN tuvo menor F1 en las 10 clases y su accuracy fue de 0.793 frente a 0.867. Sus pérdidas de entrenamiento (0.702) y de validación (0.594) seguían bajando en la época 8.
- **Clase más difícil:** Shirt. En la CNN tiene recall de 0.303 y F1 de 0.376, y en la red densa F1 de 0.656. Se confunde sobre todo con T-shirt/top (271), Coat (196) y Pullover (123).
- **Costo comparado:** La CNN tiene 2.6 veces menos parámetros (19,466 frente a 50,890) y un archivo 2.4 veces más pequeño. Aun así, tardó 6.6 veces más en entrenar (45.5 s frente a 6.9 s) y 1.6 veces más en inferir (0.136 frente a 0.085 ms/img), en un i7-11800H sin GPU.
- **¿La mejora justifica el costo?:** No. No hay mejora, sino una pérdida de 8.0 puntos de F1 macro, y el cómputo es mayor. Con esta configuración elijo el baseline denso. Para reconsiderar la CNN habría que entrenarla más épocas y repetir la comparación con varias semillas.
- **Limitación del benchmark:** Fashion-MNIST tiene imágenes de 28×28, en grises, centradas y sin fondo. Además usé una sola semilla y una sola partición, así que el resultado no se generaliza a fotos reales ni a otros dominios.
- **Decisión antes de usar otro dominio:** No desplegar. Primero hay que recolectar y etiquetar datos del dominio real, reentrenar, evaluar por clase con varias semillas, medir el costo en el hardware de destino y mantener revisión humana en las clases ambiguas.
