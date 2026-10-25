# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 04 - LAB13 Gobernanza y DSS responsable con Streamlit.
### RACI, puertas de calidad, recomendación trazable, simulacro de incidente y tablero.

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:*** GS66 Stealth 11UH
- ***Physical Memory (RAM):*** 32.0 GB
- ***Entorno:*** Windows 11, Python 3.12.10, pandas 2.3.3, scikit-learn 1.9.1, fairlearn 0.12.0, streamlit 1.64.0, gestionado con `uv`. Todo corre en CPU.

## Resumen
Integré LAB11 y LAB12 en un DSS gobernado. El pipeline carga los datos, valida el contrato, entrena, audita y aplica las puertas de calidad, y emite una recomendación trazable. El tablero de Streamlit muestra el propósito, los límites, las métricas, los grupos, las puertas, la cola recomendada y la acción humana.

**Resultado principal:** el pipeline original daba **GO**, porque solo revisaba el recall global y las brechas, mientras que LAB12 ya había mostrado que G1 queda bajo el mínimo. Agregué la puerta `min_group_recall` y ahora la decisión es **REVIEW** (`group_recall` fallida). La falla no se oculta: el sistema opera con la regla no predictiva hasta que el Product Owner decida.

## Cómo ejecutar
```bash
uv run python scripts/lab13_governance.py   # decisión gobernada → reports/lab13/
uv run python scripts/simulate_incident.py  # simulacro de incidente
uv run streamlit run app.py                 # tablero
uv run pytest -q                            # 15 pruebas
uv export --format requirements-txt --no-dev -o requirements.txt
```

**Cambios al código base:**
- **Nueva puerta `min_group_recall: 0.68`** (`configs/governance.yml`, `governance.deployment_decision`): sin ella, el promedio ocultaba la falla de G1.
- **Puerta de privacidad y estado STOP:** si aparece un identificador directo, la decisión es STOP. Una falla de desempeño o equidad da REVIEW. Cada estado tiene una acción humana concreta.
- **Trazabilidad:** la decisión incluye `trace` con la versión del modelo (hash del `.joblib`), la política (hash de `governance.yml`), el corte temporal y las rutas de evidencia.
- **Capa DSS por caso:** `pipeline.recommend_cases` da probabilidad, prioridad, si aplica la regla de seguridad y la acción recomendada. Se exporta a `reports/lab13/case_recommendations.csv` y se muestra en el tablero.
- **RACI:** `validate_raci` exige ahora exactamente un Accountable. Se agregaron cuatro actividades (auditoría de equidad, monitoreo, revisión y apelación, retiro).
- `scripts/simulate_incident.py` **no se podía ejecutar** (`SyntaxError`, el mismo error que el script de LAB11). Ahora inyecta una brecha fuera de tolerancia, comprueba que la puerta la bloquee, guarda `incident_simulation.json` y no sobrescribe el postmortem.
- El tablero usa `width="stretch"`, porque `use_container_width` está obsoleto en streamlit 1.64.
- 5 pruebas nuevas en `tests/test_governance.py`: brecha que da REVIEW, recall por grupo, privacidad que da STOP, un solo Accountable y trazabilidad.

## Resultados

### Arquitectura
| Capa | Responsabilidad | Evidencia |
|---|---|---|
| Data | Contrato, procedencia, exclusiones y corte temporal | [DATASET_CARD.md](docs/DATASET_CARD.md), `validate_schema`, `tests/test_data.py` y `tests/test_privacy.py` |
| Model | Logística suficiente y reproducible (`random_state=42`) | [MODEL_CARD.md](docs/MODEL_CARD.md), `trace.model_version = logistic-v0.1.0-74db9fc35677` |
| Fairness | Métricas por grupo e interseccionales con soporte mínimo | [AUDIT_REPORT.md](reports/lab12/AUDIT_REPORT.md) |
| Green AI | Calidad, tiempo y tamaño de las alternativas | Tabla de [LAB12.md](LAB12.md): 3.6 KB, ~0.04 s, ~0.03 ms/caso |
| DSS | Probabilidad, prioridad, política y acción | `reports/lab13/case_recommendations.csv` y tablero |
| Governance | Puertas, responsables, monitoreo, apelación e incidente | [raci.csv](student_inputs/raci.csv), [RUNBOOK.md](docs/RUNBOOK.md), [INCIDENT_POSTMORTEM.md](reports/lab13/INCIDENT_POSTMORTEM.md) |

### Decisión gobernada (`reports/lab13/deployment_decision.json`)
| Puerta | Valor | Umbral | Cumple |
|---|---|---|---|
| recall | 0.717 | ≥ 0.68 | ✅ |
| group_recall | 0.653 (G1) | ≥ 0.68 | ❌ |
| recall_gap | 0.138 | ≤ 0.16 | ✅ |
| fpr_gap | 0.125 | ≤ 0.16 | ✅ |
| latency | ~0.03 ms | ≤ 500 ms | ✅ |
| model_size | 3.6 KB | ≤ 1024 KB | ✅ |
| privacy | sin identificadores directos | — | ✅ |

**Estado: REVIEW.** Acción humana: no desplegar, operar con la regla no predictiva, investigar la puerta fallida y documentar la decisión del responsable. La regla de seguridad tampoco basta: recupera 1 de los 17 falsos negativos de G1, y el recall de G1 queda en 0.673.

### Simulacro de incidente
Se inyectó una brecha de recall de 0.26. El estado pasó a REVIEW, con `recall_gap` y `group_recall` como puertas fallidas. El [postmortem](reports/lab13/INCIDENT_POSTMORTEM.md) registra la detección, la contención, la preservación de evidencia, la comunicación, el rollback y cinco acciones con responsable y fecha.

### Pruebas post instalación
| Prueba | Resultado |
|---|---|
| Inicio | `streamlit run app.py` levanta sin errores (probado en modo headless en el puerto 8599, health `ok`, HTTP 200). `AppTest` corre sin excepciones y muestra el aviso de caso sintético. |
| Contrato | Una columna prohibida (`email`, `name`) o faltante lanza `ValueError` en `validate_schema`, antes de entrenar o predecir. |
| Puerta | Una brecha fuera de tolerancia da REVIEW (simulacro y `test_gap_out_of_tolerance_requires_review`). Un fallo de privacidad da STOP. |
| Trazabilidad | La recomendación incluye versión, política, evidencia y acción humana (`test_recommendation_is_traceable`). |

`uv run pytest -q` da **15 passed**.

### Publicación (opcional)
`requirements.txt` está generado con `uv export`. El repositorio no contiene datos personales (dataset sintético, contrato que rechaza identificadores) ni secretos. **No se desplegó** en Streamlit Community Cloud. Para hacerlo, se apunta la app a `app.py` en el repositorio público.
