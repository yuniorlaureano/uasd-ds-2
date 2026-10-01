# Ficha del dataset
- **Origen del dataset:** [Banknote Authentication](https://archive.ics.uci.edu/dataset/267/banknote+authentication)
- **Author del dataset:** Volker Lohweg (University of Applied Sciences, Ostwestfalen-Lippe)
- **Licencia:**: This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.
- **Dominio:** 
Los datos se extrajeron de imágenes obtenidas a partir de muestras auténticas y falsificadas que imitaban billetes. Para la digitalización, se utilizó una cámara industrial empleada habitualmente en la inspección de impresiones. Las imágenes finales tienen una resolución de 400 x 400 píxeles. Debido al objetivo y a la distancia respecto al objeto analizado, se obtuvieron imágenes en escala de grises con una resolución aproximada de 660 ppp. Se empleó la transformada de *wavelet* para extraer características de las imágenes.

- **Unidad de análisis:** Mediciones tomadas de Billetes autenticos y falsificados que imitaban a estos autenticos.

- **Features:**
Here is the corrected and properly aligned markdown table for the Banknote Authentication dataset:

    > | Variable Name | Role | Type | Description | Units | Missing Values |
    > | --- | --- | --- | --- | --- | --- |
    > | **variance** | Feature | Continuous | Variance of Wavelet Transformed image | — | No |
    > | **skewness** | Feature | Continuous | Skewness of Wavelet Transformed image | — | No |
    > | **curtosis** | Feature | Continuous | Curtosis of Wavelet Transformed image | — | No |
    > | **entropy** | Feature | Continuous | Entropy of image | — | No |
    > | **class** | Target | Integer | Class label | — | No |

- **Decisión:** Predecir billetes falsos. Un software realiza las mediciones, y el modelo clasificara el resultado.

- **Target:** Columna: class, si un billete es falso, o positivo

- **Error más costoso:** Un falso/positio. Clasificar el billete como autentico cuando en relealidad no lo es, lleva a que la entidad sea estafada con billetes falsos.

- **Usuario:** Bancos

- **Dataset file**

    > | File | Size |
    > | ---- | ---- |
    > | data_banknote_authentication.txt | 45.3 KB |

- **Glosario:**
    1. **Transformada wavelet:**  (o transformada de ondículas) Es un método matemático que descompone una señal en pequeñas ondas de duración limitada llamadas wavelets o ondículas madre
    2. **Píxeles:** Un píxel (del inglés picture element, o "elemento de imagen") es la unidad básica y el punto más pequeño que compone una imagen digital o una pantalla
    3. **Digitalización:**  Es el proceso de convertir información y procesos físicos o analógicos (como documentos en papel, fotos impresas o archivos manuales) en un formato electrónico digital que se puede almacenar, procesar y transmitir mediante dispositivos tecnológicos
    4. **Escala de grises:** Es una progresión gradual de tonos monocromáticos que va desde el negro absoluto hasta el blanco puro, pasando por múltiples tonalidades intermedias de gris
    5. **ppp:** píxeles por pulgada (o puntos por pulgada), y mide la resolución o la cantidad de detalles que contiene una imagen en un espacio de una pulgada lineal.
    6. **Entropia:** es una magnitud física que mide el grado de desorden o la dispersión de la energía en un sistema termodinámico. 

## ⚠️Advertencia 

> Es un caso de estudio para practicar el paso a paso con SVM con pipeline, búsqueda de parámetros y evaluación. No constituye un modelo de uso en ambientes productivos