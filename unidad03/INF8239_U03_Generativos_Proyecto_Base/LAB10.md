# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 03 - LAB10 Modelos generativos con Fashion-MNIST.
### Autoencoder y VAE: reconstrucción, espacio latente, muestras y evaluación con paneles no seleccionados.

Proyecto base del autor académico Edwin Ramón José Nolasco.

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:*** GS66 Stealth 11UH
- ***Physical Memory (RAM):*** 32.0 GB
- ***Entorno:*** Windows 11, Python 3.12.10, TensorFlow 2.21.0 (CPU), NumPy 2.5.3, Matplotlib 3.11.2, Streamlit 1.64.0, gestionado con `uv`. TensorFlow no usa GPU en Windows nativo, así que todo corre en CPU.

## Resumen
Entrené un **autoencoder** denso (AE, latente de 16 dimensiones) y un **autoencoder variacional** (VAE, latente gaussiano de 2 dimensiones) sobre Fashion-MNIST. Los comparé con un panel de 16 imágenes de prueba sorteadas con semilla fija, curvas de entrenamiento y validación, vecinos más cercanos en entrenamiento y una medida de diversidad. El decodificador del VAE se sirve en una app de Streamlit que solo hace inferencia.

**Resultado principal:** el AE reconstruye mejor que el VAE (MSE 0.020 frente a 0.033), pero no sabe generar. El VAE sí genera, pero sus muestras son tenues, borrosas y poco diversas: 0.137 de distancia media entre pares, frente a 0.417 en imágenes reales. No hay sobreajuste y las pérdidas seguían bajando al final, así que los dos modelos están poco entrenados.

- Model card: [docs/MODEL_CARD.md](docs/MODEL_CARD.md)
- Declaración de uso de IA: [docs/AI_USE_DECLARATION.md](docs/AI_USE_DECLARATION.md)

## Estructura del proyecto

```
INF8239_U03_Generativos_Proyecto_Base/
├── app/streamlit_app.py         # App local: explorador del latente del VAE (solo inferencia)
├── docs/
│   ├── MODEL_CARD.md
│   └── AI_USE_DECLARATION.md
├── models/                      # autoencoder.keras y decoder.keras (no se versionan)
├── reports/                     # Figuras y métricas (no se versionan)
│   ├── ae_vae_panel.png
│   ├── interpolation.png
│   ├── training_curves.png
│   └── training_metrics.json
├── scripts/
│   ├── check_runtime.py         # Versión de Python/TensorFlow y GPU disponible
│   └── train_ae_vae.py          # Entrenamiento, paneles, métricas y guardado de modelos
├── src/inf8239_u03_gen/
│   ├── data.py                  # Normalización y contrato de imágenes
│   ├── evaluation.py            # Vecinos más cercanos y diversidad
│   └── models.py                # Arquitecturas del AE y del VAE
└── tests/                       # Pruebas unitarias (pytest)
```

## Cómo ejecutar el proyecto

### Instalación
Desde la carpeta `uasd-ds-2/unidad03/INF8239_U03_Generativos_Proyecto_Base`:
```bash
uv python install 3.12
uv sync --extra cpu
uv run python scripts/check_runtime.py
uv run pytest -q
```

### Laboratorio
```bash
uv run python scripts/train_ae_vae.py --epochs-ae 6 --epochs-vae 8
uv run streamlit run app/streamlit_app.py
uv export --format requirements.txt --extra cpu --output-file requirements-cloud.txt
```
Fashion-MNIST se descarga solo la primera vez, con `tf.keras.datasets`. La app abre en http://localhost:8501 y tiene dos deslizadores para recorrer el latente (x, y) del VAE.

**Cambios al código base:**
- El panel original mostraba las **primeras 12** imágenes de prueba. Ahora muestra **16 sorteadas con semilla 42**, como pide §7, con la clase de cada columna y una quinta fila con el vecino más cercano de cada muestra en entrenamiento.
- El VAE solo registraba la pérdida de entrenamiento. Agregué `test_step` para medir también reconstrucción y KL en validación, y la lógica de la pérdida quedó en `compute_losses` para no duplicarla.
- Antes, el AE separaba validación con `validation_split` y el VAE no tenía. Ahora los dos usan la misma partición explícita: el último 10 % de entrenamiento.
- `training_metrics.json` antes guardaba solo tiempos y número de parámetros. Ahora también incluye pérdidas de prueba, historial por época, índices del panel, distancias a vecinos y diversidad.
- La búsqueda de vecinos y la medida de diversidad están en `src/inf8239_u03_gen/evaluation.py` y se prueban en `tests/test_evaluation.py`.

**Entregables generados:** `reports/ae_vae_panel.png`, `reports/interpolation.png`, `reports/training_curves.png`, `reports/training_metrics.json`, `models/autoencoder.keras`, `models/decoder.keras` y `requirements-cloud.txt`.

## Resultados

### 3. Dataset y entrenamiento

| Partición | Imágenes |
|---|---|
| Entrenamiento | 54,000 |
| Validación (último 10 % del train oficial) | 6,000 |
| Prueba (test oficial) | 10,000 |

Las imágenes son de 28×28 en escala de grises, en 10 clases equilibradas, escaladas a [0, 1]. Las etiquetas solo se usan para anotar el panel.

| Modelo | Épocas | Tiempo | Parámetros | MSE prueba | Otras pérdidas (prueba) |
|---|---|---|---|---|---|
| AE | 6 | ≈ 5 s | 25,888 | **0.0203** | BCE 0.307 por píxel |
| VAE | 8 | ≈ 9 s | 101,520 (decodificador) | 0.0333 | Reconstrucción 268.8, KL 6.21 |

![Curvas de entrenamiento](reports/training_curves.png)

### 4. Interpretar el autoencoder
- **Patrón observado: "entrenamiento y validación bajan juntas".** La BCE va de 0.450 a 0.306 en entrenamiento y de 0.374 a 0.307 en validación. No hay sobreajuste y EarlyStopping no se activó. La curva seguía bajando, así que hay margen con más épocas.
- **Reconstrucción nítida** en siluetas simples (pantalón, zapatilla, botín, vestido). **Salida borrosa** en texturas y detalles finos: se pierden logos, estampados y las tiras de las sandalias, porque un latente de 16 dimensiones con una sola capa no alcanza para guardarlos.
- **Error bajo no significa generación.** El AE no tiene una distribución de la cual muestrear, así que decodificar puntos arbitrarios no garantiza imágenes plausibles.

### 5. Interpretar el VAE

| Componente | Lectura |
|---|---|
| Pérdida de reconstrucción | Baja de 335 a 268 por imagen. Se pierde más información que en el AE (MSE 0.033 frente a 0.020) por el latente de 2 dimensiones y la regularización KL. |
| KL | Se estabiliza en ≈ 6.2 nats desde la época 5. El latente se usa (no colapsa a la distribución previa) y se mantiene cerca de N(0, I). |
| Muestras | Hay poca diversidad: las muestras son siluetas tenues y promediadas de calzado o torso, con una distancia entre pares de 0.137 frente a 0.417 en imágenes reales. |
| Interpolación | Es gradual de botín a pantalón, pero los pasos intermedios, con forma de camisa, no son prendas plausibles. |
| Vecino más cercano | Ninguna muestra copia un ejemplo concreto. Los vecinos son prendas oscuras de poco contraste (ver §7). |

![Interpolación en el latente](reports/interpolation.png)

### 6. Comparar AE, VAE, GAN y transferencia

| Enfoque | Objetivo dominante | Lo que mostró este laboratorio | Qué no debe afirmarse |
|---|---|---|---|
| AE | Compresión y reconstrucción. | Es el que mejor reconstruye (MSE 0.020). | Que toda decodificación desde puntos arbitrarios sea plausible. |
| VAE | Representación probabilística y generación regularizada. | Genera, pero borroso y con poca diversidad. | Que maximiza nitidez o garantiza diversidad. |
| GAN | Generación mediante competencia entre redes. | No se entrenó. | Que evita colapso o es fácil de evaluar. |
| Transfer learning | Reutilización de representaciones aprendidas. | No se aplicó. | Que elimina la necesidad de validar el nuevo dominio. |

### 7. Panel no seleccionado
Los 16 índices de prueba se sortearon con `np.random.default_rng(42)`: 4383, 891, 941, 7355, 6968, 6537, 5262, 7609, 7860, 7174, 4325, 858, 8577, 9752, 7728 y 2013. Las 16 muestras salen del mismo generador con z ~ N(0, I). No se eligió ningún resultado a mano.

![Panel AE / VAE / muestras / vecinos](reports/ae_vae_panel.png)

Filas: original con su clase, reconstrucción AE, reconstrucción VAE, muestra nueva del VAE y su vecino más cercano en entrenamiento, con la clase y la distancia RMS.

- **Clases visualmente confusas:** el VAE reconstruye las dos sandalias como botines, los bolsos como un "suéter ancho", y el abrigo y el suéter como torsos genéricos. Pantalón, zapatilla y botín se mantienen.
- **Diversidad:** de las 16 muestras, unas 4 parecen calzado y el resto son torsos o prendas difusas. No aparece ningún pantalón ni bolso reconocible.
- **Vecinos cercanos:**

| Indicador | Muestras VAE | Imágenes reales de prueba |
|---|---|---|
| Distancia RMS media al vecino de entrenamiento | 0.085 | 0.139 |
| Distancia RMS mínima | 0.055 | — |
| Distancia media entre pares (diversidad) | 0.137 | 0.417 |

Que las muestras queden **más cerca** de entrenamiento que las imágenes reales **no** indica calidad ni memorización. Son imágenes tenues y casi uniformes, y en distancia de píxeles se parecen a cualquier prenda oscura: 10 de los 16 vecinos son camisas, camisetas, suéteres o abrigos de bajo contraste. A simple vista ninguna muestra reproduce un ejemplo concreto.

### 8. Aplicación local y nube
- `app/streamlit_app.py` carga `models/decoder.keras` con una ruta relativa a la raíz del proyecto y solo hace inferencia: comprobé que arranca y responde en `/healthz`.
- `requirements-cloud.txt` se generó con `uv export --extra cpu` y tiene las versiones fijadas con hash. Para una nube con poca memoria convendría `tensorflow-cpu` o exportar el decodificador a un formato más liviano.
- El modelo no tiene secretos. Si se agregaran, irían en la configuración de la plataforma y no en Git.

### 9. Pruebas
```
uv run pytest -q
......                                                                   [100%]
6 passed
```

| Contrato | Prueba |
|---|---|
| Normalización a [0, 1] y forma (n, 28, 28, 1) | `test_normalization_contract`, `test_rejects_wrong_shape` |
| Salida del AE y del decodificador con forma de imagen | `test_autoencoder_output_contract`, `test_decoder_output_contract` |
| El vecino de una copia exacta es ella misma, aunque esté en otro bloque | `test_nearest_neighbor_finds_exact_copy_across_batches` |
| Muestras idénticas tienen diversidad 0 | `test_identical_samples_have_zero_diversity` |

## Cierre interpretativo

- **Resultado principal:** El AE reconstruye mejor (MSE 0.020 frente a 0.033), pero solo el VAE puede generar. Sus muestras son borrosas y poco diversas (0.137 frente a 0.417 en imágenes reales). Ninguno de los dos sobreajusta.
- **Evidencia utilizada:** Fashion-MNIST oficial (54,000 / 6,000 / 10,000), semilla 42, curvas de entrenamiento y validación, un panel de 16 ejemplos sorteados con sus vecinos en entrenamiento, la interpolación, 6 pruebas aprobadas y el [Model Card](docs/MODEL_CARD.md).
- **Qué representa el espacio latente:** En el VAE, cada punto (x, y) es la media de una gaussiana que el decodificador convierte en una prenda "promedio". Regiones cercanas dan prendas parecidas, pero entre clases hay zonas que decodifican a imágenes que no son ninguna prenda.
- **Limitaciones:** La capacidad es muy baja (capas densas, latente de 2 dimensiones, pocas épocas), hay una sola semilla y una sola corrida, y no se usó una métrica perceptual como FID. La distancia de píxeles a vecinos no basta para hablar de originalidad ni de privacidad.
- **Siguiente experimento:** Entrenar más épocas hasta que la validación se estanque, subir el latente del VAE a 8–16 dimensiones y probar capas convolucionales. Después, repetir el panel y los vecinos con 3 semillas para ver si la diversidad sube sin que las muestras se acerquen a copias.
