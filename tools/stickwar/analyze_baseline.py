#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASELINE = ROOT / "baseline" / "stick-war-2.swf"
WORK = ROOT / "work"
EXPORT = WORK / "export"
REPORT = WORK / "analysis.json"
MAPPING = ROOT / "mapping.json"

SIGNALS = {
    "battle_loop": [r"ENTER_FRAME", r"onEnterFrame", r"update\(", r"gameLoop", r"battle"],
    "unit_base": [r"health", r"maxHealth", r"attack", r"target", r"move"],
    "projectile_base": [r"projectile", r"velocity", r"damage", r"target"],
    "selection": [r"selected", r"selectUnit", r"mouse", r"selection"],
    "production": [r"queue", r"train", r"population", r"gold", r"mana"],
    "technology": [r"upgrade", r"technology", r"research", r"ability"],
    "save": [r"SharedObject", r"\.data\.", r"save", r"load"],
    "campaign": [r"level", r"campaign", r"mission", r"victory", r"stage"],
    "ai": [r"\bAI\b", r"computer", r"strategy", r"train", r"attack"],
    "hud": [r"gold", r"mana", r"population", r"TextField", r"health"],
}

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def ffdec_cmd() -> list[str]:
    raw=os.environ.get("FFDEC")
    if raw: return raw.split()
    for name in ("ffdec","ffdec.sh","ffdec.bat"):
        p=shutil.which(name)
        if p: return [p]
    raise SystemExit("FFDec not found. Set FFDEC to the FFDec CLI executable.")

def export_scripts():
    if EXPORT.exists() and any(EXPORT.rglob("*.as")):
        return
    EXPORT.mkdir(parents=True, exist_ok=True)
    cmd=ffdec_cmd()+["-export","script",str(EXPORT),str(BASELINE)]
    print("+"," ".join(cmd))
    subprocess.run(cmd, check=True)

def score_file(text: str, patterns: list[str]) -> int:
    score=0
    for p in patterns:
        n=len(re.findall(p,text,re.I))
        score += min(n,8)
    return score

def inventory():
    out={}
    all_files=[]
    for p in EXPORT.rglob("*.as"):
        try: text=p.read_text(encoding="utf-8-sig",errors="replace")
        except Exception: continue
        rel=str(p.relative_to(EXPORT))
        row={"path":rel,"bytes":len(text),"lines":text.count("\n")+1}
        all_files.append(row)
    for role,patterns in SIGNALS.items():
        scored=[]
        for row in all_files:
            p=EXPORT/row["path"]
            text=p.read_text(encoding="utf-8-sig",errors="replace")
            s=score_file(text,patterns)
            if s: scored.append({"path":row["path"],"score":s})
        out[role]=sorted(scored,key=lambda x:(-x["score"],x["path"]))[:20]
    return all_files,out

def main():
    if not BASELINE.exists():
        raise SystemExit(f"Missing baseline: {BASELINE}\nAdd a canonical Stick War 2 SWF; no game binary was present in the repository.")
    WORK.mkdir(parents=True,exist_ok=True)
    digest=sha256(BASELINE)
    print("baseline sha256:",digest)
    export_scripts()
    files,candidates=inventory()
    report={"baseline":{"path":str(BASELINE.relative_to(ROOT)),"sha256":digest,"bytes":BASELINE.stat().st_size},
            "source_files":len(files),"candidates":candidates}
    REPORT.write_text(json.dumps(report,indent=2)+"\n")
    if not MAPPING.exists():
        skeleton={"baseline_sha256":digest,"roles":{k:None for k in SIGNALS},
                  "notes":"Replace null roles with exact exported .as paths after reviewing work/analysis.json."}
        MAPPING.write_text(json.dumps(skeleton,indent=2)+"\n")
        print("created",MAPPING)
    print("wrote",REPORT)
    for role in SIGNALS:
        top=candidates[role][:3]
        print(f"{role:14}",", ".join(f"{x['path']} ({x['score']})" for x in top) or "no candidates")

if __name__=="__main__":
    main()
