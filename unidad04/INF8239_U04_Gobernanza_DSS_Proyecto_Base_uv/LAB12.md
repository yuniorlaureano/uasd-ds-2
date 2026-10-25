# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 04 - LAB12 Auditoría de equidad con Fairlearn.
### Métricas globales, por grupo e interseccionales; dos modelos, baseline y Green AI.

### Equipo utilizado

- ***Procesador:*** 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz, 8 Core(s), 16 Logical Processor(s)
- ***Modelo:*** GS66 Stealth 11UH
- ***Physical Memory (RAM):*** 32.0 GB
- ***Entorno:*** Windows 11, Python 3.12.10, pandas 2.3.3, scikit-learn 1.9.1, fairlearn 0.12.0, gestionado con `uv`. Todo corre en CPU.

## Resumen
Audité una regresión logística y un árbol de decisión con `MetricFrame` de Fairlearn, sobre un corte temporal (160 casos de prueba). Los comparé con la regla no predictiva de LAB11.

**Resultado principal:** la logística cumple el recall global (0.717) y las brechas (0.138 y 0.125), pero **el promedio oculta una falla en un grupo**: el recall de G1 es 0.653, bajo el mínimo de 0.68. El árbol no mejora la utilidad y se sale de tolerancia. Decisión: **REVISAR**, con la logística como candidata.

## Cómo ejecutar
```bash
uv run python scripts/describe_dataset.py
uv run python scripts/lab12_audit.py --model logistic
uv run python scripts/lab12_audit.py --model tree
uv run python scripts/lab12_baseline.py
uv run python scripts/validate_lab12_decision.py
uv run pytest -q tests/test_fairness.py tests/test_model.py
```

**Cambios al código base:**
- Nuevo `scripts/lab12_baseline.py`: mide la regla no predictiva con el mismo formato de reporte que los modelos.

**Entregables:** `reports/lab12/{logistic,tree,baseline_rule}/` (`global_metrics.json`, `fairness_by_group.csv`, `fairness_intersectional.csv`), [`student_inputs/lab12_decision.yml`](student_inputs/lab12_decision.yml) e informe completo en [`reports/lab12/AUDIT_REPORT.md`](reports/lab12/AUDIT_REPORT.md).

## Resultados

| Modelo | Recall | Recall G1 | Recall G2 | Brecha recall | Brecha FPR | Tamaño |
|---|---|---|---|---|---|---|
| **Logística** | 0.717 | **0.653** | 0.791 | 0.138 | 0.125 | 3.6 KB |
| Árbol | 0.717 | 0.633 | 0.814 | 0.181 ❌ | 0.168 ❌ | 7.9 KB |
| Regla no predictiva | 0.359 | 0.327 | 0.395 | 0.069 | 0.053 | — |

- **Soporte:** el FPR de G2 se calcula con solo 16 negativos. El intervalo bootstrap 95% de la brecha de recall es [0.01, 0.31]. Solo interpreto subgrupos con n ≥ 20 y al menos 10 positivos o negativos; 4 de 8 no lo cumplen.
- **Compromiso:** la regla tiene brechas menores solo porque detecta pocos casos (recall 0.36). Eso no es una victoria.
- **Green AI:** el árbol pesa 2.2 veces más y no mejora nada. La logística es suficiente.
- **Causalidad:** una brecha observada obliga a investigar (azar de muestreo, tasa base 73% frente a 49%, proxies, un solo corte), pero no prueba discriminación.
