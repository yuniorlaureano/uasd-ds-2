# Model Card — Territorial Review DSS (sintético)

**Versión:** `logistic-v0.1.0-74db9fc35677` · **Política:** `configs/governance.yml` · **Estado:** REVIEW (no desplegado)

## Intended use
Ordenar la cola semanal de casos territoriales **sintéticos** para que un analista técnico revise primero los de mayor probabilidad de riesgo. El modelo da una probabilidad y una prioridad; el analista decide y firma cada caso. Una regla de seguridad (exposición ≥ 0.7 o infraestructura ≤ 0.3) obliga a revisar el caso en la semana sin importar el puntaje.

## Out-of-scope use
Prohibido: intervención automática, decisión de elegibilidad para ayudas o servicios, declaración de emergencias, perfilado de personas o grupos reales e inferencia sobre poblaciones reales de la República Dominicana. El modelo no debe usarse sin revisión humana.

## Data and split
- Dataset sintético `data/territorial_risk_synthetic.csv`: 640 casos, 55.2% positivos. Ver [DATASET_CARD.md](DATASET_CARD.md).
- Variables del modelo: `zone`, `age_band`, `previous_incidents`, `infrastructure_score`, `exposure`. Excluidas: `case_id`, `received_date`, `protected_group` y `target`.
- Partición temporal 75/25: entrenamiento hasta 2026-09-24 (480 casos), prueba desde 2026-09-25 (160 casos).
- Modelo: `OneHotEncoder` + `StandardScaler` + `LogisticRegression(class_weight="balanced", max_iter=1200, random_state=42)`.

## Global and subgroup evaluation
| Métrica (test, n = 160) | Logística | Árbol (depth 5) | Regla no predictiva | Umbral |
|---|---|---|---|---|
| Recall | **0.717** | 0.717 | 0.359 | ≥ 0.68 |
| Recall mínimo por grupo | **0.653 (G1)** ❌ | 0.633 (G1) | 0.327 (G1) | ≥ 0.68 |
| FPR | 0.279 | 0.309 | 0.103 | — |
| Brecha de recall | 0.138 | 0.181 ❌ | 0.069 | ≤ 0.16 |
| Brecha de FPR | 0.125 | 0.168 ❌ | 0.053 | ≤ 0.16 |

| Grupo | n | Positivos | Recall | FPR | Tasa de selección |
|---|---|---|---|---|---|
| G1 | 101 | 49 | 0.653 | 0.250 | 0.446 |
| G2 | 59 | 43 | 0.791 | 0.375 | 0.678 |

- El intervalo bootstrap 95% de la brecha de recall es [0.01, 0.31]. El FPR de G2 se calcula con solo 16 negativos.
- En el análisis interseccional, el recall bajo de G1 se concentra en los tramos de 30-44 años (0.563) y 45-59 años (0.588). Cuatro subgrupos no tienen el soporte mínimo (n ≥ 20 y 10 o más positivos). Detalle en `reports/lab12/AUDIT_REPORT.md`.
- La regla de seguridad recupera solo 1 de los 17 falsos negativos de G1, y con ella el recall de G1 sube a 0.673: **sigue bajo el umbral**.

## Green AI evidence
| Modelo | Entrenamiento | Tamaño | Latencia por caso |
|---|---|---|---|
| **Logística** | ~0.04 s (CPU) | 3.6 KB | ~0.03 ms |
| Árbol | ~0.05 s | 7.9 KB | — |

El árbol duplica el tamaño sin mejorar el recall y empeora las brechas. La logística es la opción suficiente: 0.3% del límite de tamaño (1024 KB), latencia muy por debajo de 500 ms y coeficientes interpretables. Equipo: Intel i7-11800H, 32 GB RAM, sin GPU.

## Limitations, human oversight and appeal
- **Limitaciones:** datos sintéticos, un solo corte temporal, muestra de prueba pequeña y proxies del grupo (G2 tiene menor infraestructura y mayor exposición). Una brecha observada indica algo que investigar, no una prueba de discriminación causal.
- **Supervisión humana:** el analista ve la probabilidad, la prioridad y la regla aplicada. Puede cambiar el orden si deja una justificación. Cada semana un segundo analista revisa a ciegas el 10% de los casos de baja prioridad.
- **Apelación:** formulario con número de caso. Lo revisa un segundo analista sin ver el puntaje, en un máximo de 5 días hábiles.
- **Retiro:** ante cualquier condición de `student_inputs/lab11_impact.yml`, se vuelve a la regla no predictiva y se sigue [RUNBOOK.md](RUNBOOK.md).

## Owner and review date
- **Accountable:** Product Owner · **Responsible:** Data Scientist (validación) y ML Engineer (despliegue y monitoreo) · **Escalamiento:** Institutional Owner.
- **Fecha de esta versión:** 2026-10-25 · **Próxima revisión:** 2026-11-25, o antes si cambian los datos o falla una puerta.
