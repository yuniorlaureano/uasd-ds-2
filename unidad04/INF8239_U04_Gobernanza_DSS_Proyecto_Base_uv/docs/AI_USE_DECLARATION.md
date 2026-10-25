# Declaración de uso de IA

## LAB11 — Evaluación de impacto ético

- **Herramienta:** Claude Code (modelo Claude Opus 5.5, Anthropic).
- **Finalidad:** redactar una primera versión de la evaluación de impacto, el mapa de actores, el registro de riesgos y el registro de decisión, y corregir un error de sintaxis en el script.
- **Fragmentos afectados:** `student_inputs/lab11_impact.yml`, `student_inputs/stakeholders.csv`, `student_inputs/risk_register.csv`, `reports/lab11/DECISION_RECORD.md` y `scripts/lab11_impact.py`. Se respetaron los valores de probabilidad, impacto, riesgo residual y poder que venían en la plantilla.
- **Verificaciones:** se ejecutaron `uv run python scripts/lab11_impact.py` y `uv run pytest -q tests/test_impact.py tests/test_privacy.py` (3 pruebas superadas). Se revisó la tasa base por grupo en el dataset (G1 50%, G2 64%) para fundamentar R01. Los umbrales citados coinciden con `configs/governance.yml`.
- **Errores detectados y correcciones:** `scripts/lab11_impact.py` tenía saltos de línea literales dentro de un string, lo que impedía ejecutarlo. Se reemplazaron por `\n`. Además, el script ahora solo crea la plantilla de `DECISION_RECORD.md` si el archivo no existe, para no borrar el registro al volver a ejecutarlo.
- **Revisión humana pendiente:** el estudiante debe revisar y ajustar los escenarios, controles y la decisión REVISAR. Es su responsabilidad validarlos antes de entregar.

## LAB12 — Auditoría de equidad

- **Herramienta:** Claude Code (modelo Claude Opus 5.5, Anthropic).
- **Finalidad:** ejecutar la auditoría de los dos modelos, agregar el baseline no predictivo (`scripts/lab12_baseline.py`), calcular intervalos bootstrap y conteos por subgrupo, y redactar `student_inputs/lab12_decision.yml` y `reports/lab12/AUDIT_REPORT.md`.
- **Verificaciones:** las cifras del informe salen de `reports/lab12/*/global_metrics.json` y de los CSV por grupo. Se ejecutaron `scripts/validate_lab12_decision.py` y `pytest -q tests/test_fairness.py tests/test_model.py`.
- **Errores detectados:** la hipótesis R01 de LAB11 (menor recall en G2) no se confirmó: el recall más bajo está en G1. Queda documentado en el informe.
- **Revisión humana pendiente:** el estudiante debe revisar el mínimo interseccional elegido (n ≥ 20 y 10 o más positivos o negativos) y la recomendación REVISAR.

## LAB13 — Gobernanza y DSS

- **Herramienta:** Claude Code (modelo Claude Opus 5.5, Anthropic).
- **Finalidad:** agregar las puertas `min_group_recall` y de privacidad (con estado STOP), la trazabilidad y la recomendación por caso; corregir `scripts/simulate_incident.py`; ampliar el tablero y la RACI; agregar 5 pruebas; redactar el Model Card, el Runbook, el Dataset Card, el postmortem, LAB11.md, LAB12.md, LAB13.md y el README.
- **Verificaciones:** se ejecutaron `lab13_governance.py` (REVIEW, `group_recall`), `simulate_incident.py` (REVIEW) y `uv run pytest -q` (15 pruebas superadas). Se levantó Streamlit en modo headless (health `ok`) y se revisó con `AppTest` que no hubiera excepciones. Las cifras de la documentación salen de los JSON y CSV en `reports/`.
- **Errores detectados:** el pipeline daba GO aunque G1 estuviera bajo el recall mínimo; se corrigió con una puerta nueva. `simulate_incident.py` tenía un `SyntaxError`. El riesgo R01 se actualizó con la evidencia de LAB12.
- **Revisión humana pendiente:** el estudiante debe revisar el Runbook (plazos y roles), las fechas del postmortem y decidir si publica en Streamlit Community Cloud.
