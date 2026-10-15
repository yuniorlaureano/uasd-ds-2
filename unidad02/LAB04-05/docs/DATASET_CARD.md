# Dataset Card

## Identificación
- Nombre: Sentiment Labelled Sentences
- Fuente original: https://archive.ics.uci.edu/dataset/331/sentiment%2Blabelled%2Bsentences
- Responsable: Dimitrios Kotzias
- Versión o fecha: 5/29/2015
- Licencia: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Idioma: Inglés (English)

## Propósito y variable objetivo
- text: representa el texto de la reseña que hizo el usuario de los tres website estudiados.
- label: representa la connotación del texto etiquetado como ``|1 (positivo)`` o ``0 (negativo)``.

## Diccionario de datos

| Columna | Tipo | Descripción | Valores o unidad |
|---|---|---|---|
text  |  str   |  representa el texto de la reseña | texto o reseña
label | int64 | representa la connotación del texto etiquetado como 1 (positivo)`` o 0 (negativo) | 0 o 1 (negativo o positivo)

## Procedimiento de obtención
Fui a UCI y allí encontré el dataset [Sentiment Labelled Sentences](https://dl.acm.org/doi/10.1145/2783258.2783380)

## Calidad observada
Los datos fueron limpiados, no contienen nulos, ni duplicados.

## Población cubierta y excluida
Usuarios reales de internet que escribieron en tres plataformas populares:
- Amazon: Específicamente reseñas de la categoría de Celulares y Accesorios.
- IMDb: Reseñas de películas.
- Yelp: Reseñas de restaurantes y comercios locales.

## Riesgos, sesgos y usos prohibidos
El dataset es de uso académico. Los sesgos posibles son las ironías manejadas en el texto y los emogies utilizados. En el caso de los riesgos, podrían darse al momento de entrenar, podríamos no dividir bien y causar fuga de datos