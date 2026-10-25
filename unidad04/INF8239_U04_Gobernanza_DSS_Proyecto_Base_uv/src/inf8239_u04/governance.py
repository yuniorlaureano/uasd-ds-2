import hashlib
from pathlib import Path
import pandas as pd
import yaml

def load_config(path="configs/governance.yml"):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]

def validate_raci(df):
    required={"activity","R","A","C","I"}
    if required-set(df.columns): raise ValueError("RACI columns missing")
    if df[["R","A"]].fillna("").apply(lambda s:s.str.strip().eq("")).any().any(): raise ValueError("Every activity needs R and A")
    if df.A.str.contains(r",|;|/|\+| and | y ",regex=True).any(): raise ValueError("Every activity needs exactly one A")
    return True

def deployment_decision(metrics, gaps, resources, gates, privacy_ok=True):
    checks={
      "recall": metrics["recall"] >= gates["min_recall"],
      "group_recall": metrics.get("min_group_recall",1.0) >= gates.get("min_group_recall",0.0),
      "recall_gap": gaps["recall_gap"] <= gates["max_recall_gap"],
      "fpr_gap": gaps["fpr_gap"] <= gates["max_fpr_gap"],
      "latency": resources["latency_ms"] <= gates["max_latency_ms"],
      "model_size": resources["model_kb"] <= gates["max_model_kb"],
      "privacy": privacy_ok,
    }
    failed=[k for k,v in checks.items() if not v]
    status="STOP" if "privacy" in failed else "REVIEW" if failed else "GO"
    action={"GO":"Analyst reviews each case in model order; safety rule stays active; monthly audit",
            "REVIEW":"Do not deploy: operate with the non-predictive baseline, investigate failed gates and document the owner's decision",
            "STOP":"Withdraw the model, contain data exposure and activate the incident runbook"}[status]
    return {"status":status, "checks":checks, "failed":failed, "human_action":action}
