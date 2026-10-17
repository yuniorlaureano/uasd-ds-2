# Redacción del estudiante · U02.LAB05

## Campos solicitados

**Resultado principal:**
La regresión logística con TF-IDF (unigramas y bigramas) obtuvo un F1 macro de 0.832 y una exactitud de 0.832 sobre 250 oraciones de prueba de reseñas de Amazon (Celulares y Accesorios). Supera ampliamente al baseline dummy (0.333) y ligeramente a Naive Bayes (0.824).

**Modelo seleccionado y evidencia:**
Se seleccionó la regresión logística (`class_weight="balanced"`). Evidencia: `reports/text_metrics.csv` (mayor F1 macro), `reports/confusion_text.png` (208 de 250 aciertos) y el modelo serializado en `models/text_model.joblib`. La diferencia con Naive Bayes (0.008) proviene de una única partición y no es concluyente; la selección se basa en el mejor F1 macro y en un rendimiento equilibrado entre clases.

**Clase con mayor dificultad:**
La clase positiva (1): recall de 0.80 frente a 0.864 de la negativa. 25 de 125 reseñas positivas fueron clasificadas como negativas.

**Tipo de error más frecuente:**
Predominan los falsos negativos (positivo → negativo): 25 casos frente a 17 falsos positivos. En la revisión manual de los 42 errores (`reports/error_analysis.csv`), la categoría más frecuente fue "positivo implícito sin vocabulario de sentimiento" (13 de 42, todos falsos negativos), por ejemplo "Protects the phone on all sides." y "The delivery was on time.". Le sigue la negación (10 de 42, en ambas direcciones), como en "I wouldn't recommend buying this product." o "not distracting at all".

**Impacto en el contexto:**
Si el modelo se usara para monitorear la satisfacción de clientes, los falsos negativos inflarían la percepción de insatisfacción y generarían alertas innecesarias. Los falsos positivos (17) son más delicados: quejas reales pasarían como satisfechas y no recibirían atención. Aproximadamente 1 de cada 6 oraciones se clasifica incorrectamente.

**Limitación del dataset:**
Son solo 1,000 oraciones en inglés de una única categoría de Amazon, de reseñas de finales de los 2000 a 2014, seleccionadas por tener polaridad clara (sin neutrales). El modelo se entrenó solo con Amazon, no con IMDb ni Yelp, por lo que no generaliza a otros dominios, idiomas, textos neutros o mixtos ni al lenguaje actual. La prueba de 250 casos es pequeña y se detectó posible ruido de etiquetas ("Excellent starter wireless headset." aparece etiquetada como negativa).

**Decisión antes del despliegue:**
No desplegar para decisiones automáticas. Antes se debe: (1) validar con validación cruzada estratificada para confirmar la diferencia entre modelos; (2) evaluar fuera de dominio con IMDb y Yelp; (3) revisar etiquetas dudosas y tratar negaciones y errores ortográficos; (4) usarlo solo como apoyo con revisión humana, como ya advierte la aplicación `app/main.py`.

---

## Conclusión

El objetivo de este laboratorio fue construir un clasificador de sentimiento para oraciones de reseñas y evaluar con honestidad si estaría listo para usarse. Se trabajó con el corpus público Sentiment Labelled Sentences (Kotzias, UCI, 2015), usando el subconjunto de Amazon, Celulares y Accesorios: 1,000 oraciones en inglés, balanceadas 50/50 entre positivas y negativas. La auditoría confirmó que no había valores ausentes ni textos vacíos y que las longitudes van de 11 a 149 caracteres. Los datos se dividieron 75/25 de forma estratificada, con 750 oraciones para entrenar y 250 para evaluar.

Se compararon tres pipelines con TF-IDF de unigramas y bigramas. El baseline dummy, que siempre predice la clase más frecuente, obtuvo un F1 macro de 0.333, el piso de lo que se logra sin aprender nada. Naive Bayes alcanzó 0.824 y la regresión logística 0.832, ambos muy por encima del baseline. Se seleccionó la regresión logística por tener el mejor F1 macro y un rendimiento equilibrado entre clases. Sin embargo, la diferencia con Naive Bayes equivale a unas dos oraciones de prueba en una sola partición, por lo que no puede considerarse significativa sin validación cruzada.

La matriz de confusión muestra 208 aciertos de 250. La clase positiva es la más difícil: su recall es 0.80, frente a 0.864 de la negativa. El modelo comete 25 falsos negativos y 17 falsos positivos, es decir, tiende a calificar como negativas reseñas que eran positivas. La revisión manual de los 42 errores explica por qué. La causa más frecuente son las oraciones positivas que describen hechos en lugar de usar adjetivos ("The delivery was on time.", "Protects the phone on all sides."), con 13 casos, todos falsos negativos. La segunda es la negación, con 10 casos, porque TF-IDF trata "not good" casi igual que "good". También aparecen frases muy cortas, vocabulario poco frecuente como "abhor" o "unacceptable", errores ortográficos como "Excelent" y al menos una etiqueta que parece incorrecta.

Estos patrones no son fallos aleatorios: reflejan la naturaleza de la bolsa de palabras, que pondera términos sin entender el orden, la negación ni el contexto. En un uso real, como el monitoreo de la satisfacción de clientes, aproximadamente una de cada seis oraciones se clasificaría mal. Los falsos negativos inflarían la percepción de insatisfacción. Los falsos positivos son más costosos, porque dejarían quejas reales sin atender.

El dataset también impone límites. Cubre una sola categoría de productos de una sola plataforma, en inglés y con reseñas de hace más de diez años. Además, los autores seleccionaron solo oraciones con polaridad clara, excluyendo las neutrales y las ambiguas, que en la práctica son muy comunes. Un modelo entrenado así probablemente rendirá peor con reseñas de restaurantes, películas, otros idiomas o lenguaje actual.

Por todo esto, la decisión es no desplegar el modelo para tomar decisiones automáticas. Antes sería necesario confirmar los resultados con validación cruzada estratificada, evaluarlo fuera de dominio con los subconjuntos de IMDb y Yelp, corregir las etiquetas dudosas y probar representaciones que capturen la negación, como embeddings o modelos de lenguaje preentrenados. Mientras tanto, la aplicación local en Streamlit sirve como demostración académica y apoyo a un revisor humano, tal como lo advierte su propia interfaz. El laboratorio muestra que una métrica de 0.83 es un buen punto de partida, pero que entender dónde y por qué falla un modelo es lo que permite decidir con responsabilidad si debe usarse.
