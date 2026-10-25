import time
import sklearn
from sklearn.metrics import accuracy_score, recall_score
from . import __version__
from .data import features, temporal_split
from .fairness import audit, gap
from .governance import deployment_decision, file_sha256
from .model import build_model, fit_measure

def run(df, gates, kind="logistic", direct_identifiers=(), config_path="configs/governance.yml"):
    train,test=temporal_split(df); model=build_model(kind); model_path=f"models/{kind}.joblib"; resources=fit_measure(model,features(train),train.target,model_path)
    start=time.perf_counter(); pred=model.predict(features(test)); resources["latency_ms"]=(time.perf_counter()-start)*1000/len(test)
    overall,by_group,_=audit(test.target,pred,test.protected_group)
    metrics={"accuracy":float(accuracy_score(test.target,pred)),"recall":float(recall_score(test.target,pred,zero_division=0)),"min_group_recall":float(by_group["recall"].min())}
    gaps={"recall_gap":gap(by_group,"recall"),"fpr_gap":gap(by_group,"fpr")}
    privacy_ok=not ({str(c).lower() for c in df.columns} & set(direct_identifiers))
    decision=deployment_decision(metrics,gaps,resources,gates,privacy_ok)
    decision["trace"]={"model_version":f"{kind}-v{__version__}-{file_sha256(model_path)}","sklearn":sklearn.__version__,"policy":f"{config_path}@{file_sha256(config_path)}",
                       "train_end":str(train.received_date.max().date()),"test_start":str(test.received_date.min().date()),"test_rows":len(test),
                       "evidence":["reports/lab11/DECISION_RECORD.md","reports/lab12/AUDIT_REPORT.md","reports/lab13/deployment_decision.json","docs/MODEL_CARD.md"]}
    return {"model":model,"test":test,"pred":pred,"overall":overall,"by_group":by_group,"metrics":metrics,"gaps":gaps,"resources":resources,"decision":decision}

def recommend_cases(model, cases, safety_exposure=0.7, safety_infrastructure=0.3):
    out=cases[["case_id","received_date","zone","exposure","infrastructure_score"]].copy()
    out["probability"]=model.predict_proba(features(cases))[:,1].round(3)
    out["safety_rule"]=(cases.exposure>=safety_exposure)|(cases.infrastructure_score<=safety_infrastructure)
    out["recommended_action"]=out.apply(lambda r:"Revisar esta semana (regla de seguridad)" if r.safety_rule else "Revisar primero" if r.probability>=0.5 else "Revisar en orden de cola",axis=1)
    out=out.sort_values(["safety_rule","probability","received_date"],ascending=[False,False,True]); out.insert(0,"priority",range(1,len(out)+1))
    return out
