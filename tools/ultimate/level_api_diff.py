#!/usr/bin/env python3
"""Compare KR1 and KRF Level APIs and emit an adapter-oriented report.

This intentionally records signatures/names only, not method bodies. It is used
for converting the already-existing namespaced KR1__Level class into a thin
compatibility shim over the enhanced Frontiers Level runtime.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

IDENT = r"[A-Za-z_$§][A-Za-z0-9_$§]*"
VIS = r"(?:public|protected|private|internal)?"
STATIC = r"(?:static\s+)?"
VAR_RE = re.compile(rf"^\s*({VIS})\s*{STATIC}(var|const)\s+({IDENT})\s*(?::\s*([^=;]+))?", re.M)
FUNC_RE = re.compile(rf"^\s*({VIS})\s*(?:override\s+)?{STATIC}function\s+({IDENT})\s*\(([^)]*)\)\s*(?::\s*([^\s{{]+))?", re.M)
THIS_RE = re.compile(rf"\bthis\.({IDENT})\b")
SUPER_RE = re.compile(rf"\bsuper\.({IDENT})\b")
CALL_RE = re.compile(rf"(?<![.\w$§])({IDENT})\s*\(")
DECL_CLASS_RE = re.compile(rf"\bclass\s+({IDENT})(?:\s+extends\s+({IDENT}))?")

KEYWORDS = {
    "if","for","while","switch","catch","function","return","new","super",
    "int","uint","Number","String","Boolean","Array","Object","Math","trace",
}

@dataclass(frozen=True)
class Member:
    name: str
    kind: str
    visibility: str
    type: str | None
    args: str | None = None


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def members(text: str) -> dict[str, list[Member]]:
    out: dict[str, list[Member]] = {}
    for m in VAR_RE.finditer(text):
        item = Member(m.group(3), m.group(2), (m.group(1) or "internal").strip(), (m.group(4) or "").strip() or None)
        out.setdefault(item.name, []).append(item)
    for m in FUNC_RE.finditer(text):
        item = Member(m.group(2), "function", (m.group(1) or "internal").strip(), (m.group(4) or "").strip() or None, m.group(3).strip())
        out.setdefault(item.name, []).append(item)
    return out


def class_info(text: str) -> dict:
    m = DECL_CLASS_RE.search(text)
    return {"class": m.group(1) if m else None, "extends": m.group(2) if m else None}


def inherited_refs(level_text: str) -> dict[str, list[str]]:
    own = set(members(level_text))
    this_refs = set(THIS_RE.findall(level_text)) - own
    super_refs = set(SUPER_RE.findall(level_text))
    calls = set(CALL_RE.findall(level_text)) - own - KEYWORDS
    return {
        "this_refs_not_declared_locally": sorted(this_refs),
        "super_refs": sorted(super_refs),
        "unqualified_calls_not_declared_locally": sorted(calls),
    }


def serial_member_list(rows: list[Member]) -> list[dict]:
    return [asdict(x) for x in rows]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kr1-level", type=Path, required=True)
    ap.add_argument("--krf-level", type=Path, required=True)
    ap.add_argument("--kr1-stage", type=Path, required=True, help="Usually KR1 Level1.as / Southport")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--skeleton", type=Path)
    args = ap.parse_args()

    k1 = read(args.kr1_level)
    kf = read(args.krf_level)
    stage = read(args.kr1_stage)
    k1m = members(k1)
    kfm = members(kf)
    stm = members(stage)
    refs = inherited_refs(stage)

    k1_names = set(k1m)
    kf_names = set(kfm)
    stage_own = set(stm)

    # A stage can also call inherited Flash framework methods such as
    # addEventListener. Those are not KR1-Level compatibility requirements.
    # Only treat a reference as part of the KR1 Level contract when KR1 Level
    # itself actually declares that member.
    inherited_this = set(refs["this_refs_not_declared_locally"]) & k1_names
    inherited_super = set(refs["super_refs"]) & k1_names
    inherited_unqualified = set(refs["unqualified_calls_not_declared_locally"]) & k1_names
    direct_stage_refs = inherited_this | inherited_super | inherited_unqualified
    framework_or_ancestor_refs = sorted(
        (set(refs["this_refs_not_declared_locally"]) | set(refs["super_refs"])) - k1_names
    )
    missing_for_stage = sorted(x for x in direct_stage_refs if x not in kf_names and x not in stage_own)
    already_shared_for_stage = sorted(x for x in direct_stage_refs if x in kf_names)

    report = {
        "kr1": {**class_info(k1), "member_count": len(k1_names)},
        "krf": {**class_info(kf), "member_count": len(kf_names)},
        "stage": {**class_info(stage), "declared_member_count": len(stage_own)},
        "same_name_member_count": len(k1_names & kf_names),
        "kr1_level_members_absent_from_krf_count": len(k1_names - kf_names),
        "krf_level_members_absent_from_kr1_count": len(kf_names - k1_names),
        "stage_inherited_references": refs,
        "stage_framework_or_ancestor_refs_not_in_kr1_level": framework_or_ancestor_refs,
        "stage_inherited_unqualified_calls_confirmed_on_kr1_level": sorted(inherited_unqualified),
        "stage_refs_already_available_on_krf": already_shared_for_stage,
        "stage_refs_missing_on_krf": missing_for_stage,
        "adapter_candidates": {
            name: {
                "kr1_signatures": serial_member_list(k1m.get(name, [])),
                "krf_same_name_signatures": serial_member_list(kfm.get(name, [])),
            }
            for name in missing_for_stage
        },
        "same_name_signatures": {
            name: {
                "kr1": serial_member_list(k1m[name]),
                "krf": serial_member_list(kfm[name]),
            }
            for name in sorted(k1_names & kf_names)
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.skeleton:
        lines = [
            "// Generated adapter skeleton: signatures only, no source method bodies.",
            "// Intended strategy: replace existing namespaced KR1__Level after binary merge.",
            "package",
            "{",
            "   public class KR1__Level extends Level",
            "   {",
            "      public function KR1__Level()",
            "      {",
            "         super();",
            "      }",
            "",
        ]
        for name in missing_for_stage:
            sigs = k1m.get(name, [])
            for s in sigs:
                if s.kind == "function":
                    ret = f" : {s.type}" if s.type else ""
                    lines.append(f"      // TODO adapt KR1 {s.visibility} function {name}({s.args or ''}){ret}")
                else:
                    lines.append(f"      // TODO adapt KR1 {s.visibility} {s.kind} {name}:{s.type or '*'}")
        lines += ["   }", "}", ""]
        args.skeleton.parent.mkdir(parents=True, exist_ok=True)
        args.skeleton.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "kr1_level_members": len(k1_names),
        "krf_level_members": len(kf_names),
        "stage_direct_kr1_level_refs": len(direct_stage_refs),
        "stage_framework_or_ancestor_refs": framework_or_ancestor_refs,
        "stage_refs_already_on_krf": len(already_shared_for_stage),
        "stage_refs_missing_on_krf": len(missing_for_stage),
        "missing_names": missing_for_stage,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
