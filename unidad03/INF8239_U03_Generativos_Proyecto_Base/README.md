# INF-8239-C2
## Manual laboratorios guiados.
## Unidad 03 - Modelos generativos con Fashion-MNIST.

Proyecto base del autor académico Edwin Ramón José Nolasco. Autoencoder y VAE reproducibles; la app solo hace inferencia con el decodificador entrenado.

| Laboratorio | Tema | Documento |
|---|---|---|
| LAB10 | Autoencoder y VAE: reconstrucción, latente, muestras y vecinos cercanos | [LAB10.md](LAB10.md) |

- Model card: [docs/MODEL_CARD.md](docs/MODEL_CARD.md)
- Declaración de uso de IA: [docs/AI_USE_DECLARATION.md](docs/AI_USE_DECLARATION.md)

## Inicio (CPU)
```bash
uv python install 3.12
uv sync --extra cpu
uv run python scripts/check_runtime.py
uv run python scripts/train_ae_vae.py --epochs-ae 6 --epochs-vae 8
uv run pytest -q
```

## GPU
Solo para WSL2/Linux con NVIDIA correctamente configurada:
```bash
uv sync --extra gpu
```

## Aplicación
```bash
uv run streamlit run app/streamlit_app.py
```

No afirme privacidad por el solo hecho de generar datos sintéticos.
