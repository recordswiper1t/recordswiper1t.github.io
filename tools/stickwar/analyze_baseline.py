#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_BASELINE = ROOT / "baseline" / "stick-war-2.swf"
WORK = ROOT / "work"
DEFAULT_EXPORT = WORK / "export"
DEFAULT_REPORT = WORK / "analysis.json"
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
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def ffdec_cmd() -> list[str]:
    raw=os.environ.get("FFDEC")
    if raw:
        return raw.split()
    for name in ("ffdec","ffdec.sh","ffdec.bat"):
        p=shutil.which(name)
        if p:
            return [p]
    raise SystemExit("FFDec not found. Set FFDEC to the FFDec CLI executable.")

def export_scripts(baseline: Path, export_root: Path):
    if export_root.exists() and any(export_root.rglob("*.as")):
        return
    if not baseline.exists():
        raise SystemExit(f"Missing baseline: {baseline}")
    export_root.mkdir(parents=True, exist_ok=True)
    cmd=ffdec_cmd()+["-export","script",str(export_root),str(baseline)]
    print("+"," ".join(cmd))
    subprocess.run(cmd, check=True)

def score_file(text: str, patterns: list[str]) -> int:
    score=0
    for p in patterns:
        n=len(re.findall(p,text,re.I))
        score += min(n,8)
    return score

def inventory(export_root: Path):
    out={}
    all_files=[]
    texts={}
    for p in export_root.rglob("*.as"):
        try:
            text=p.read_text(encoding="utf-8-sig",errors="replace")
        except Exception:
            continue
        rel=str(p.relative_to(export_root))
        texts[rel]=text
        all_files.append({"path":rel,"bytes":len(text),"lines":text.count("\n")+1})
    for role,patterns in SIGNALS.items():
        scored=[]
        for row in all_files:
            s=score_file(texts[row["path"]],patterns)
            if s:
                scored.append({"path":row["path"],"score":s})
        out[role]=sorted(scored,key=lambda x:(-x["score"],x["path"]))[:30]
    return all_files,out

def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    p.add_argument("--exported", type=Path, default=None,
                   help="Existing FFDec script-export root; skips export when supplied")
    p.add_argument("--out", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--write-mapping-skeleton", action="store_true")
    return p.parse_args()

def main():
    args=parse_args()
    baseline=args.baseline.resolve()
    export_root=(args.exported.resolve() if args.exported else DEFAULT_EXPORT.resolve())
    if not baseline.exists() and not args.exported:
        raise SystemExit(f"Missing baseline: {baseline}\nAdd a canonical Stick War 2 SWF or pass --exported with an existing FFDec export.")
    if args.exported:
        if not export_root.exists() or not any(export_root.rglob("*.as")):
            raise SystemExit(f"Exported source tree is empty: {export_root}")
    else:
        export_scripts(baseline, export_root)
    digest=sha256(baseline) if baseline.exists() else None
    if digest:
        print("baseline sha256:",digest)
    files,candidates=inventory(export_root)
    report={
        "baseline": None if not baseline.exists() else {
            "path":str(baseline),"sha256":digest,"bytes":baseline.stat().st_size
        },
        "export_root":str(export_root),
        "source_files":len(files),
        "candidates":candidates,
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+"\n")
    if args.write_mapping_skeleton:
        skeleton={"baseline_sha256":digest,"roles":{k:None for k in SIGNALS},
                  "notes":"Replace null roles with exact exported .as paths after reviewing analysis output."}
        MAPPING.write_text(json.dumps(skeleton,indent=2)+"\n")
        print("wrote",MAPPING)
    print("wrote",args.out)
    for role in SIGNALS:
        top=candidates[role][:5]
        print(f"{role:14}",", ".join(f"{x['path']} ({x['score']})" for x in top) or "no candidates")

if __name__=="__main__":
    main()
