# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 04 - Gobernanza y DSS responsable.

Proyecto base acumulativo para LAB11–13. Se completan archivos pequeños en `student_inputs/`, se ejecutan los scripts y el esfuerzo se concentra en interpretar y justificar decisiones. Los datos son sintéticos y didácticos. El sistema no autoriza decisiones automáticas sobre personas.

| Laboratorio | Tema | Documento |
|---|---|---|
| LAB11 | Evaluación de impacto ético, actores y registro de riesgos | [LAB11.md](LAB11.md) |
| LAB12 | Auditoría de equidad con Fairlearn, baseline y Green AI | [LAB12.md](LAB12.md) |
| LAB13 | Gobernanza, puertas de calidad, incidente y tablero Streamlit | [LAB13.md](LAB13.md) |

**Decisión actual del sistema: REVIEW.** El recall global cumple (0.717), pero el recall de G1 (0.653) está bajo el mínimo de 0.68. Ver [reports/lab13/deployment_decision.json](reports/lab13/deployment_decision.json).

- Dataset card: [docs/DATASET_CARD.md](docs/DATASET_CARD.md)
- Model card: [docs/MODEL_CARD.md](docs/MODEL_CARD.md)
- Runbook de incidentes: [docs/RUNBOOK.md](docs/RUNBOOK.md)
- Declaración de uso de IA: [docs/AI_USE_DECLARATION.md](docs/AI_USE_DECLARATION.md)

## Inicio
```bash
uv sync --frozen
uv run pytest -q
uv run python scripts/check_environment.py
```

## Ruta
```bash
uv run python scripts/lab11_impact.py
uv run python scripts/lab12_audit.py --model logistic
uv run python scripts/lab12_audit.py --model tree
uv run python scripts/lab12_baseline.py
uv run python scripts/lab13_governance.py
uv run python scripts/simulate_incident.py
uv run streamlit run app.py
```
