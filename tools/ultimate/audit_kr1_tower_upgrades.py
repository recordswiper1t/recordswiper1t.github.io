#!/usr/bin/env python3
"""Extract KR1 tier-4 upgrade action/state contracts from FFDec sources.

The report is deliberately structural: it records action strings, fields touched
inside each `upgradeTower` case, declared fields, and nearby level/rank-like
identifiers. It does not guess ability semantics. The output is used to build
`qolBlueprintActions()` methods only after each action->rank field relationship
is evidenced by the source.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TOWERS={
    "TowerArcherRanger":"kr1-rangers-hideout",
    "TowerArcherMusketeer":"kr1-musketeer-garrison",
    "TowerSoldierPaladin":"kr1-holy-order",
    "TowerSoldierBarbarian":"kr1-barbarian-mead-hall",
    "TowerMageArcane":"kr1-arcane-wizard",
    "TowerMageSorcerer":"kr1-sorcerer-mage",
    "TowerEngineerTesla":"kr1-tesla-x104",
    "TowerEngineerBfg":"kr1-big-bertha",
}
ACTION_RE=re.compile(r'"(special_[^"\\]+)"')
THIS_RE=re.compile(r'this\.([^\s;,.()\[\]+\-*/=!<>?:]+|§[^§]+§)')
RANK_WORD_RE=re.compile(r'(level|rank|current|special|upgrade|price|cost)',re.I)


def extract_function(text:str,name:str)->str:
    marker=f"function {name}"
    start=text.find(marker)
    if start<0: return ""
    brace=text.find("{",start)
    if brace<0: return ""
    depth=0; ins=False; esc=False; q=""; i=brace
    while i<len(text):
        c=text[i]
        if ins:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c==q: ins=False
        else:
            if c in ('"',"'"): ins=True; q=c
            elif c=="{": depth+=1
            elif c=="}":
                depth-=1
                if depth==0: return text[start:i+1]
        i+=1
    return text[start:]


def declarations(text:str)->list[dict]:
    rows=[]
    for line_no,line in enumerate(text.splitlines(),1):
        if " var " not in f" {line} " and not line.lstrip().startswith(("private var ","public var ","protected var ")):
            continue
        m=re.search(r'\bvar\s+(.+?)\s*:\s*([^=;]+)',line)
        if not m: continue
        name=m.group(1).strip(); typ=m.group(2).strip()
        rows.append({"line":line_no,"name":name,"type":typ,"rank_like":bool(RANK_WORD_RE.search(name))})
    return rows


def case_blocks(fn:str)->dict[str,str]:
    matches=list(re.finditer(r'case\s+"(special_[^"\\]+)"\s*:',fn))
    out={}
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(fn)
        default=fn.find("default:",m.end(),end)
        if default>=0: end=default
        out[m.group(1)]=fn[m.start():end]
    return out


def audit_one(path:Path)->dict:
    text=path.read_text(encoding="utf-8-sig",errors="replace")
    fn=extract_function(text,"upgradeTower")
    actions=sorted(set(ACTION_RE.findall(fn or text)))
    blocks=case_blocks(fn)
    cases=[]
    for action in actions:
        block=blocks.get(action,"")
        refs=[]
        for ref in THIS_RE.findall(block):
            if ref not in refs: refs.append(ref)
        assignments=[]
        for line in block.splitlines():
            stripped=line.strip()
            if any(op in stripped for op in ("=","++","--","+=","-=")) and "case " not in stripped:
                assignments.append(stripped)
        cases.append({
            "action":action,
            "this_fields_referenced":refs,
            "rank_like_field_refs":[r for r in refs if RANK_WORD_RE.search(r)],
            "assignment_lines":assignments[:40],
        })
    decl=declarations(text)
    return {
        "source_file":str(path),
        "actions":actions,
        "action_count":len(actions),
        "cases":cases,
        "declared_fields":decl,
        "rank_like_declared_fields":[x for x in decl if x["rank_like"]],
        "has_upgradeTower":bool(fn),
        "qol_blueprint_present":"qolBlueprintActions" in text,
    }


def main()->None:
    p=argparse.ArgumentParser()
    p.add_argument("scripts",type=Path)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    out={"towers":{},"summary":{}}
    total_actions=0
    for cls,stable_id in TOWERS.items():
        path=a.scripts/(cls+".as")
        if not path.is_file(): raise SystemExit(f"missing KR1 tower source: {path}")
        row=audit_one(path); row["stable_id"]=stable_id; out["towers"][cls]=row
        total_actions+=row["action_count"]
    out["summary"]={
        "tower_count":len(TOWERS),
        "total_special_actions":total_actions,
        "all_have_upgradeTower":all(x["has_upgradeTower"] for x in out["towers"].values()),
        "already_have_qol_blueprints":sum(x["qol_blueprint_present"] for x in out["towers"].values()),
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out["summary"],indent=2))
    for cls,row in out["towers"].items(): print(cls,":",", ".join(row["actions"]))

if __name__=="__main__": main()
