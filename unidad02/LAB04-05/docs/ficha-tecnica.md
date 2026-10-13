### Ficha técnica

> Esta dataset fue creado para el paper 'From Group to Individual Labels using Deep Features', Kotzias et. al,. KDD 2015. Sition web: Kotzias, D. (2015). Sentiment Labelled Sentences [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C57604.
> Para cada website, hay 500 oraciones positivas y 500 negativas. Las oraciones fueron seleccionadas aleatoriamente de un dataset grande de reivews. El objetivo es seleccionar oraciones que tengan una connotación positiva o negativa.

**Poblacion:** Usuarios reales de internet que escribieron en tres plataformas populares:
- Amazon: Específicamente reseñas de la categoría de Celulares y Accesorios.
- IMDb: Reseñas de películas.
- Yelp: Reseñas de restaurantes y comercios locales.

_Los autores tomaron grandes bases de datos de estas plataformas y extrajeron y etiquetaron manualmente 1,000 oraciones de cada una (50% positivas y 50% negativas), filtrando únicamente aquellas con una connotación muy clara para evitar opiniones neutrales._

**Idioma:** ``Inglés (English)`` en su totalidad. Al tratarse de lenguaje de internet, incluye modismos, contracciones informales (como don't, wasn't) y errores tipográficos comunes de plataformas web.

**Periodo de recolección:** El dataset se publicó oficialmente en el repositorio UCI en mayo de 2015. Las reseñas originales de donde se extrajeron los enunciados abarcan un periodo que va desde finales de la década de 2000 hasta 2014, coincidiendo con los datasets públicos de origen (como el Yelp Dataset Challenge y los archivos históricos de Amazon recopilados por McAuley y Leskovec) [sentiment-analysis-python](https://github.com/tarunsharma87/sentiment-analysis-python)

**Paper:** [From Group to Individual Labels Using Deep Features](https://dl.acm.org/doi/10.1145/2783258.2783380)

**Origen del dataset:** [
Sentiment Labelled Sentences](https://archive.ics.uci.edu/dataset/331/sentiment%2Blabelled%2Bsentences)

**Feature:** 
- text: representa el texto de la reseña que hizo el usuario de los tres website estudiados.

**Traget:**
- label: representa la connotación del texto etiquetado como ``|1 (positivo)`` o ``0 (negativo)``.

**Tamaño del dataset:**
- 1,000 reseñas para Amazon. 50% postivas, 50% nevativas.
- 1,000 reseñas para IMDb. 50% postivas, 50% nevativas.
- 1,000 reseñas para Yelp. 50% postivas, 50% nevativas.

Un total de 3000 reseñas.

**Licencia:**
Creative Commons Attribution 4.0 International (CC BY 4.0)

**Clases:**
La etiqueta puede ser 1 (para positivo), o 0 (para negativo).

**Hipótesis:**
La preguna a responder es si el texto tiene connotación negativa o positiva.

**Dimitrios Kotzias:** Dimitrios Kotzias