import pandas as pd, pytest
from inf8239_u04.governance import deployment_decision,validate_raci
def test_failed_gate_requires_review():
    d=deployment_decision({"recall":.5},{"recall_gap":.1,"fpr_gap":.1},{"latency_ms":1,"model_kb":5},{"min_recall":.7,"max_recall_gap":.2,"max_fpr_gap":.2,"max_latency_ms":10,"max_model_kb":20}); assert d["status"]=="REVIEW"
GATES={"min_recall":.7,"min_group_recall":.7,"max_recall_gap":.2,"max_fpr_gap":.2,"max_latency_ms":10,"max_model_kb":20}
def test_gap_out_of_tolerance_requires_review():
    d=deployment_decision({"recall":.8},{"recall_gap":.3,"fpr_gap":.1},{"latency_ms":1,"model_kb":5},GATES); assert d["status"]=="REVIEW" and d["failed"]==["recall_gap"]
def test_low_group_recall_requires_review():
    d=deployment_decision({"recall":.8,"min_group_recall":.6},{"recall_gap":.1,"fpr_gap":.1},{"latency_ms":1,"model_kb":5},GATES); assert d["status"]=="REVIEW" and "group_recall" in d["failed"]
def test_privacy_failure_stops():
    d=deployment_decision({"recall":.8},{"recall_gap":.1,"fpr_gap":.1},{"latency_ms":1,"model_kb":5},GATES,privacy_ok=False); assert d["status"]=="STOP"
def test_raci_requires_single_accountable():
    with pytest.raises(ValueError): validate_raci(pd.DataFrame([{"activity":"deploy","R":"ML","A":"PO, DS","C":"DS","I":"Users"}]))
def test_raci_requires_accountable():
    with pytest.raises(ValueError): validate_raci(pd.DataFrame([{"activity":"deploy","R":"ML","A":"","C":"DS","I":"Users"}]))
def test_recommendation_is_traceable():
    from inf8239_u04.data import load_data
    from inf8239_u04.governance import load_config
    from inf8239_u04.pipeline import run,recommend_cases
    cfg=load_config(); r=run(load_data(),cfg["gates"],direct_identifiers=cfg["direct_identifiers"]); t=r["decision"]["trace"]
    assert t["model_version"].startswith("logistic-v") and t["policy"].startswith("configs/governance.yml@") and t["evidence"] and r["decision"]["human_action"]
    cases=recommend_cases(r["model"],r["test"]); assert cases.probability.between(0,1).all() and cases.priority.is_unique
