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
