# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 03 - LAB08 Sistemas recomendadores con MovieLens.
### Popularidad ponderada y recomendación por contenido: evidencia, cold start y sobre-especialización.

Proyecto base del autor académico Edwin Ramón José Nolasco. El dataset de muestra de `tests/` prueba el código; la evidencia final usa MovieLens.

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:*** GS66 Stealth 11UH
- ***Physical Memory (RAM):*** 32.0 GB
- ***Entorno:*** Windows 11, Python 3.12.10, pandas 2.3.3, scikit-learn 1.9.1, gestionado con `uv`.

## Resumen
Construí dos recomendadores sobre MovieLens `ml-latest-small`: una línea base de **popularidad ponderada** (media bayesiana con un mínimo de votos) y un recomendador **por contenido** (TF-IDF de géneros y similitud coseno). El código reutilizable está en `src/inf8239_u03`, los pasos del laboratorio en `scripts/` y las pruebas en `tests/`.

**Resultado principal:** la popularidad da un Top-10 estable y reconocible, encabezado por *The Shawshank Redemption* (4.40). El recomendador por contenido encuentra películas del mismo género, pero no sabe ordenarlas: en las tres consultas, 9 o 10 de las 10 recomendaciones tienen puntuación 1.0.

- Dataset card: [docs/DATASET_CARD.md](docs/DATASET_CARD.md)
- System card: [docs/SYSTEM_CARD.md](docs/SYSTEM_CARD.md)

## Estructura del proyecto

```
INF8239_U03_Recomendadores_Proyecto_Base/
├── app/streamlit_app.py         # App local: recomendación por contenido
├── data/raw/                    # MovieLens descargado (no se versiona)
├── docs/
│   ├── DATASET_CARD.md
│   └── SYSTEM_CARD.md
├── models/                      # Modelos de LAB09 (no se versionan)
├── reports/                     # Salidas de los scripts (no se versionan)
│   ├── popular_top10.csv
│   └── content_recommendations.csv
├── scripts/
│   ├── download_data.py         # Descarga, SHA-256 y extracción
│   ├── audit_data.py            # Auditoría del dataset
│   ├── lab08_content.py         # Popularidad y contenido
│   └── lab09_hybrid.py          # Factorización matricial e híbrido
├── src/inf8239_u03/
│   ├── config.py                # Rutas, URL y semilla
│   ├── data.py                  # Descarga, carga y contrato de datos
│   ├── metrics.py               # HitRate@K y cobertura
│   └── recommenders.py          # Popularidad, contenido, MF y partición temporal
└── tests/                       # Pruebas unitarias (pytest)
```

## Cómo ejecutar el proyecto

### Instalación
Desde la carpeta `uasd-ds-2/unidad03/INF8239_U03_Recomendadores_Proyecto_Base`:
```bash
uv python install 3.12
uv sync
uv run pytest -q
uv run python scripts/download_data.py
uv run python scripts/audit_data.py
```

### Laboratorios
```bash
uv run python scripts/lab08_content.py
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.75
uv run streamlit run app/streamlit_app.py
```
La app abre en http://localhost:8501. Se elige una película de referencia y se pulsa **Recomendar**.

## Resultados (LAB08)

### 1. Descarga y hash
```
Destino: data/raw
SHA-256: 696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436
```
Versión `ml-latest-small` generada el 26-09-2018 y descargada el 23-10-2026. Como GroupLens puede regenerar esta versión, el hash permite comprobar que dos ejecuciones usan los mismos datos.

### 2. Auditoría

| Indicador | Valor |
|---|---|
| Ratings | 100,836 |
| Usuarios | 610 (mínimo 20 ratings cada uno) |
| Películas en el catálogo / con ratings | 9,742 / 9,724 |
| Rango temporal | 29-03-1996 a 24-09-2018 |
| Densidad | 1.70 % |
| Rating medio (desviación) | 3.50 (1.04) |
| Películas con un solo rating | 3,446 |
| Películas sin géneros | 34 |

La matriz usuario-película es muy dispersa: el 98.3 % de los pares no tiene rating. El 10 % de películas más valoradas concentra el 60 % de los ratings.

### 3. Top-10 de popularidad ([`reports/popular_top10.csv`](reports/popular_top10.csv))
Media bayesiana con `m` = 12 votos mínimos (percentil 80) y `C` = 3.50 (media global).

| # | Película | Votos | Media | Score |
|---|---|---|---|---|
| 1 | The Shawshank Redemption (1994) | 317 | 4.43 | 4.40 |
| 2 | The Godfather (1972) | 192 | 4.29 | 4.24 |
| 3 | Fight Club (1999) | 218 | 4.27 | 4.23 |
| 4 | Star Wars: Episode IV - A New Hope (1977) | 251 | 4.23 | 4.20 |
| 5 | The Usual Suspects (1995) | 204 | 4.24 | 4.20 |
| 6 | The Godfather: Part II (1974) | 129 | 4.26 | 4.20 |
| 7 | Schindler's List (1993) | 220 | 4.23 | 4.19 |
| 8 | Goodfellas (1990) | 126 | 4.25 | 4.18 |
| 9 | Dr. Strangelove (1964) | 97 | 4.27 | 4.18 |
| 10 | The Dark Knight (2008) | 149 | 4.24 | 4.18 |

La ponderación funciona: ninguna película con pocos votos y media de 5.0 se cuela en el ranking. A cambio, son clásicos muy votados, casi todos de Hollywood, y la lista es la misma para todos los usuarios.

### 4. Tres consultas por contenido
TF-IDF sobre los géneros y similitud coseno. La consulta de *Toy Story* está en [`reports/content_recommendations.csv`](reports/content_recommendations.csv).

| Consulta (géneros) | Top-10 | Puntuación |
|---|---|---|
| *Toy Story (1995)* (Adventure\|Animation\|Children\|Comedy\|Fantasy) | Turbo, The Emperor's New Groove, The Adventures of Rocky and Bullwinkle, Toy Story 2, Asterix and the Vikings, Antz, The Wild, Shrek the Third, The Good Dinosaur, Monsters, Inc. | Las 10 con 1.0 |
| *Matrix, The (1999)* (Action\|Sci-Fi\|Thriller) | Screamers, The Terminator, Repo Men, Predators, Johnny Mnemonic, The Chronicles of Riddick, Ready Player One, Total Recall (2012), Equilibrium, Solo (1996) | Las 10 con 1.0 |
| *Pulp Fiction (1994)* (Comedy\|Crime\|Drama\|Thriller) | Confessions of a Dangerous Mind, The Informant!, Leaves of Grass, Freeway, In Bruges, Man Bites Dog, Party Monster, Beautiful Creatures, Fargo, Life Eternal | 9 con 1.0; *Life Eternal* con 0.93 |

- **Lo que hace bien:** todas las recomendaciones son del mismo tipo que la consulta. Para *Toy Story* son todas películas animadas e infantiles.
- **Lo que no hace:** el 1.0 solo significa "misma combinación de géneros". *Screamers* queda igual de cerca de *Matrix* que *The Terminator*, y *Fargo* aparece en el puesto 9 detrás de títulos poco conocidos.
- **Empates:** para *Toy Story* hay 13 películas empatadas en 1.0. El orden entre ellas lo decide el algoritmo de ordenamiento, no la calidad ni la popularidad.

### 5. Pruebas
```
uv run pytest -q
.......                                                                  [100%]
7 passed
```

| Contrato | Prueba |
|---|---|
| Columnas requeridas y ratings con película | `test_valid_contract`, `test_rejects_orphan_rating` |
| La película consultada no aparece en su lista y no hay repetidos | `test_content_excludes_query_and_returns_unique_items` |
| La popularidad incluye `weighted_score` | `test_popularity_contains_weighted_score` |
| HitRate@K y cobertura | `test_ranking_metrics` |
| Partición temporal y factorización matricial | `tests/test_matrix_factorization.py` |

> **Defecto conocido:** en `src/inf8239_u03/recommenders.py:33`, el filtro `value != index` compara la *puntuación* con el *índice*, así que no excluye de verdad la película consultada. La prueba pasa con el dataset de muestra y en MovieLens la consulta no aparece solo por el orden de los empates. La corrección es `[i for i in scores.argsort()[::-1] if i != index][:k]`.

## Cierre interpretativo

- **Resultado principal:** La popularidad ponderada da un Top-10 estable y creíble, encabezado por *The Shawshank Redemption* (4.40), *The Godfather* (4.24) y *Fight Club* (4.23). El recomendador por contenido encuentra películas del mismo género, pero no sabe ordenarlas: en las tres consultas, 9 o 10 de las 10 recomendaciones tienen puntuación 1.0.
- **Evidencia utilizada:** MovieLens `ml-latest-small` con SHA-256 `696d65a3…e436`, documentado en el [Dataset Card](docs/DATASET_CARD.md). La auditoría da 100,836 ratings, 610 usuarios, 9,742 películas y 1.70 % de densidad. Usé el Top-10 de popularidad, tres consultas por contenido (*Toy Story*, *Matrix* y *Pulp Fiction*), 7 pruebas aprobadas y el [System Card](docs/SYSTEM_CARD.md).
- **Qué representa la similitud:** La similitud coseno entre vectores TF-IDF de géneros mide cuánto coinciden dos películas en su etiqueta de género. No mide calidad, trama, tono, director ni el gusto del usuario. Un 1.0 significa "misma combinación exacta de géneros", no "igual de buena" ni "le gustará".
- **Problema de cold start observado:** Un usuario nuevo solo puede recibir el Top-10 de popularidad, que es el mismo para todos. Las películas nuevas o poco vistas tampoco tienen salida por popularidad: 3,446 tienen un solo rating y 18 ninguno, y el umbral de 12 votos las deja fuera. El contenido sí cubre películas sin ratings porque solo necesita géneros, pero falla con las 34 que no tienen géneros.
- **Riesgo de sobre-especialización:** Alto. Las listas por contenido repiten la misma combinación de géneros que la consulta, una "burbuja de género" sin novedad ni diversidad. Como hay tantos empates en 1.0, el orden final no depende de ningún mérito. Por su parte, la popularidad concentra la exposición en pocos clásicos muy votados (sesgo de popularidad).
- **Decisión o siguiente experimento:** Usar la popularidad solo como fallback de cold start, no como recomendador principal. En LAB09, entrenar el híbrido de factorización matricial y contenido (`--factors 20 --epochs 12 --alpha 0.75`) y evaluarlo con *temporal leave-one-out* midiendo RMSE, HitRate@10 y cobertura, comparado con la popularidad. Para el contenido, corregir la exclusión de la consulta, desempatar los 1.0 con la popularidad ponderada y enriquecer las características con `tags.csv` y el año.