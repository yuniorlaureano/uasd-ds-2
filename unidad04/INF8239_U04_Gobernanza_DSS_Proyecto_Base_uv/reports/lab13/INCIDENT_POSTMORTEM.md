# Incident simulation — Postmortem

**Tipo:** simulacro (`uv run python scripts/simulate_incident.py`) · **Severidad:** S2 (REVIEW) · **Modelo:** `logistic-v0.1.0-74db9fc35677`

- **detected_at:** 2026-10-25T17:14:10Z (ver `reports/lab13/incident_simulation.json`).
- **signal:** se inyectó una brecha de recall de 0.26 (umbral 0.16). El pipeline marcó `recall_gap` como fallida y además confirmó la falla real ya existente en `group_recall` (G1 = 0.653 < 0.68). El estado pasó a **REVIEW**: la puerta no se ocultó.
- **containment:** el ML Engineer pasó la cola a la regla no predictiva FIFO + triaje. El modelo quedó sin desplegar, a la espera de la decisión del Product Owner. Los analistas siguen decidiendo cada caso.
- **evidence:** se preservaron `incident_simulation.json`, `deployment_decision.json`, `fairness_by_group.csv`, `case_recommendations.csv`, el hash del modelo (`74db9fc35677`) y el hash de la política (`configs/governance.yml@7f38401ccc05` en `trace.policy`).
- **communication:**
  - **Interna (en 24 h):** el Product Owner informa a operadores e Institutional Owner que el modelo no se despliega, que la cola usa la regla de triaje y que deben reportar los casos de G1 que les parezcan mal priorizados.
  - **Personas afectadas (en 5 días hábiles):** aviso a sus representantes de que se revisa una posible diferencia de detección entre grupos y de que pueden pedir la revisión de su caso.
- **causa (de la falla real `group_recall`):** el umbral de decisión único (0.5) detecta peor los positivos de G1, sobre todo en los tramos de 30 a 59 años. La regla de seguridad solo recupera 1 de los 17 falsos negativos de G1. Las causas posibles (azar de muestreo, distinta tasa base, proxies) siguen abiertas: no está probada una discriminación causal.
- **lección:** antes de LAB13, el pipeline daba **GO** porque solo miraba el recall global. Se agregó la puerta `min_group_recall: 0.68` para que el promedio no oculte una falla localizada.

## Corrective actions, owners and dates
| # | Acción | Responsable | Fecha |
|---|---|---|---|
| 1 | Revisar manualmente los 17 falsos negativos de G1 y documentar el patrón | Data Scientist + Operator | 2026-11-06 |
| 2 | Evaluar umbral por costo de error y calibración; aceptar solo si recall G1 ≥ 0.68 y brecha FPR ≤ 0.16 | Data Scientist | 2026-11-13 |
| 3 | Repetir la auditoría con un segundo corte temporal o más datos de G2 por tramo de edad | Data Engineer | 2026-11-20 |
| 4 | Implementar justificación obligatoria y muestreo semanal a ciegas en la herramienta de revisión (R02) | ML Engineer | 2026-11-20 |
| 5 | Aprobar o rechazar el nuevo despliegue con la evidencia de 1–3 | Product Owner (A) / Institutional Owner | 2026-11-25 |
