import pandas as pd
import streamlit as st
from inf8239_u04.data import load_data
from inf8239_u04.governance import load_config
from inf8239_u04.pipeline import run,recommend_cases
st.set_page_config(page_title="Governed Green DSS",layout="wide")
st.title("DSS territorial sintético · Gobernanza y Green AI")
st.warning("Demostración educativa con datos sintéticos. No autoriza decisiones automáticas ni representa estadísticas reales.")
cfg=load_config(); result=run(load_data(),cfg["gates"],direct_identifiers=cfg["direct_identifiers"]); decision=result["decision"]
st.subheader("Propósito y autoridad"); st.write(cfg["purpose"]); st.write("Usos prohibidos:",", ".join(cfg["prohibited_uses"]))
c1,c2,c3,c4=st.columns(4); c1.metric("Accuracy",f"{result['metrics']['accuracy']:.3f}"); c2.metric("Recall",f"{result['metrics']['recall']:.3f}"); c3.metric("Recall mínimo por grupo",f"{result['metrics']['min_group_recall']:.3f}"); c4.metric("Decisión",decision["status"])
if decision["failed"]: st.error(f"Puertas fallidas: {', '.join(decision['failed'])}. {decision['human_action']}.")
else: st.success(decision["human_action"])
st.subheader("Métricas por grupo"); st.dataframe(result["by_group"],width="stretch")
st.caption("Solo se interpretan subgrupos con n ≥ 20 y al menos 10 positivos (recall) o 10 negativos (FPR).")
st.subheader("Puertas de calidad")
st.dataframe(pd.DataFrame({"puerta":list(decision["checks"]),"cumple":list(decision["checks"].values())}),hide_index=True,width="stretch")
st.subheader("Green AI"); g1,g2,g3=st.columns(3); g1.metric("Entrenamiento",f"{result['resources']['training_seconds']:.3f} s"); g2.metric("Tamaño",f"{result['resources']['model_kb']:.1f} KB"); g3.metric("Latencia por caso",f"{result['resources']['latency_ms']:.3f} ms")
st.subheader("Cola recomendada (casos de prueba)")
st.dataframe(recommend_cases(result["model"],result["test"]),hide_index=True,width="stretch")
st.subheader("Trazabilidad"); st.json(decision["trace"])
st.info("Acción humana: el analista decide y firma cada caso, puede cambiar el orden con justificación y cualquier persona afectada puede apelar. Ante una puerta fallida se opera con la regla no predictiva y se activa el runbook.")
