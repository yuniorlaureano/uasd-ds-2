# INF-8239-C2
> Manual laboratorios guiados.
> Búsqueda, selección y auditoría de un dataset público
## Unidad 01 - LAB02
### Modelos avanzados, reducción dimensional y Green AI

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 2304 Mhz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:***	GS66 Stealth 11UH
- ***Physical Memory (RAM):***	32.0 GB
- ***GPU:*** NVIDIA GeForce RTX 3080


## Resumen
En este proyecto guiado, se estuvo utilizando un conjunto de datos descrito en [ficha del dataset](docs/ficha_dataset.md)

Todo el proceso está descrito paso a paso en el notebook: [main.ipynb](notebooks/main.ipynb)

## Resultado

    dummy 0.354
    svm   0.996

                precision    recall  f1-score   support

              0       1.00      0.99      1.00       148
              1       0.99      1.00      1.00       122

        accuracy                           1.00       270
       macro avg       1.00      1.00      1.00       270
    weighted avg       1.00      1.00      1.00       270

El modelo SVM alcanzó un F1 macro de 0.996 sobre el conjunto de prueba (270 billetes), muy por encima del baseline dummy (0.354), lo que confirma que aprendió un patrón real de separación entre billetes auténticos y falsos.
