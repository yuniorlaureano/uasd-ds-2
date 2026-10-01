# INF-8239-C2
> Manual laboratorios guiados.
> SVM con pipeline, búsqueda de parámetros y evaluación
## Unidad 01 - LAB01

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 2304 Mhz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:***	GS66 Stealth 11UH
- ***Physical Memory (RAM):***	32.0 GB
- ***GPU:*** NVIDIA GeForce RTX 3080


## ⚠️Advertencia 

> Es un caso de estudio para practicar el paso a paso con SVM con pipeline, búsqueda de parámetros y evaluación. No constituye un modelo de uso en ambientes productivos

## Como ejecutar el proyecto
### prerequisitos
- Como gestor de proyecto de python [uv](https://docs.astral.sh/uv/)
    1. Instalar uv

### Arranque del proyecto
- Ejecutando el proyecto
    1. Ingresar a la carpeta `/unidad01/LAB01` y ejectuar `uv sync` en su terminal, para instalar las dependencia conetnidas en [pyproject.toml](pyproject.toml). En el proceso de instalación, uv creará un entorno virtual para el proyecto.
    2. Para ejecutar el notebook [notebook](notebooks/01_svm_guiada.ipynb) debe abrirlo y en la opción `Select kernel`, debe selecionar el entorno virtual que se creó automáticamente en el paso **2**. Por defecto uv permite que la carpeta src y sus module estén disponibles para el notebook, en caso de utilizar otro gestor de proyecto, el notebook está configurado para cargar src al `sys.pah`
- Correr pruebas unitarias
   1. Luego de haber ejecutado el paso 1 de las sección `Ejecutando el proyecto`, puede correr el comando `uv run pytest` y esto le mostrará la consola con el resultado de las pruebas unitarias