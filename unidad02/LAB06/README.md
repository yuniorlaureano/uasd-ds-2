# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 02 - LAB06 Embeddings y análisis responsable de redes.
### Similitud semántica, centralidades, comunidades y límites.

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 2304 Mhz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:***	GS66 Stealth 11UH
- ***Physical Memory (RAM):***	32.0 GB
- ***GPU:*** NVIDIA GeForce RTX 3080

## Resumen
Este laboratorio no consistió en escribir código, más bien en ejecutar el proyecto ``INF8239_U02_NLP_Proyecto_Base`` provisto por el profe Edwing para explorar y experimentar como cambian las métricas bajo la manipulación de ceritos parámetros. En este apatado no trabajé directamente el código, sino ejecución, porque esa parte la practiqué en [U2 LAB04-05: Laboratorio 04](https://github.com/yuniorlaureano/uasd-ds-2/blob/master/unidad02/LAB04-05/notebooks/LAB04.ipynb)

## Resultados

1. Registre los vecinos obtenidos con window=5. ``--word operación``
```
[
    ('recomiendo', 0.2783249020576477),
    ('resultado', 0.276801198720932), 
    ('sistema', 0.2327394187450409), 
    ('confuso', 0.17735466361045837), 
    ('llegó', 0.17678046226501465), 
    ('fue', 0.16485843062400818), 
    ('experiencia', 0.1628860980272293), 
    ('funcionó', 0.1355970948934555), 
    ('claro', 0.13449051976203918), 
    ('está', 0.1271587461233139)
]
```
2. Cambie solamente window o min_count en el script.
    Hiceel cambios de _min_count = 2_.
    El resultado fue:
    ```
    ocabulario: 12 
    Cobertura: 0.481
    La palabra 'operación' no está en el vocabulario
    ```

3. Ejecute nuevamente y compare cobertura y vecinos. Explique por qué el cambio modifica el tipo de contexto capturado.

    > Obtuve dicho resultado porque la ocurrencia de ``operación`` es solo una en todo el corpus de ejemplo.
4. Restaure o documente el valor seleccionado.

    El valor que seleccioné fue _min_count = 2_

5. Resultado estructural de la red

    [network](/network.png)

7. Interpretación permitida:

    Cuando se eleva el numero de palabras a tomar en cuenta, como elevar el min_count de 1 a 2, esto lo que hace es tomar en cuenta aquellas palabras que tienen más de una ocurrencia en el corpus. Esto podría hacer más predictible el modelo, según mi opinión, porque puede tener el contexto coloquios o palabras que los usuarios sí usen en su generalidad, más que algo random que alguien uso de momento.