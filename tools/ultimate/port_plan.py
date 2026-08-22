#!/usr/bin/env python3
"""Build a KR1 -> Frontiers class import policy from FFDec exports.

The plan deliberately keeps Frontiers engine/core classes authoritative. KR1
stage classes and their colliding stage graphics are renamed so they can coexist;
other colliding KR1 definitions are shadow-renamed but references continue to
resolve to the Frontiers runtime unless explicitly listed for reference rewrite.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from audit_exports import inventory


LEVEL_RE = re.compile(r"^Level(\d+)$")
GLEVEL_RE = re.compile(r"^GLevel(\d+)$")

# These are content-bearing collisions where KR1 references must follow the
# renamed KR1 symbol/class instead of binding to Frontiers' same-named content.
def rewrite_collision(name: str) -> bool:
    return bool(LEVEL_RE.fullmatch(name) or GLEVEL_RE.fullmatch(name))


def target_name(name: str, collides: bool) -> str:
    m = LEVEL_RE.fullmatch(name)
    if m:
        return f"KR1_Level{m.group(1)}"
    m = GLEVEL_RE.fullmatch(name)
    if m:
        return f"KR1_GLevel{m.group(1)}"
    if collides:
        return f"KR1_Shadow_{name}"
    return name


def build_plan(kr1_root: Path, krf_root: Path) -> dict:
    kr1 = inventory(kr1_root)
    krf = inventory(krf_root)
    kr1_classes = kr1["classes"]
    krf_names = set(krf["classes"])

    entries = []
    counts = {
        "keep_unique": 0,
        "rename_content_and_rewrite_refs": 0,
        "shadow_definition_keep_refs_on_krf": 0,
    }

    for name in sorted(kr1_classes):
        collides = name in krf_names
        target = target_name(name, collides)
        if not collides:
            policy = "keep_unique"
        elif rewrite_collision(name):
            policy = "rename_content_and_rewrite_refs"
        else:
            policy = "shadow_definition_keep_refs_on_krf"
        counts[policy] += 1
        entries.append({
            "source": name,
            "target": target,
            "policy": policy,
            "collides": collides,
            "base": kr1_classes[name].get("base"),
            "kinds": kr1_classes[name].get("kinds", []),
            "files": kr1_classes[name].get("files", []),
        })

    stages = [e for e in entries if LEVEL_RE.fullmatch(e["source"])]
    graphics = [e for e in entries if GLEVEL_RE.fullmatch(e["source"])]
    towers = [e for e in entries if "tower" in e["kinds"]]
    heroes = [e for e in entries if "hero" in e["kinds"]]
    enemies = [e for e in entries if "enemy" in e["kinds"]]

    return {
        "policy_version": 1,
        "runtime": "Frontiers V12/V11 authoritative",
        "rules": {
            "unique_kr1_class": "import unchanged",
            "LevelN/GLevelN_collision": "rename KR1 definition and rewrite KR1 references to KR1_*",
            "other_collision": "rename KR1 definition to KR1_Shadow_*; do not rewrite references, so imported KR1 content binds to Frontiers core",
        },
        "counts": counts,
        "kr1_class_count": len(entries),
        "krf_class_count": len(krf_names),
        "collision_count": sum(e["collides"] for e in entries),
        "stage_logic": stages,
        "stage_graphics": graphics,
        "tower_candidates": towers,
        "hero_candidates": heroes,
        "enemy_candidates": enemies,
        "classes": entries,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--kr1", required=True)
    p.add_argument("--krf", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    plan = build_plan(Path(args.kr1), Path(args.krf))
    Path(args.output).write_text(json.dumps(plan, indent=2), encoding="utf-8", newline="\n")
    print("wrote", args.output)
    print(json.dumps(plan["counts"], indent=2))
    print("stage logic classes:", len(plan["stage_logic"]))
    print("stage graphic classes:", len(plan["stage_graphics"]))


if __name__ == "__main__":
    main()
