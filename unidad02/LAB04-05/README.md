# INF-8239-C2
> Manual laboratorios guiados.
> Microejemplo · De la imagen al texto

## Unidad 02 - LAB04 y LAB05: 
> ### Desde cero: localizar, aprobar y auditar un corpus público
> ### Clasificación de texto: TF-IDF, Naive Bayes y modelo lineal

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 2304 Mhz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:***	GS66 Stealth 11UH
- ***Physical Memory (RAM):***	32.0 GB
- ***GPU:*** NVIDIA GeForce RTX 3080
-**Sistema operativo:** Windows 11 con WSL habilitado con Ubuntu 24

## Como ejecutar el proyecto
### prerequisitos
- Como gestor de proyecto de python [uv](https://docs.astral.sh/uv/)
    1. Instalar uv

- Sistema operativo
    1. El proyecto se inicializó en ``Windows 11``, se corrieron algunas funcionalidades inciales en este sistema operativo, pero el proyecto completo no puede ser ejecutado en ``Windows``, sino que requiere ``Ubuntu Linux``. Puede utilizar otras ditribuciones de linux, pero para ello debe modificar los comandos que instalan las dependencias y quizás agregar referencias a esas dependencias propias del administrador de paquete que permita la distribución de linux.

- Librerías a instalar en el sistema operativo
    1. **tesseract-ocr** El motor OCR en sí: el programa ejecutable tesseract. Incluye por defecto los datos de inglés (eng) y de detección de orientación (osd).
    2. **tesseract-ocr-spa** Los datos del idioma español (spa.traineddata): el modelo entrenado que conoce la ñ, los acentos, ¿ y ¡, y los patrones de palabras del español.

    > Nota: solo debe instalar esas librerías. Su contraparte que se instala automáticamente a python cuand ocorra ``uv sync`` hará uso de estas como dependencias.
### Arranque del proyecto
- Ejecutando el proyecto
    1. Como estos demos dependen de Linux, en este caso Ubuntu, debe clonar el repositorio en dicho sistema operativo o en la distrución habilitadad en su WSL. Luego habre la carpeta ``uasd-ds-2/unidad02/DEMO02`` en su editor de preferencia, en este caso utilizamos vscode.
    2. Si utiliza WSL con vscode, debe instalar las extensiones:
        - **WSL**. De microsoftt. Eso le permite poder abrir código en vscode desde su Windows, apuntando a su distribución en WSL.
        - **Python**. Pack de microsoft
        - **Jupyter**. De microsoft. Este le permite ejecutar Notebooks en vscode sin necesidad de tener un servidor Jupyter.

        2.1 Dentro de la carpeta del proyecto, puede ejecutar ``code .``, esto abrirá una instancia del vscdoe apuntando a esa ruta en WSL. La primera vez que haga esto, se instalará un servidor de vscode en WSL para crera el puente entre ambos sistemas operativo.
    3. Si ejecuta desde una distribución linux directa, sin WSL
        - Desde el royecto clonado y la carpeta  ``uasd-ds-2/unidad02/DEMO02``, debe abrir vscode. En este caso solo necesita las extensiones:
            - **Python**. Pack de microsoft
            - **Jupyter**. De microsoft. Este le permite ejecutar Notebooks en vscode sin necesidad de tener un servidor Jupyter.

    4. Ingresar a la carpeta `/unidad02/DEMO02` y ejectuar `uv sync` en su terminal, para instalar las dependencia conetnidas en [pyproject.toml](pyproject.toml). En el proceso de instalación, uv creará un entorno virtual para el proyecto.
    5. Para ejecutar los notebooks [demo03](notebooks/demo03.ipynb) o [demo02](notebooks/demo02.ipynb) debe abrirlo y en la opción `Select kernel`, debe selecionar el entorno virtual que se creó automáticamente en el paso **4**. Por defecto uv permite que la carpeta src y sus module estén disponibles para el notebook, en caso de utilizar otro gestor de proyecto, el notebook está configurado para cargar src al `sys.pah`
- Correr pruebas unitarias
   1. Luego de haber ejecutado los pasos anteriores de la sección `Ejecutando el proyecto`, puede correr el comando `uv run pytest` y esto le mostrará la consola con el resultado de las pruebas unitarias