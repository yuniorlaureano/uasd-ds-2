# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 04 - LAB11 Evaluación de impacto ético.
### Propósito, actores, registro de riesgos y decisión GO/REVIEW/STOP.

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:*** GS66 Stealth 11UH
- ***Physical Memory (RAM):*** 32.0 GB
- ***Entorno:*** Windows 11, Python 3.12.10, pandas 2.3.3, scikit-learn 1.9.1, gestionado con `uv`. Todo corre en CPU.

## Resumen
Evalué el impacto del DSS territorial sintético **antes** de medir el modelo. Definí su propósito y sus límites, mapeé a los cuatro actores y documenté ocho riesgos, cada uno con su control, responsable y evidencia.

**Resultado principal:** la decisión es **REVISAR**. El caso de uso es legítimo y tiene una alternativa no predictiva, pero los riesgos de mayor impacto dependían de métricas que todavía no existían (se midieron en LAB12).

## Cómo ejecutar
```bash
uv run python scripts/lab11_impact.py
uv run pytest -q tests/test_impact.py tests/test_privacy.py
```

**Cambios al código base:**
- `scripts/lab11_impact.py` **no se podía ejecutar** (`SyntaxError`): tenía saltos de línea literales dentro de un string. Se cambiaron por `\n`.
- El script sobrescribía `DECISION_RECORD.md` en cada ejecución. Ahora solo crea la plantilla si el archivo no existe.

**Entregables:** [`student_inputs/lab11_impact.yml`](student_inputs/lab11_impact.yml), [`stakeholders.csv`](student_inputs/stakeholders.csv), [`risk_register.csv`](student_inputs/risk_register.csv), `reports/lab11/risk_register_scored.csv`, `reports/lab11/rmf_summary.json` y [`reports/lab11/DECISION_RECORD.md`](reports/lab11/DECISION_RECORD.md).

## Resultados

### Evaluación de impacto
| Campo | Definición |
|---|---|
| Decisión asistida | En qué orden un analista abre los casos pendientes. El analista decide y firma. |
| Alternativa no predictiva | FIFO + triaje: exposición ≥ 0.7 o infraestructura ≤ 0.3 primero. |
| Uso prohibido | Elegibilidad, emergencias, intervención automática, perfilado real. |
| Condición de retiro | Recall < 0.68, brecha > 0.16, uso fuera de alcance, identificador directo, o no superar a la línea base dos meses seguidos. |
| Apelación | Un segundo analista que no vio el puntaje revisa el caso en un máximo de 5 días hábiles. |

### Riesgos prioritarios (probabilidad × impacto)
| Riesgo | Prioridad | Responsable |
|---|---|---|
| R02 Sesgo de automatización | 9 | Product Owner |
| R01 Recall desigual entre grupos | 8 | Data Scientist |
| R07 Falsos negativos con alta exposición | 8 | Product Owner |

El orden numérico solo indica dónde mirar primero. R01 y R07 son más graves que R02 aunque tengan menos puntos, porque su daño es retrasar la revisión de quien la necesita. `rmf_summary.json` mostraba MEASURE como "LAB12 pending": había archivos, pero ningún control medido.

**Actualización después de LAB12:** R01 suponía menor recall en G2. La auditoría mostró lo contrario: el recall más bajo está en **G1** (0.653 frente a 0.791). El registro de riesgos se actualizó.
