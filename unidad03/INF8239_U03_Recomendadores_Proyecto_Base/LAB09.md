# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 03 - LAB09 Sistemas recomendadores con MovieLens.
### Factorización matricial e híbrido: corte temporal, perfiles, costo y riesgos.

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:*** GS66 Stealth 11UH
- ***Physical Memory (RAM):*** 32.0 GB
- ***Entorno:*** Windows 11, Python 3.12.10, pandas 2.3.3, scikit-learn 1.9.1, gestionado con `uv`. Todo corre en CPU.

## Resumen
Continúo LAB08 ([LAB08.md](LAB08.md)) con el mismo dataset (SHA-256 `696d65a3…e436`). Entrené una factorización matricial (MF) por SGD y la combiné con la señal de contenido de géneros en un híbrido controlado por `alpha`. Comparé 5 valores de `alpha`, 3 tamaños de factores y 3 semillas (45 configuraciones), evalué tres perfiles de usuario y armé una tabla de Pareto de costo y utilidad.

**Resultado principal:** el híbrido duplica casi el HitRate@10 de la popularidad (0.038 frente a 0.020), pero la MF no predice ratings mejor que la media de cada usuario (RMSE 1.0255 frente a 1.0231). Selecciono **20 factores y `alpha` = 0.5**, con la advertencia de que su ventaja sobre `alpha` = 0.75 está dentro de la variación entre semillas.

## Cómo ejecutar
```bash
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.75             # experimento base
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.25 --seed 42   # comparación de alpha
uv run python scripts/lab09_experiments.py                                              # cuadrícula completa (~6 min)
uv run pytest -q
```

**Cambios al código base:**
- La lógica del híbrido pasó del script a `hybrid_top_n` y `popularity_fallback` (`src/inf8239_u03/recommenders.py`) para poder reutilizarla y probarla. Comprobé que el experimento base da exactamente el mismo resultado que antes.
- `scripts/lab09_hybrid.py` acepta `--seed` y registra el tamaño del modelo (`model_kb`).
- El script original **fallaba** con scikit-learn 1.9 (`TypeError: np.matrix is not supported`), porque el perfil de usuario quedaba como `np.matrix`. Se corrigió con `np.asarray`.
- `MatrixFactorization.top_n` ahora calcula todas las puntuaciones con una sola multiplicación de matrices en lugar de un bucle. El resultado es el mismo.

**Entregables generados:** `reports/hybrid_metrics.json`, `reports/cold_start_fallback.csv`, `reports/lab09_runs.csv` (45 corridas), `reports/lab09_profiles.csv` (listas de los tres perfiles) y `reports/lab09_baseline.json`.

## Resultados

### 3. Corte temporal
`temporal_leave_one_out` ordena los ratings de cada usuario por `timestamp` y separa el **último** para prueba. Así el modelo nunca ve el futuro del usuario que evalúa.

| Partición | Ratings | Usuarios |
|---|---|---|
| Entrenamiento | 100,226 | 610 |
| Prueba | 610 (uno por usuario) | 610 |
| Prueba evaluable | 587 | 587 |

23 usuarios quedan fuera de la evaluación porque su última película **no aparece en entrenamiento**: es cold start de ítem, y la MF no puede puntuar algo que nunca vio.

**Experimento base** (`--factors 20 --epochs 12 --alpha 0.75`, semilla 42):

| RMSE | HitRate@10 | Cobertura | Entrenamiento | Tamaño |
|---|---|---|---|---|
| 1.0264 | 0.0375 (22 de 587) | 7.75 % | 13.7 s | 1,611 KB |

### 4. Interpretar la factorización
La MF representa a cada usuario y cada película con un vector de 20 factores latentes, y predice `media global + usuario · película`. Los factores no tienen nombre: son direcciones que el SGD encuentra para explicar los ratings.

| Predictor | RMSE (587 usuarios) |
|---|---|
| Media global (3.50) | 1.1157 |
| Media de la película | 1.0503 |
| **Media del usuario** | **1.0231** |
| MF, 10 factores (3 semillas) | 1.0300 ± 0.0030 |
| MF, 20 factores (3 semillas) | 1.0255 ± 0.0010 |
| MF, 40 factores (3 semillas) | 1.0203 ± 0.0038 |

- La MF mejora mucho sobre la media global, pero **no supera a la media de cada usuario** salvo con 40 factores, y entonces por solo 0.003.
- **Causa probable:** el modelo no tiene sesgos de usuario ni de película (`b_u`, `b_i`). Tiene que aprender con los factores lo que una sola media por usuario ya explica, y en 12 épocas no lo consigue del todo.
- **Error típico:** un RMSE de 1.03 significa que la predicción se equivoca en alrededor de un punto en una escala de 0.5 a 5.
- **Ratings frente a ranking:** el RMSE mide si el modelo acierta el número. El híbrido solo usa la MF para **ordenar** candidatos, y ahí sí aporta (ver la sección 5).

### 5. Construir y explicar el híbrido
> El proyecto combina una puntuación colaborativa normalizada con una señal de contenido. `alpha` controla el peso colaborativo. Para usuarios fríos se utiliza un fallback documentado de popularidad/contenido.

`hybrid_score = alpha · colaborativo + (1 − alpha) · contenido`, con ambas señales normalizadas entre 0 y 1.

- **Colaborativo:** la predicción de la MF para las 100 películas no vistas con mayor puntuación.
- **Contenido:** la similitud coseno entre esas 100 candidatas y el perfil de géneros del usuario (promedio TF-IDF ponderado por `rating − 2.5`).

**Matiz importante:** el contenido solo **reordena** las 100 candidatas que eligió la MF. Por eso incluso `alpha` = 0 depende de la señal colaborativa.

**Comparación pedida** (20 factores, 12 épocas, mismo corte, semillas 42, 7 y 2026):

| Semilla | HitRate@10 α=0.25 | HitRate@10 α=0.75 | Cobertura α=0.25 | Cobertura α=0.75 |
|---|---|---|---|---|
| 42 | 0.0324 | **0.0375** | **10.6 %** | 7.8 % |
| 7 | 0.0256 | **0.0392** | **10.1 %** | 7.0 % |
| 2026 | **0.0324** | 0.0290 | **9.8 %** | 7.4 % |
| **Media** | 0.0301 | **0.0352** | **10.2 %** | 7.4 % |

**Cuadrícula completa de alpha** (20 factores, media de 3 semillas, 587 usuarios):

| alpha | HitRate@10 | Aciertos (mín.–máx.) | Cobertura | Votos medianos de lo recomendado | Géneros distintos por lista |
|---|---|---|---|---|---|
| 0.00 | 0.0278 | 15–18 | **11.1 %** | — | — |
| 0.25 | 0.0301 | 15–19 | 10.2 % | 79 | 7.9 |
| **0.50** | **0.0380** | 18–27 | 8.5 % | 119 | 9.6 |
| 0.75 | 0.0352 | 17–23 | 7.4 % | 128 | **10.9** |
| 1.00 | 0.0341 | 15–23 | 7.1 % | — | — |

Los votos medianos y los géneros por lista se midieron con la semilla 42.

**Títulos recomendados (usuario 414, semilla 42):**
- α = 0.25: *Intouchables*, *12 Angry Men*, *The Philadelphia Story*, *Life Is Beautiful*, *Modern Times*, *My Life as a Dog*, *Manhattan*… Casi todas son Comedy|Drama (contenido entre 0.90 y 1.00), aunque su puntuación colaborativa sea baja, hasta 0.01 en *The King of Comedy*.
- α = 0.75: *Life Is Beautiful*, *12 Angry Men*, *My Fair Lady*, *Intouchables*, *Annie Hall*, *Psycho*, *The Lives of Others*, *Ben-Hur*, *Shutter Island*… Entran *Psycho* (contenido 0.20) y *Ben-Hur* (0.68) porque la MF las puntúa alto.

**Qué señal domina:**
- **Con `alpha` = 0.25 domina el contenido.** La lista se parece a los géneros favoritos del usuario (Comedy y Drama), cubre más catálogo y recomienda películas menos vistas (mediana de 79 votos). A cambio, cada lista tiene menos variedad de géneros (7.9): es la burbuja de género de LAB08.
- **Con `alpha` = 0.75 domina el colaborativo.** Entran películas fuera del perfil de géneros, cada lista es más variada (10.9 géneros), pero se concentra en títulos populares (mediana de 128 votos) y cubre menos catálogo.
- **Con `alpha` = 0.5** las dos señales se compensan: obtiene el mejor HitRate medio y mantiene una cobertura intermedia.

**Selección por evidencia: 20 factores y `alpha` = 0.5.**
- Tiene el mayor HitRate@10 medio (0.0380) y no está dominada en la tabla de Pareto (sección 7).
- Domina a `alpha` = 0.75 en esos 20 factores: mejor HitRate y mejor cobertura con el mismo costo.
- Da la lista más estable entre semillas para el usuario con historial amplio (Jaccard 0.62).
- **Límite:** la diferencia con 0.75 es de unos 1.7 aciertos sobre 587 usuarios, y los rangos de aciertos se solapan (18–27 frente a 17–23). Con 3 semillas no es una diferencia concluyente. Lo que sí es consistente es que `alpha` ≥ 0.5 supera a `alpha` ≤ 0.25 en HitRate.

### 6. Evaluar tres perfiles
Elegí el usuario con más ratings de entrenamiento, el que tiene menos y un identificador que no existe en el modelo. Usé 20 factores y comparé las tres semillas.

| Perfil | Usuario | Ratings en entrenamiento | ¿Excluye vistos? | Jaccard medio entre semillas (α=0.5) | Fuente |
|---|---|---|---|---|---|
| Historial amplio | 414 | 2,697 | Sí (0 vistos en 45 listas) | 0.62 | híbrido |
| Historial pequeño | 53 | 19 | Sí (0 vistos en 45 listas) | 0.02 | híbrido |
| Usuario nuevo | — | 0 | No aplica | 1.00 | popularidad (no personalizada) |

- **Historial amplio (414):** la lista excluye todo lo visto y usa la señal colaborativa. Con `alpha` = 0.75, *Life Is Beautiful* (colaborativo 1.00) y *12 Angry Men* (0.87) encabezan la lista. Entre semillas se mantiene buena parte de la lista (Jaccard de 0.58 a 0.62 para `alpha` 0.5 y 0.75).
- **Historial pequeño (53):** con solo 19 ratings, los factores del usuario son casi ruido. **Ninguna película se repite en las tres semillas**, para ningún `alpha` (Jaccard entre 0.00 y 0.02). Con `alpha` = 0.25, tres de las cuatro primeras tienen contenido 1.00 (Comedy|Drama|Romance, como su perfil). Con `alpha` = 0.75 sube *The Godfather* (colaborativo 1.00). Como el contenido solo reordena candidatas que eligió la MF, no puede estabilizar la lista. Este perfil depende del contenido para tener sentido, pero el sistema no le da al contenido una lista propia.
- **Usuario nuevo:** `hybrid_top_n` detecta que el usuario no existe y devuelve 10 películas por popularidad, marcadas con `source = "popularidad (no personalizada)"`: *Forrest Gump*, *The Shawshank Redemption*, *Pulp Fiction*, *Matrix*, *The Silence of the Lambs*, *Star Wars IV*, *Braveheart*, *Jurassic Park*, *Terminator 2* y *Fight Club*. La lista es idéntica para cualquier semilla y cualquier `alpha`. Este fallback ordena por número de votos, así que no coincide con el Top-10 ponderado de LAB08.

### 7. Comparar costo y utilidad
Tres semillas (42, 7 y 2026) por configuración. La utilidad es HitRate@10 y cobertura; el costo, el tamaño del modelo y el tiempo.

| Factores | alpha | HitRate@10 | Cobertura | Entrenamiento (s) | Tamaño (KB) | ¿Dominada? |
|---|---|---|---|---|---|---|
| 10 | 0.00 | 0.0256 | 9.0 % | 13.6 ± 0.7 | 806 | No |
| 10 | 0.25 | 0.0261 | 8.3 % | 13.6 ± 0.7 | 806 | No |
| 10 | 0.50 | 0.0324 | 6.6 % | 13.6 ± 0.7 | 806 | No |
| **10** | **0.75** | **0.0346** | 5.6 % | 13.6 ± 0.7 | **806** | **No** |
| 10 | 1.00 | 0.0329 | 5.4 % | 13.6 ± 0.7 | 806 | Sí, por 10 / 0.75 |
| 20 | 0.00 | 0.0278 | 11.1 % | 13.8 ± 0.5 | 1,611 | No |
| 20 | 0.25 | 0.0301 | 10.2 % | 13.8 ± 0.5 | 1,611 | No |
| **20** | **0.50** | **0.0380** | 8.5 % | 13.8 ± 0.5 | 1,611 | **No** |
| 20 | 0.75 | 0.0352 | 7.4 % | 13.8 ± 0.5 | 1,611 | Sí, por 20 / 0.50 |
| 20 | 1.00 | 0.0341 | 7.1 % | 13.8 ± 0.5 | 1,611 | Sí, por 20 / 0.50 y 20 / 0.75 |
| **40** | **0.00** | 0.0278 | **13.7 %** | 14.1 ± 0.2 | 3,222 | **No** |
| 40 | 0.25 | 0.0273 | 12.5 % | 14.1 ± 0.2 | 3,222 | Sí, por 40 / 0.00 |
| 40 | 0.50 | 0.0363 | 10.8 % | 14.1 ± 0.2 | 3,222 | No |
| 40 | 0.75 | 0.0335 | 10.0 % | 14.1 ± 0.2 | 3,222 | Sí, por 40 / 0.50 |
| 40 | 1.00 | 0.0284 | 9.8 % | 14.1 ± 0.2 | 3,222 | Sí, por 20 / 0.25, 40 / 0.50 y 40 / 0.75 |
| Popularidad | — | 0.0204 | 0.1 % | 0 | — | Sí, por cualquier híbrido |

Una configuración está dominada si otra obtiene igual o mejor HitRate y cobertura con igual o menor tamaño. No usé el tiempo de entrenamiento para decidir porque es prácticamente igual en todas: entre 13.6 y 14.1 s, con una desviación de hasta 0.7 s.

- **El tamaño crece lineal con los factores:** `(610 usuarios + 9,701 películas) × factores × 8 bytes`.
- **El tiempo de entrenamiento casi no cambia:** lo domina el bucle de Python que recorre los 100,226 ratings, no el tamaño de los vectores. Generar las listas de los 587 usuarios tarda unos 4.7 s.
- **Frente de Pareto:** 10 / 0.75 si importa la memoria (la mitad del tamaño y un HitRate 0.003 menor), 20 / 0.50 para el mejor HitRate y 40 / 0.00 para la mejor cobertura.
- **La popularidad** es gratis, pero tiene el peor HitRate (12 de 587) y recomienda lo mismo a todos.

### 8. Revisar riesgos
- **Popularidad dominante:** con `alpha` = 0.5, *Fight Club* aparece en el Top-10 del **35 %** de los usuarios, *Inception* en el 29 % y *City of God* en el 28 %. Las películas recomendadas tienen una mediana de 119 votos, mientras que la mediana del catálogo es de 3. Subir `alpha` empeora la concentración: con 0.75 se recomiendan 752 películas distintas, frente a 1,033 con 0.25.
- **Burbuja de filtro:** con `alpha` bajo, las listas repiten los géneros del perfil (7.9 géneros distintos por lista con 0.25, frente a 10.9 con 0.75). Hay que mirar las dos burbujas, la de género y la de popularidad, porque `alpha` cambia una por la otra.
- **Sesgo de selección:** solo se observan valoraciones de películas que el usuario eligió ver. No haber valorado una película no significa que no guste, y el HitRate premia predecir lo que el usuario vio después, no lo que le habría gustado.
- **Ausencia de demografía:** MovieLens no tiene edad, género ni país. No puedo afirmar que el sistema funcione igual para ningún grupo de población. Solo puedo segmentar por actividad, y ahí el usuario con poco historial recibe listas inestables.
- **Retroalimentación:** si estas listas se mostraran, la gente vería y valoraría más *Fight Club* o *Inception*, el siguiente entrenamiento las reforzaría y el catálogo poco visto seguiría sin datos. La evaluación offline no detecta este ciclo.

### 9. Pruebas
```
uv run pytest -q
..........                                                               [100%]
10 passed
```

| Contrato | Prueba |
|---|---|
| El corte temporal deja el último evento en prueba | `test_temporal_split_keeps_last_event` |
| La MF predice un valor finito | `test_matrix_factorization_predicts_finite_value` |
| HitRate@K y cobertura | `test_ranking_metrics` |
| **El híbrido excluye vistos y no repite ítems** | `test_hybrid_excludes_seen_items` (nueva) |
| **Con `alpha` = 1 el orden es el colaborativo** | `test_alpha_one_follows_collaborative_order` (nueva) |
| **El usuario nuevo recibe un fallback declarado como no personalizado** | `test_cold_user_gets_declared_fallback` (nueva) |
| Contrato de datos, contenido y popularidad (LAB08) | `test_valid_contract`, `test_rejects_orphan_rating`, `test_content_*`, `test_popularity_*` |

## Cierre interpretativo

- **Resultado de ratings:** La MF con 20 factores obtiene un RMSE de 1.0255 ± 0.0010 (3 semillas), mucho mejor que la media global (1.1157), pero ligeramente peor que predecir la media de cada usuario (1.0231). Solo con 40 factores la supera, por 0.003. Al modelo le faltan los sesgos de usuario y de película.
- **Resultado de ranking:** El híbrido con 20 factores y `alpha` = 0.5 acierta la siguiente película del usuario en su Top-10 en el 3.8 % de los casos (22 de 587 de media), casi el doble que la popularidad (2.0 %). En términos absolutos es poco: en el 96 % de los usuarios la película siguiente no está en la lista.
- **Cobertura del catálogo:** El híbrido seleccionado recomienda el 8.5 % del catálogo entrenado, frente al 0.1 % de la popularidad. La cobertura baja a medida que sube `alpha`: de 11.1 % con 0 a 7.1 % con 1.0.
- **Comportamiento del usuario frío:** El usuario nuevo recibe siempre las mismas 10 películas por popularidad, marcadas como no personalizadas, y la prueba lo verifica. El usuario con solo 19 ratings sí recibe un híbrido, pero sus listas cambian casi por completo de una semilla a otra (Jaccard 0.02), mientras que el usuario con 2,697 ratings conserva el 62 %. Además hay cold start de ítem: 23 películas de prueba no existían en entrenamiento.
- **Configuración seleccionada y evidencia:** 20 factores y `alpha` = 0.5. Tiene el mejor HitRate medio, domina a `alpha` = 0.75 en el mismo tamaño y está en el frente de Pareto. Su ventaja sobre 0.75 (1.7 aciertos) está dentro del rango entre semillas, así que la sostengo como la mejor opción observada, no como una diferencia demostrada. Si la memoria importa, 10 factores con `alpha` = 0.75 da casi lo mismo con la mitad del tamaño.
- **Costo computacional:** Entrenar toma entre 13.6 y 14.1 s en un i7-11800H con cualquier número de factores, porque lo domina el bucle de Python. El modelo ocupa 806, 1,611 o 3,222 KB según los factores, y recomendar a 587 usuarios toma unos 4.7 s. La cuadrícula completa (45 configuraciones) tardó unos 6 minutos.
- **Riesgo principal y mitigación:** La popularidad dominante. Con `alpha` = 0.5, *Fight Club* aparece para el 35 % de los usuarios, y un ciclo de retroalimentación lo reforzaría. Para mitigarlo propongo: monitorear la cobertura y la frecuencia del ítem más recomendado, usar `alpha` ≤ 0.5 o penalizar la popularidad al reordenar, dar a los usuarios con poco historial una lista propia por contenido en lugar de solo reordenar las candidatas de la MF, añadir sesgos `b_u`/`b_i` a la MF, y evaluar con más semillas antes de afirmar diferencias pequeñas.

> **Interpretación responsable:** son métricas offline sobre un solo corte temporal de usuarios voluntarios de MovieLens. No miden satisfacción real ni se generalizan a otras poblaciones.
