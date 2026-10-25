# Decision record — LAB11 Evaluación de impacto ético

**Sistema:** Territorial Review DSS - Synthetic (prioriza casos sintéticos para revisión humana)
**Responsable de la decisión:** Product Owner del DSS · escalamiento: Propietario Institucional
**Fecha:** 2026-10-25 · **Próxima revisión:** al cerrar la auditoría LAB12

## Decisión: REVISAR

No se recomienda desplegar el modelo todavía, pero tampoco detener el proyecto. El caso de uso
es legítimo y acotado (ordenar una cola para revisión humana), existe una alternativa no
predictiva y hay condiciones de retiro y apelación definidas. Sin embargo, los dos riesgos de
mayor impacto dependen de métricas que **aún no se han medido** (LAB12). Mientras tanto la cola
opera con la regla FIFO + triaje.

## Tres riesgos prioritarios

El orden de `risk_register_scored.csv` (probabilidad × impacto) se usó para dirigir la atención,
no como verdad. Revisando los escenarios, R01 y R07 son más graves que R02 aunque tengan menor
prioridad numérica, porque su daño es retrasar una revisión necesaria a quien la necesita.

| Riesgo | Prioridad | Interpretación | Evidencia hoy | Estado del control |
|---|---|---|---|---|
| **R02** Sesgo de automatización | 9 (3×3) | Es el más probable: si los analistas siguen el orden sin revisar, los demás errores del modelo pasan sin corregir. Por eso amplifica a R01 y R07. | Ninguna. El registro de justificaciones y el muestreo a ciegas aún no existen. | Diseñado, **no implementado** |
| **R01** Menor recall en G2 | 8 (2×4) | G2 tiene tasa base mayor (64% vs 50%). Un recall más bajo en G2 dejaría al grupo con más casos positivos al final de la cola: daño desigual. | Umbral `max_recall_gap: 0.16` en `configs/governance.yml`. La métrica por subgrupo está pendiente. | Umbral definido, **sin medir** |
| **R07** Falsos negativos con alta exposición | 8 (2×4) | Es el daño más directo: un caso urgente queda abajo en la cola. La regla de seguridad (exposición ≥ 0.7 o infraestructura ≤ 0.3 se revisa sí o sí) protege aunque el modelo falle. | Regla escrita en `student_inputs/lab11_impact.yml`. El recall global está pendiente. | Regla definida, **sin verificar en operación** |

Que un archivo de configuración tenga un umbral no prueba que el control funcione. Hoy la
evidencia de GOVERN y MAP es documental. MEASURE no tiene evidencia (`rmf_summary.json`:
"LAB12 pending"). MANAGE tiene retiro y apelación escritos, pero no probados.

## Incertidumbre

- No hay métricas del modelo: ni recall global, ni brechas por grupo o zona, ni comparación con la línea base.
- Los datos son sintéticos (640 casos, 244 en G2). Las métricas por subgrupo tendrán intervalos amplios.
- `previous_incidents` puede medir cuánto reporta una zona y no cuánto riesgo tiene (R06). No hay datos para separar ambas cosas.
- Las probabilidades e impactos (1–4) son juicios del equipo, no frecuencias observadas.

## Condiciones para pasar a CONTINUAR

1. LAB12 muestra recall global ≥ 0.68 y brechas de recall y FPR entre G1 y G2 ≤ 0.16 (responsable: Data Scientist).
2. El modelo supera a la regla FIFO + triaje en recall de casos positivos (responsable: Data Scientist).
3. Están implementados la justificación obligatoria por caso y el muestreo semanal a ciegas del 10% (responsable: Product Owner).
4. La regla de seguridad de R07 está activa en la aplicación y probada (responsable: ML Engineer).

## Condición de retiro (STOP)

Suspender el modelo y volver a FIFO + triaje si: el recall global baja de 0.68; una brecha de
recall o FPR entre grupos supera 0.16; se detecta un uso fuera de alcance (elegibilidad,
emergencias, intervención automática); aparece un identificador directo en los datos; o el
modelo no supera a la línea base en dos revisiones mensuales seguidas. Quien tiene autoridad
para retirarlo es el Propietario Institucional, a propuesta del Product Owner o de cualquier
miembro del equipo de datos.

## Revisión humana y apelación

Cada caso lo decide y firma un analista. Cualquier persona afectada u operador puede pedir que
un segundo analista, que no vio el puntaje, revise el caso en un máximo de 5 días hábiles. Cada
mes se analizan las apelaciones aceptadas como señal de error del modelo.
