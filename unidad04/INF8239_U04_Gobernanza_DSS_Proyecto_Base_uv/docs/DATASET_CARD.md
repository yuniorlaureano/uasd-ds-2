# Dataset Card

Synthetic territorial-risk dataset generated with a fixed educational seed. It contains no real persons, locations, rates or official Dominican Republic statistics. Intended only to practice contracts, temporal evaluation, subgroup auditing and governance. Prohibited: operational profiling or inference about real populations.

## Contrato y procedencia
- **Archivo:** `data/territorial_risk_synthetic.csv`. Sintético, entregado con el proyecto base del curso.
- **Tamaño:** 640 filas y 9 columnas; `case_id` es único. Fechas de recepción desde 2026-01-01.
- **Columnas requeridas:** `case_id`, `received_date`, `zone`, `protected_group`, `age_band`, `previous_incidents`, `infrastructure_score`, `exposure` y `target` (binario 0/1).
- **Columnas prohibidas:** `name`, `document_number`, `email` y `phone`. `validate_schema` rechaza el dataset **antes de entrenar o predecir** si falta una columna requerida, si aparece una prohibida o si `target` no es binario. Lo cubren `tests/test_data.py` y `tests/test_privacy.py`.

## Composición
| | Valor |
|---|---|
| Positivos (`target = 1`) | 55.2% |
| G1 / G2 | 396 / 244 (tasa positiva 50% / 64%) |
| Zonas | Este 164, Sur 164, Oeste 157, Norte 155 |
| Tramos de edad | 18-29, 30-44, 45-59, 60+ |

## Exclusiones y corte temporal
- El modelo no usa `case_id` (identificador), `received_date` (solo para el corte), `protected_group` (atributo sensible, que se reserva para la auditoría) ni `target`.
- Quitar `protected_group` **no elimina los proxies**: G2 tiene menor `infrastructure_score` (0.44 frente a 0.57) y mayor `exposure` (0.56 frente a 0.47). Por eso igual se audita por grupo.
- `previous_incidents` puede reflejar cuánto reporta una zona y no su riesgo real (riesgo R06).
- Partición temporal: 75% más antiguo para entrenamiento (hasta 2026-09-24) y 25% más reciente para prueba (desde 2026-09-25). Así se evalúa como en producción, sin usar el futuro.
