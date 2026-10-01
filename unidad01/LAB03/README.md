# INF-8239-C2
> Manual laboratorios guiados.
> Guía paso a paso · Ensambles, PCA, t-SNE y selección Green AI
## Unidad 01 - LAB03

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 2304 Mhz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:***	GS66 Stealth 11UH
- ***Physical Memory (RAM):***	32.0 GB
- ***GPU:*** NVIDIA GeForce RTX 3080

## Resumen
En este proyecto guiado, se estuvo utilizando un conjunto de datos descrito en [ficha del dataset](docs/ficha_dataset.md)

Todo el proceso está descrito paso a paso en el notebook: [main.ipynb](notebooks/main.ipynb)

## Resulado
    model    f1_macro	recall_macro  fit_median_s	predict_ms	size_kb	    is_pareto
    svm_c10	 1.000000	1.000000	  0.020105	    3.0063	    5.568359	True
    logistic 0.985086	0.986486	  0.011247	    3.7979	    3.166016	True
    rf_100	 1.000000	1.000000	  0.173395	    31.8002	    424.479492	False
    boost	 1.000000	1.000000	  0.215501	    6.6735	    330.830078	False
    svm_c1	 0.996264	0.996622	  0.037834	    5.9151  	8.068359	False
    rf_300	 0.996264	0.996622	  0.484977	    62.7270	    1262.291992	False

> Basado en las metricas obtenidas de la jecucion de los diferetnes modelos. Los únicos en la frontera de pareto son:`svm_c10` y `logistic`. Los demás modelo son dominados, es decir, hay dos modelos que los superan en diferentes conextos.
> De los dos modelos tomamos el `svm_c10`, es el más exacto en predecir con un f1 de 1, un recall de 1. En cuatno al factor tiempo de ejecuión `svm_c10` es más 
> rápdio. Y por último, en cuanto a espacio en disco `svm_c10` ocupa más que `logistic`, pero no es un tamaño que requiera nuestra ateción comparado con el tiempo que logra.

## Como ejecutar el proyecto
### prerequisitos
- Como gestor de proyecto de python [uv](https://docs.astral.sh/uv/)
    1. Instalar uv

 ### Arranque del proyecto
- Ejecutando el proyecto
    1. Ingresar a la carpeta `/unidad01/LAB03` y ejectuar `uv sync` en su terminal, para instalar las dependencia conetnidas en [pyproject.toml](pyproject.toml). En el proceso de instalación, uv creará un entorno virtual para el proyecto.
    2. Para ejecutar el notebook [notebook](notebooks/main.ipynb) debe abrirlo y en la opción `Select kernel`, debe selecionar el entorno virtual que se creó automáticamente en el paso **2**. Por defecto uv permite que la carpeta src y sus module estén disponibles para el notebook, en caso de utilizar otro gestor de proyecto, el notebook está configurado para cargar src al `sys.pah`
- Correr pruebas unitarias
   1. Luego de haber ejecutado el paso 1 de las sección `Ejecutando el proyecto`, puede correr el comando `uv run pytest` y esto le mostrará la consola con el resultado de las pruebas unitarias