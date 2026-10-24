## 3. Crear el corte temporal

###Experimento base
```
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.75
```
## 4. Interpretar la factorización

## 5. Construir y explicar el híbrido

> El proyecto combina una puntuación colaborativa normalizada con una señal de contenido. alpha controla el peso colaborativo. Para usuarios fríos se utiliza un fallback documentado de popularidad/contenido.

```
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.25
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.75
```

1. Mantenga iguales semilla, corte, número de factores y épocas.
2. Compare HitRate@10, cobertura y títulos recomendados.
3. Explique qué señal domina en cada configuración.
4. Seleccione un valor de alpha utilizando evidencia, no preferencia personal.

## 6. Evaluar tres perfiles

Usuario con historial amplio	La lista debe excluir ítems vistos y utilizar señal colaborativa.
Usuario con historial pequeño	Compare estabilidad y dependencia del contenido.
Usuario nuevo	Verifique que el fallback produzca una lista y declare que no es personalizada.

## 7. Comparar costo y utilidad

> Ejecute tres semillas y registre tiempo, métricas y tamaño del modelo. Construya una tabla de Pareto: una configuración está dominada si otra obtiene igual o mejor utilidad con igual o menor costo.


## 8. Revisar riesgos

- Popularidad dominante: los mismos ítems aparecen para muchas personas.
- Burbuja de filtro: poca exposición a categorías distintas.
- Sesgo de selección: solo se observan valoraciones de ítems consumidos.
- Ausencia de demografía: no pueden afirmarse resultados por grupos poblacionales.
- Retroalimentación: recomendaciones futuras pueden modificar las interacciones que luego entrenan el modelo.

## 9. Pruebas

## Cierre interpretativo
Redacción del estudiante
Resultado de ratings:
Resultado de ranking:
Cobertura del catálogo:
Comportamiento del usuario frío:
Configuración seleccionada y evidencia:
Costo computacional:
Riesgo principal y mitigación: