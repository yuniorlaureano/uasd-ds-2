# System Card · Recomendador

## Usuarios y propósito
Es un ejercicio didáctico del curso INF-8239 (Unidad 03, LAB08 y LAB09). Sirve para comparar una línea base de popularidad, un recomendador por contenido y un modelo híbrido colaborativo, y para documentar sus métricas, cold start y límites.

Los usuarios son estudiantes y docentes que exploran MovieLens desde la app local (`app/streamlit_app.py`). No es un sistema para usuarios finales: la lista que devuelve expresa similitud de géneros, no una preferencia individual garantizada.

## Catálogo y candidatos
- **Catálogo:** las 9,742 películas de `movies.csv`.
- **Popularidad:** las candidatas son las películas con al menos 12 ratings (percentil 80 del número de ratings por película). Las 18 películas sin ratings y la mayoría de las poco vistas quedan fuera.
- **Contenido:** todo el catálogo menos la película consultada.
- **Híbrido (LAB09):** las 100 películas con mayor puntuación colaborativa que el usuario no ha visto. Después se reordenan combinando esa puntuación con la similitud de contenido.

## Señales utilizadas
- **Explícitas:** `rating` (0.5–5.0) y `timestamp` de `ratings.csv`.
- **Contenido:** `genres` de `movies.csv`, vectorizado con TF-IDF.
- **No se usan:** `tags.csv`, `links.csv`, el año del título ni ningún dato demográfico. No hay señales implícitas como clics o tiempo de visualización.

## Modelos y fallback

| Modelo | Código | Cómo puntúa |
|---|---|---|
| Popularidad ponderada | `weighted_popularity` | Media bayesiana: `v/(v+m)·R + m/(v+m)·C`, donde `v` son los votos de la película, `R` su media, `m` = 12 (percentil 80) y `C` = 3.50 (media global) |
| Contenido | `ContentRecommender` | TF-IDF de géneros y similitud coseno con la película consultada |
| Factorización matricial | `MatrixFactorization` | SGD con 20 factores, 12 épocas, tasa de aprendizaje 0.01, regularización 0.05 y semilla 42 |
| Híbrido | `scripts/lab09_hybrid.py` | `α·colaborativo + (1−α)·contenido`, ambos normalizados entre 0 y 1, con α = 0.75 |

- **Fallback:** si el usuario no está en el modelo colaborativo (`top_n` devuelve una tabla vacía), se usa la popularidad, que no es personalizada.
- **Top-10 de popularidad (LAB08):**

  | # | Película | Votos | Media | Score |
  |---|---|---|---|---|
  | 1 | The Shawshank Redemption (1994) | 317 | 4.43 | 4.40 |
  | 2 | The Godfather (1972) | 192 | 4.29 | 4.24 |
  | 3 | Fight Club (1999) | 218 | 4.27 | 4.23 |
  | 4 | Star Wars: Episode IV (1977) | 251 | 4.23 | 4.20 |
  | 5 | The Usual Suspects (1995) | 204 | 4.24 | 4.20 |
  | 6 | The Godfather: Part II (1974) | 129 | 4.26 | 4.20 |
  | 7 | Schindler's List (1993) | 220 | 4.23 | 4.19 |
  | 8 | Goodfellas (1990) | 126 | 4.25 | 4.18 |
  | 9 | Dr. Strangelove (1964) | 97 | 4.27 | 4.18 |
  | 10 | The Dark Knight (2008) | 149 | 4.24 | 4.18 |

## Métricas offline
- **Partición (LAB09):** *temporal leave-one-out*. El último rating de cada usuario va a prueba y el resto a entrenamiento (`temporal_leave_one_out`).
- **Métricas:** RMSE de la predicción del rating, HitRate@10 (proporción de usuarios cuya película de prueba aparece en su Top-10) y cobertura del catálogo. Se guardan en `reports/hybrid_metrics.json`.
- **Estado:** LAB09 todavía no se ha ejecutado, así que no hay métricas del modelo híbrido.
- **LAB08 no tiene métricas offline:** la popularidad y el contenido se evaluaron cualitativamente, revisando el Top-10 y tres consultas por contenido (ver el README).

## Cold start, cobertura y diversidad
- **Usuario nuevo:** recibe el Top-10 de popularidad, que es el mismo para todos.
- **Película nueva:** el recomendador por contenido la cubre si tiene géneros. No la cubren la popularidad (necesita al menos 12 ratings) ni el colaborativo (necesita ratings de entrenamiento). Las 34 películas sin géneros no tienen ninguna señal.
- **Cobertura:** el Top-10 de popularidad cubre 10 de 9,742 películas (0.1 %), siempre las mismas.
- **Diversidad:** es baja en el contenido. En las tres consultas, 9 o 10 de las 10 recomendaciones tienen exactamente los mismos géneros que la consulta (puntuación 1.0). Es sobre-especialización: el sistema no propone nada fuera de esa combinación.
- **Empates:** con solo géneros hay muchos empates en 1.0 (13 películas para *Toy Story*), y el orden entre ellas lo decide el algoritmo de ordenamiento, no ningún criterio de calidad.

## Riesgos y monitoreo
- **Sesgo de popularidad:** la línea base refuerza lo que ya es popular (clásicos de Hollywood muy votados) y no da exposición al catálogo poco visto.
- **Similitud mal interpretada:** un 1.0 significa la misma combinación de géneros, no la misma calidad ni que al usuario le vaya a gustar. La app lo aclara en su texto.
- **Defecto conocido:** en `ContentRecommender.recommend`, el filtro `value != index` compara la puntuación con el índice, así que no excluye de verdad la película consultada. Hoy no aparece en las listas solo por el orden de los empates. Hay que corregirlo antes de LAB09.
- **Datos:** la versión de `ml-latest-small` puede cambiar. Hay que comparar el SHA-256 antes de comparar resultados.
- **Monitoreo propuesto:** cobertura del catálogo, diversidad de géneros dentro de cada lista, proporción de usuarios que caen en el fallback, HitRate@10 por segmento de actividad del usuario, y repetir `uv run pytest -q` ante cualquier cambio de datos o de código.
- **Uso:** no usar en producción ni para decisiones sobre personas. Es un ejercicio académico.
