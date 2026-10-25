# LAB12 — Auditoría de equidad con Fairlearn

**Sistema:** Territorial Review DSS - Synthetic · **Fecha:** 2026-10-25 · **Responsable:** Data Scientist · **Aprueba:** Product Owner

Reproducir:
```bash
uv run python scripts/describe_dataset.py
uv run python scripts/lab12_audit.py --model logistic
uv run python scripts/lab12_audit.py --model tree
uv run python scripts/lab12_baseline.py
```
Resultados en `reports/lab12/{logistic,tree,baseline_rule}/`.

## 1. Comprender el dataset

| Comprobación | Resultado | Lectura |
|---|---|---|
| Distribución de target | 55.2% positivos, 44.8% negativos | El desbalance es leve, pero accuracy no basta. Trata igual un falso negativo (caso urgente que se retrasa) y un falso positivo (revisión innecesaria), y aquí el daño prioritario es el falso negativo. Por eso la métrica principal es recall. |
| Tamaño por grupo | G1 = 396, G2 = 244 en total. En test: G1 = 101 (49 positivos), G2 = 59 (43 positivos, **16 negativos**) | La comparación G1 vs G2 tiene soporte para recall. El FPR de G2 se calcula con 16 negativos: un solo caso cambia el valor en 0.06. |
| Corte temporal | Train hasta 2026-09-24, test desde 2026-09-25 (75/25) | En producción el modelo puntúa casos futuros. Una partición aleatoria mezclaría casos posteriores en el entrenamiento y daría métricas optimistas. |
| Variables excluidas | `case_id`, `received_date`, `protected_group`, `target` | Quitar `protected_group` no elimina el sesgo indirecto. G2 tiene menor `infrastructure_score` (0.44 vs 0.57) y mayor `exposure` (0.56 vs 0.47), así que el modelo puede reconstruir parte del grupo a partir de esas variables. Por eso igual se audita por grupo. |

## 2. Métricas globales (test, n = 160)

| Modelo | Accuracy | Recall | Precisión | FPR | Tasa de selección | Brecha de recall | Brecha de FPR | Entrenamiento | Tamaño |
|---|---|---|---|---|---|---|---|---|---|
| **Regresión logística** | 0.719 | **0.717** | 0.776 | 0.279 | 0.531 | **0.138** ✅ | **0.125** ✅ | 0.04 s | 3.6 KB |
| Árbol (max_depth = 5) | 0.706 | 0.717 | 0.759 | 0.309 | 0.544 | 0.181 ❌ | 0.168 ❌ | 0.05 s | 7.9 KB |
| Regla no predictiva (LAB11) | 0.588 | 0.359 ❌ | 0.825 | 0.103 | 0.250 | 0.069 | 0.053 | — | — |

Umbrales (`configs/governance.yml`): recall ≥ 0.68, brechas ≤ 0.16. Los tiempos de entrenamiento varían un poco entre ejecuciones.

## 3. Métricas por grupo

| Modelo | Grupo | n | Positivos | Recall | FPR | Tasa de selección | Precisión |
|---|---|---|---|---|---|---|---|
| Logística | G1 | 101 | 49 | **0.653** ⚠️ | 0.250 | 0.446 | 0.711 |
| Logística | G2 | 59 | 43 | 0.791 | 0.375 | 0.678 | 0.850 |
| Árbol | G1 | 101 | 49 | 0.633 ⚠️ | 0.269 | 0.446 | 0.689 |
| Árbol | G2 | 59 | 43 | 0.814 | 0.438 | 0.712 | 0.833 |
| Regla | G1 | 101 | 49 | 0.327 | 0.115 | 0.218 | 0.727 |
| Regla | G2 | 59 | 43 | 0.395 | 0.062 | 0.305 | 0.944 |

**Lectura.** La logística cumple el umbral global, pero el promedio esconde una falla en un
grupo: el recall de G1 (0.653) queda bajo 0.68. Uno de cada tres casos positivos de G1 no
se detecta. En G2 pasa lo contrario: más revisiones innecesarias (FPR 0.375). Esto contradice
la hipótesis de R01 en LAB11, que esperaba menor recall en G2, y muestra por qué hay que
medir en vez de suponer. El registro de riesgos debe actualizarse.

**Incertidumbre.** Un bootstrap de 1000 remuestreos del test da, para la logística, un
intervalo 95% de **[0.01, 0.31]** para la brecha de recall y de [0.01, 0.40] para la de FPR.
Que la brecha puntual sea menor que 0.16 no garantiza que la brecha real también lo sea.

## 4. Análisis interseccional (grupo × edad)

**Mínimo documentado:** solo se interpreta un subgrupo con n ≥ 20, y además ≥ 10 positivos para
recall o ≥ 10 negativos para FPR. Los subgrupos más pequeños se muestran, no se ocultan, pero
no se sacan conclusiones de ellos.

| Subgrupo | n | Positivos | Recall logística | Recall árbol | ¿Interpretable? |
|---|---|---|---|---|---|
| G1 · 18-29 | 18 | 4 | 0.750 | 0.750 | No (n < 20) |
| G1 · 30-44 | 24 | 16 | **0.563** | 0.625 | Sí (recall) |
| G1 · 45-59 | 35 | 17 | **0.588** | 0.647 | Sí (recall y FPR) |
| G1 · 60+ | 24 | 12 | 0.833 | 0.583 | Sí (recall) |
| G2 · 18-29 | 11 | 8 | 0.875 | 1.000 | No |
| G2 · 30-44 | 14 | 12 | 0.667 | 0.833 | No |
| G2 · 45-59 | 8 | 6 | 1.000 | 0.667 | No |
| G2 · 60+ | 26 | 17 | 0.765 | 0.765 | Sí (recall) |

El recall bajo de la logística en G1 se concentra en los tramos de 30 a 59 años. El árbol
mejora esos dos tramos pero baja mucho en G1 · 60+ (0.583). Cuatro de los ocho subgrupos no
tienen soporte suficiente, y faltan datos de G2 por tramo de edad.

## 5. Comparación y Green AI

- **Árbol vs logística:** misma utilidad (recall 0.717), más falsos positivos, brechas fuera de tolerancia y 2.2 veces el tamaño. Más complejidad no aporta nada: **no está justificado**.
- **Logística vs regla no predictiva:** la regla tiene brechas menores, pero solo porque detecta pocos casos (recall 0.36). Deja sin detectar casi dos de cada tres casos positivos. Brechas pequeñas a costa de tanta utilidad no son una opción aceptable como sistema principal. La regla se mantiene como modo seguro y como red de seguridad junto al modelo.
- **Green AI:** la logística es la opción suficiente. Se entrena en menos de 0.1 s en CPU, pesa 3.6 KB (el límite es 1024 KB) y es interpretable por coeficientes. Su costo energético es despreciable, y no hay razón para probar modelos más pesados mientras el problema principal sea de datos y de umbral, no de capacidad.

## 6. Por qué una brecha no prueba discriminación causal

La brecha de recall entre G1 y G2 es una **asociación observada en 160 casos sintéticos**, no
una prueba de que el modelo trate peor a G1 *por* pertenecer a G1. Puede deberse a:
1. **Variación de muestreo:** el intervalo de la brecha va de 0.01 a 0.31.
2. **Diferencias en la tasa base y en la dificultad del caso:** G2 tiene 73% de positivos en test y G1 49%. Un umbral único funciona distinto en cada grupo.
3. **Proxies y calidad de medición:** si `previous_incidents` refleja cuánto reporta una zona y no cuánto riesgo tiene (R06), el error viene de los datos, no del algoritmo.
4. **Un solo corte temporal:** otro periodo podría dar otra brecha.

Por eso la brecha obliga a **investigar** (revisar los casos de G1 que el modelo no detectó,
calibrar el umbral, repetir con otro corte, analizar las variables), no a concluir. Para afirmar
discriminación causal haría falta un diseño que controle esas explicaciones alternativas.

## 7. Decisión

**REVISAR.** Se elige la regresión logística como candidata, pero no se despliega hasta:
1. Ajustar el umbral de decisión y verificar que el recall de G1 llegue a 0.68 o más sin que la brecha de FPR pase de 0.16 (Data Scientist).
2. Revisar manualmente los 17 casos positivos de G1 que el modelo no detectó en test (Data Scientist con un analista).
3. Repetir la auditoría con otro corte temporal o con más datos de G2 (Data Engineer).
4. Mantener activa la regla de seguridad (exposición ≥ 0.7 o infraestructura ≤ 0.3).

**Acción humana:** el analista decide y firma cada caso y puede cambiar el orden con una
justificación. La apelación sigue el mecanismo definido en LAB11. **Retiro:** se aplican las
condiciones de `student_inputs/lab11_impact.yml`.
