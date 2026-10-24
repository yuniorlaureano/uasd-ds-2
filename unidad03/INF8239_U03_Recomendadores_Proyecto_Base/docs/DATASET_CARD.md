# Dataset Card · MovieLens

## Fuente, fecha, versión y hash
- **Nombre:** MovieLens `ml-latest-small`.
- **Fuente:** GroupLens Research, Universidad de Minnesota. https://grouplens.org/datasets/movielens/
- **URL de descarga:** https://files.grouplens.org/datasets/movielens/ml-latest-small.zip (variable `MOVIELENS_URL` en `src/inf8239_u03/config.py`).
- **Versión:** generada el 26 de septiembre de 2018, según `README.txt` del ZIP. `ml-latest-small` es una versión de desarrollo: GroupLens puede regenerarla, por eso se registra el hash.
- **Fecha de descarga:** 23 de octubre de 2026.
- **SHA-256 del ZIP:** `696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436`

## Licencia y cita
Harper, F. M., & Konstan, J. A. (2015). The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems (TiiS)*, 5(4), 19:1–19:19. DOI: 10.1145/2827872.

La licencia de GroupLens permite usarlo con fines de investigación con estas condiciones:
- No se puede afirmar ni insinuar que la Universidad de Minnesota o GroupLens respaldan el trabajo.
- Hay que citar el dataset en cualquier publicación que lo use.
- No se puede redistribuir sin permiso. Por eso `data/raw/*` está en `.gitignore` y cada persona lo descarga.
- No se puede usar con fines comerciales sin permiso de GroupLens.

## Archivos y diccionario

| Archivo | Tamaño | Filas | Uso en el proyecto |
|---|---|---|---|
| `ratings.csv` | 2.4 MB | 100,836 | Popularidad (LAB08) y factorización matricial (LAB09) |
| `movies.csv` | 483 KB | 9,742 | Catálogo, títulos y géneros para el recomendador por contenido |
| `tags.csv` | 116 KB | 3,683 | No se usa todavía |
| `links.csv` | 193 KB | 9,742 | No se usa (identificadores de IMDb y TMDb) |

| Archivo | Columna | Tipo | Descripción | Valores o unidad |
|---|---|---|---|---|
| `ratings.csv` | `userId` | int | Usuario anonimizado | 1–610 |
| `ratings.csv` | `movieId` | int | Película, clave hacia `movies.csv` | Identificador de MovieLens |
| `ratings.csv` | `rating` | float | Valoración explícita | 0.5–5.0, en pasos de 0.5 |
| `ratings.csv` | `timestamp` | int | Momento de la valoración | Segundos desde 1970-01-01 UTC |
| `movies.csv` | `movieId` | int | Película | Identificador de MovieLens |
| `movies.csv` | `title` | str | Título con el año entre paréntesis | Texto, p. ej. `Toy Story (1995)` |
| `movies.csv` | `genres` | str | Géneros separados por `\|` | 19 géneros o `(no genres listed)` |
| `tags.csv` | `userId`, `movieId`, `tag`, `timestamp` | int, int, str, int | Etiqueta libre que un usuario puso a una película | Texto libre |
| `links.csv` | `movieId`, `imdbId`, `tmdbId` | int, int, float | Enlaces a otras bases de datos | `tmdbId` tiene 8 nulos |

## Procedimiento de descarga
```bash
uv run python scripts/download_data.py   # descarga, calcula el SHA-256 y extrae en data/raw/
uv run python scripts/audit_data.py      # valida el contrato y muestra la auditoría
```
`download_zip` (`src/inf8239_u03/data.py`) calcula el SHA-256 sobre los bytes del ZIP y rechaza rutas inseguras antes de extraerlo. `load_movielens` valida el contrato: columnas requeridas, que cada rating tenga película y que los ratings estén entre 0.5 y 5.0.

## Población observada y exclusiones
- **Auditoría:** 100,836 ratings de 610 usuarios sobre 9,742 películas. 9,724 películas tienen al menos un rating y 18 no tienen ninguno.
- **Rango temporal:** del 29-03-1996 (`828124615`) al 24-09-2018 (`1537799250`).
- **Densidad:** 1.70 % (100,836 de 610 × 9,742 pares posibles).
- **Ratings:** media 3.50, mediana 3.5, desviación estándar 1.04. El valor más frecuente es 4.0 (26,818) y el menos frecuente 0.5 (1,370).
- **Películas:** los años del título van de 1902 a 2018. 13 títulos no tienen año, 5 títulos están repetidos y 34 películas no tienen géneros.
- **Exclusión de origen:** GroupLens solo incluyó usuarios con **al menos 20 ratings** (el mínimo observado es 20 y la mediana es 70.5). No hay datos demográficos.
- **Calidad:** no hay nulos en `ratings.csv` ni en `movies.csv`, ni pares usuario-película duplicados.

## Calidad, sesgos y usos prohibidos
- **Sesgo de popularidad:** el 10 % de películas más valoradas concentra el 60 % de los ratings. 3,446 películas tienen un solo rating.
- **Sesgo de selección:** los usuarios eligen qué películas valorar, así que la falta de un rating no significa que no les guste. Además, el filtro de 20 ratings deja fuera a los usuarios ocasionales, que son justo los del caso cold start.
- **Sesgo de escala:** hay más valoraciones altas que bajas (moda 4.0). Cada usuario usa la escala de forma distinta.
- **Géneros pobres:** cada película solo tiene etiquetas de género (19 posibles, 951 combinaciones distintas). Drama (4,361) y Comedy (3,756) dominan. No hay sinopsis, reparto ni director.
- **Población no representativa:** son usuarios voluntarios del sitio MovieLens, sobre todo de habla inglesa, y el catálogo es mayormente de Hollywood.
- **Usos prohibidos:** uso comercial sin permiso, intentar reidentificar a los usuarios, inferir atributos personales (edad, género, orientación) a partir de los gustos, y presentar los resultados como preferencias reales de cualquier población fuera de MovieLens.
