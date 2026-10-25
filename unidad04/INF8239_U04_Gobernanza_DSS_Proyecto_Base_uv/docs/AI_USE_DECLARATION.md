# Declaración de uso de IA

## LAB11 — Evaluación de impacto ético

- **Herramienta:** Claude Code (modelo Claude Opus 5.5, Anthropic).
- **Finalidad:** redactar una primera versión de la evaluación de impacto, el mapa de actores, el registro de riesgos y el registro de decisión, y corregir un error de sintaxis en el script.
- **Fragmentos afectados:** `student_inputs/lab11_impact.yml`, `student_inputs/stakeholders.csv`, `student_inputs/risk_register.csv`, `reports/lab11/DECISION_RECORD.md` y `scripts/lab11_impact.py`. Se respetaron los valores de probabilidad, impacto, riesgo residual y poder que venían en la plantilla.
- **Verificaciones:** se ejecutaron `uv run python scripts/lab11_impact.py` y `uv run pytest -q tests/test_impact.py tests/test_privacy.py` (3 pruebas superadas). Se revisó la tasa base por grupo en el dataset (G1 50%, G2 64%) para fundamentar R01. Los umbrales citados coinciden con `configs/governance.yml`.
- **Errores detectados y correcciones:** `scripts/lab11_impact.py` tenía saltos de línea literales dentro de un string, lo que impedía ejecutarlo. Se reemplazaron por `\n`. Además, el script ahora solo crea la plantilla de `DECISION_RECORD.md` si el archivo no existe, para no borrar el registro al volver a ejecutarlo.
- **Revisión humana pendiente:** el estudiante debe revisar y ajustar los escenarios, controles y la decisión REVISAR. Es su responsabilidad validarlos antes de entregar.
