# Model Card · Autoencoder y VAE

## Modelos y versiones
- `models/autoencoder.keras`: autoencoder denso (AE), proyecto `inf8239-u03-generative` 0.1.0.
- `models/decoder.keras`: decodificador del autoencoder variacional (VAE); es el único modelo que usa la aplicación.
- Entorno: Python 3.12.10, TensorFlow 2.21.0 (CPU), dependencias fijadas en `uv.lock`. Semilla global 42.
- Comando: `uv run python scripts/train_ae_vae.py --epochs-ae 6 --epochs-vae 8`.

## Uso previsto y usuarios
Material docente de INF-8239 para estudiantes y docentes: comparar compresión (AE) con generación regularizada (VAE), explorar un espacio latente de 2 dimensiones en `app/streamlit_app.py` y discutir cómo se evalúan los modelos generativos.

## Usos fuera de alcance
- Generar datos sintéticos para entrenar o evaluar sistemas en producción.
- Usarlo como garantía de privacidad o anonimización: las muestras se derivan de los datos de entrenamiento.
- Imágenes fuera de Fashion-MNIST (otras resoluciones, color, fotografías reales de ropa).
- Clasificar prendas o decidir sobre personas o productos.

## Dataset, licencia y particiones
- Fashion-MNIST (Zalando Research, licencia MIT), cargado con `tf.keras.datasets.fashion_mnist`. Son imágenes de 28×28 en escala de grises, en 10 clases equilibradas.
- Preprocesamiento: se escala a [0, 1] y se añade un canal; `validate_images` comprueba la forma y el rango.
- Particiones: 54 000 para entrenamiento y 6 000 para validación (el último 10 % del conjunto oficial de entrenamiento), y 10 000 para prueba (el conjunto oficial). Las etiquetas solo se usan para anotar los paneles, no para entrenar.

## Arquitectura y espacio latente
| Modelo | Arquitectura | Latente | Parámetros |
|---|---|---|---|
| AE | Flatten → Dense(16, ReLU) → Dense(784, sigmoide) | 16, determinista | 25 888 |
| VAE, codificador | Flatten → Dense(128, ReLU) → μ, log σ² | 2, gaussiano | — |
| VAE, decodificador | Dense(128, ReLU) → Dense(784, sigmoide) | — | 101 520 |

La pérdida del AE es la BCE media por píxel. La pérdida del VAE es la BCE sumada por imagen más el término KL hacia N(0, I), con peso 1, y usa el truco de reparametrización. El optimizador es Adam con batch de 256. El AE usa EarlyStopping con paciencia 2, pero en esta corrida no se activó.

## Métricas de reconstrucción y generación
Conjunto de prueba (`reports/training_metrics.json`):

| Métrica | AE | VAE |
|---|---|---|
| MSE por píxel | 0.0203 | 0.0333 |
| BCE | 0.307 por píxel | 268.8 por imagen (≈ 0.343 por píxel) |
| KL | — | 6.21 |

- En las curvas (`reports/training_curves.png`), entrenamiento y validación bajan juntas y no hay señales de sobreajuste. Las dos pérdidas siguen bajando al final, así que ambos modelos están poco entrenados.
- El KL se estabiliza alrededor de 6.2 nats: el latente se usa y no colapsa a la distribución previa.
- El AE reconstruye mejor porque tiene 8 veces más dimensiones latentes y ninguna regularización. Eso no significa que genere mejor: no tiene una distribución de la cual muestrear.
- La pérdida no mide la calidad perceptual de las muestras y no se calculó FID ni otra métrica de ese tipo.

## Diversidad y vecinos cercanos
Panel no seleccionado (`reports/ae_vae_panel.png`): 16 índices de prueba sorteados con semilla 42 (`panel_test_indices` en las métricas) y 16 muestras con z ~ N(0, I).

- **Reconstrucciones.** Las prendas con silueta simple (pantalón, zapatilla, botín, vestido) se reconstruyen bien en ambos modelos. El VAE confunde sandalias con botines y abrigos o suéteres con camisetas genéricas, y pierde texturas, logos y estampados. Los bolsos se reconstruyen como "suéter ancho" en el VAE.
- **Diversidad.** La distancia RMS media entre pares es 0.137 para las muestras frente a 0.417 para imágenes reales de prueba. Las muestras son mucho menos diversas: en su mayoría son siluetas tenues y promediadas de calzado o de torso.
- **Vecinos más cercanos en entrenamiento.** La distancia RMS media es 0.085 para las muestras frente a 0.139 para las imágenes reales de prueba. Que sea menor **no** indica calidad ni originalidad. Los vecinos son prendas oscuras y de bajo contraste (sobre todo camisas y camisetas), y se parecen porque las muestras son tenues. A simple vista ninguna muestra copia un ejemplo concreto.
- **Interpolación** (`reports/interpolation.png`): pasa de botín a pantalón de forma gradual. Los puntos intermedios, con forma de camisa, no son prendas plausibles.

## Hardware, tiempo y tamaño
- CPU Intel Core i7-11800H y 32 GB de RAM, en Windows 11. TensorFlow no usa GPU en Windows nativo.
- Tiempo de entrenamiento: AE ≈ 5 s (6 épocas) y VAE ≈ 9 s (8 épocas). Los tiempos cambian según el hardware.
- Tamaño en disco: `autoencoder.keras` ≈ 339 KB y `decoder.keras` ≈ 426 KB.

## Limitaciones, riesgos y supervisión
- Es un modelo de capacidad muy baja: capas densas, latente de 2 dimensiones y pocas épocas. Las muestras son borrosas, tenues y poco diversas.
- Las métricas vienen de una sola semilla y una sola corrida, sin intervalos de variación.
- Hay regiones del latente que decodifican a imágenes que no son prendas. La app permite recorrer el rango [-3, 3], más allá de la masa de N(0, I).
- Generar datos sintéticos no implica privacidad; con modelos de más capacidad habría que volver a comparar con vecinos de entrenamiento.
- La interpretación de los paneles y la decisión de usar el modelo corresponden a personas, no al modelo.
