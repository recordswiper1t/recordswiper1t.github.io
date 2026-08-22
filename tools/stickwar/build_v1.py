#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
BASELINE=ROOT/"baseline"/"stick-war-2.swf"
MAPPING=ROOT/"mapping.json"
CAMPAIGN=ROOT/"data"/"campaign.json"
TECH=ROOT/"data"/"tech.json"
PERF=ROOT/"data"/"performance.json"
WORK=ROOT/"work"
REQUIRED_ROLES=("battle_loop","unit_base","projectile_base","selection","production","technology","save","campaign","ai","hud")

def digest(path:Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def load(path): return json.loads(path.read_text(encoding="utf-8"))

def validate_data():
    c=load(CAMPAIGN); t=load(TECH); p=load(PERF)
    count=sum(len(ch["stages"]) for ch in c["chapters"])
    assert count==c["stage_count"] and count>=60, "campaign must remain a large contiguous expansion"
    assert len(t["factions"]["order"])==9 and len(t["factions"]["chaos"])==9
    for faction in ("order","chaos"):
        for name,nodes in t["factions"][faction]:
            assert name and len(nodes)==6
    assert p["acceptance"]["simulation_rule"]=="No reduced combat tick rate at any tier."
    return c,t,p,count

def require_mapping():
    if not MAPPING.exists():
        raise SystemExit("mapping.json missing. Run analyze_baseline.py first.")
    m=load(MAPPING)
    missing=[r for r in REQUIRED_ROLES if not m.get("roles",{}).get(r)]
    if missing:
        raise SystemExit("Baseline is analyzed but not mapped. Fill exact exported ActionScript paths in mapping.json for: "+", ".join(missing))
    if digest(BASELINE)!=m.get("baseline_sha256"):
        raise SystemExit("Baseline hash changed since mapping; re-run analysis instead of patching the wrong SWF.")
    return m

def main():
    campaign,tech,perf,count=validate_data()
    if not BASELINE.exists():
        raise SystemExit(
            "No Stick War 2 baseline is present. The expansion framework/data are complete, "
            "but a playable SWF cannot be fabricated without the source game binary."
        )
    mapping=require_mapping()
    WORK.mkdir(parents=True,exist_ok=True)
    plan={
      "baseline_sha256":digest(BASELINE),
      "stages":count,
      "order_units":len(tech["factions"]["order"]),
      "chaos_units":len(tech["factions"]["chaos"]),
      "tech_nodes":sum(len(nodes) for f in tech["factions"].values() for _,nodes in f),
      "mapped_roles":mapping["roles"],
      "performance_targets":perf["acceptance"],
      "status":"mapping-complete; low-level source patch layer required before release"
    }
    (WORK/"build-plan.json").write_text(json.dumps(plan,indent=2)+"\n",encoding="utf-8")
    raise SystemExit(
      "V1 content/mapping validation passed. Binary publication is deliberately blocked until "
      "the mapped low-level ActionScript patch layer (spatial hash, active vectors, pools, UI cadence, "
      "possession, save/campaign hooks) is implemented, FFDec-imported, and re-decompile verified."
    )

if __name__=="__main__":
    main()
