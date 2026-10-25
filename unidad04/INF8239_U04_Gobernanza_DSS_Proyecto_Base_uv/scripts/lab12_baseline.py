import json
from pathlib import Path
from inf8239_u04.data import load_data,temporal_split
from inf8239_u04.fairness import audit,intersectional
# Non-predictive alternative from LAB11: review first exposure>=0.7 or infrastructure<=0.3
out=Path("reports/lab12/baseline_rule"); out.mkdir(parents=True,exist_ok=True)
df=load_data(); _,test=temporal_split(df); pred=((test.exposure>=0.7)|(test.infrastructure_score<=0.3)).astype(int)
overall,groups,diff=audit(test.target,pred,test.protected_group); _,inter,_=audit(test.target,pred,intersectional(test))
groups.to_csv(out/"fairness_by_group.csv"); inter.to_csv(out/"fairness_intersectional.csv")
(out/"global_metrics.json").write_text(json.dumps({"metrics":{k:float(v) for k,v in overall.items()},"differences":{k:float(v) for k,v in diff.items()},"resources":{"training_seconds":0.0,"model_kb":0.0}},indent=2),encoding="utf-8")
print(groups.round(3))
