import json
from datetime import datetime,timezone
from pathlib import Path
from inf8239_u04.data import load_data
from inf8239_u04.governance import load_config,deployment_decision
from inf8239_u04.pipeline import run
# Drill: inject a recall gap above tolerance and check that the gate blocks deployment
cfg=load_config(); result=run(load_data(),cfg["gates"],direct_identifiers=cfg["direct_identifiers"])
injected={**result["gaps"],"recall_gap":cfg["gates"]["max_recall_gap"]+0.10}
decision=deployment_decision(result["metrics"],injected,result["resources"],cfg["gates"])
out=Path("reports/lab13"); out.mkdir(parents=True,exist_ok=True)
(out/"incident_simulation.json").write_text(json.dumps({"detected_at":datetime.now(timezone.utc).isoformat(),"signal":"recall gap exceeded","observed_gaps":result["gaps"],"injected_gaps":injected,"decision":decision,"model_version":result["decision"]["trace"]["model_version"]},indent=2),encoding="utf-8")
path=out/"INCIDENT_POSTMORTEM.md"
if not path.exists(): path.write_text("# Incident simulation\n\n- detected_at: see incident_simulation.json\n- signal: recall gap exceeded\n- containment: REVIEW and safe baseline\n- evidence: preserved report and model version\n- communication: REPLACE\n- corrective actions, owners and dates: REPLACE\n",encoding="utf-8")
print(decision["status"],decision["failed"]); print(path)
