# Incident Runbook — Territorial Review DSS

Aplica a cualquier puerta fallida en `reports/lab13/deployment_decision.json`, apelación aceptada con patrón de error, uso fuera de alcance o exposición de datos. Roles según `student_inputs/raci.csv`.

1. **Detection and classification:** las señales son una puerta fallida en el pipeline (recall, recall por grupo, brechas, latencia, tamaño o privacidad), una caída en el monitoreo mensual, varias apelaciones aceptadas de un mismo grupo o zona, o el reporte de un operador. El ML Engineer abre el incidente en menos de 24 h y lo clasifica:
   - **S1 (STOP):** identificador directo en los datos, uso prohibido o exposición de datos.
   - **S2 (REVIEW):** una puerta de equidad o desempeño fuera de tolerancia.
   - **S3:** latencia, tamaño o disponibilidad.
2. **Containment authority:** el ML Engineer puede pasar el sistema a modo seguro de inmediato, sin pedir aprobación. El Product Owner confirma REVIEW en S2 y S3. Solo el Institutional Owner declara STOP y aprueba un nuevo despliegue. Mientras dure el incidente, la cola opera con la regla no predictiva y el analista sigue decidiendo cada caso.
3. **Evidence preservation:** se copian a `reports/incidents/<fecha>/` los archivos `deployment_decision.json` e `incident_simulation.json`, el `models/<modelo>.joblib` (con su hash en `trace.model_version`), el hash de la política (`trace.policy`), el CSV de recomendaciones y las apelaciones relacionadas. No se borra ni se reentrena nada antes de copiar.
4. **Internal and affected-party communication:**
   - En 24 h: el Product Owner avisa a operadores e Institutional Owner (qué falló, qué está en modo seguro, qué deben hacer).
   - En 5 días hábiles: aviso en lenguaje claro a los representantes de las personas afectadas. Se ofrece revisar sus casos, y en S1 interviene Legal.
   - No se publican datos de casos individuales.
5. **Rollback or safe baseline:** se vuelve a la regla FIFO + triaje (`scripts/lab12_baseline.py`), o a la última versión con decisión GO cuyo hash esté registrado. Se verifica que la cola se genere y que las pruebas pasen (`uv run pytest -q`).
6. **Postmortem, owner and due date:** el Data Scientist escribe el postmortem en un máximo de 10 días hábiles (causa, impacto por grupo, controles que fallaron, acciones). Cada acción tiene un responsable y una fecha. El Product Owner la aprueba y el registro de riesgos se actualiza. Ejemplo: `reports/lab13/INCIDENT_POSTMORTEM.md`.
