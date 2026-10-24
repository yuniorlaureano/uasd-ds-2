# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 03 - Sistemas recomendadores con MovieLens.

Proyecto base del autor académico Edwin Ramón José Nolasco. El dataset de muestra de `tests/` prueba el código; la evidencia final usa MovieLens.

| Laboratorio | Tema | Documento |
|---|---|---|
| LAB08 | Popularidad ponderada y recomendación por contenido | [LAB08.md](LAB08.md) |
| LAB09 | Factorización matricial, híbrido, perfiles y costo | [LAB09.md](LAB09.md) |

- Dataset card: [docs/DATASET_CARD.md](docs/DATASET_CARD.md)
- System card: [docs/SYSTEM_CARD.md](docs/SYSTEM_CARD.md)

## Inicio
```bash
uv python install 3.12
uv sync
uv run pytest -q
uv run python scripts/download_data.py
uv run python scripts/audit_data.py
```
