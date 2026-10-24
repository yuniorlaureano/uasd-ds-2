# Declaración de uso de inteligencia artificial

## Herramientas utilizadas
- Claude Code (Anthropic, modelo Claude Opus 5.5), usado como asistente en la terminal.

## Propósito de cada uso
- Ejecutar los comandos de `instrucciones.md`: entrenamiento, pruebas, exportación de requisitos y arranque de la app.
- Ampliar `scripts/train_ae_vae.py` con un panel de 16 ejemplos sorteados con semilla, curvas de entrenamiento y validación, métricas de prueba, vecinos más cercanos y diversidad.
- Crear `src/inf8239_u03_gen/evaluation.py` y `tests/test_evaluation.py`.
- Redactar un primer borrador de `docs/MODEL_CARD.md` y `LAB10.md` a partir de las métricas y figuras generadas, siguiendo la organización del proyecto de Recomendadores.

## Prompts o decisiones relevantes
- Prompt: "En este proyecto necesito correr las instrucciones en instrucciones.md, ayúdame ahí" y la aprobación posterior para completar lo que faltaba.
- Decisiones: usar como validación el último 10 % de entrenamiento (la misma partición que `validation_split`); medir distancias como RMS por píxel; comparar las muestras con imágenes reales de prueba como referencia.

## Elementos verificados por el equipo
<!-- Completar: qué revisó el equipo personalmente (código, figuras, cifras del Model Card). -->

## Cambios realizados sobre resultados generados
<!-- Completar: qué se modificó del código o del texto propuesto por la herramienta. -->

## Responsabilidad asumida
<!-- Completar: declaración del equipo sobre su responsabilidad por el contenido entregado. -->
