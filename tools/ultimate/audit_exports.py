#!/usr/bin/env python3
"""Inventory two FFDec ActionScript exports before merging them.

The useful output is not just a file count: it identifies class-name collisions,
level/tower/hero/enemy candidates and produces a deterministic namespace plan
for KR1 classes that collide with the Frontiers runtime.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

from content_manifest import summary, validate


CLASS_RE = re.compile(r"\b(?:public\s+|internal\s+|final\s+|dynamic\s+)*class\s+([^\s{]+)(?:\s+extends\s+([^\s{]+))?")


def clean_name(name: str | None) -> str | None:
    if not name:
        return None
    return name.strip().rstrip("{")


def classify(name: str, base: str | None, path: Path) -> set[str]:
    low = name.lower()
    base_low = (base or "").lower()
    file_low = path.name.lower()
    kinds: set[str] = set()
    if re.fullmatch(r"level\d+", low) or low.startswith("level") or base_low.startswith("level"):
        kinds.add("level")
    if "tower" in low or "tower" in base_low:
        kinds.add("tower")
    if "hero" in low or "hero" in base_low:
        kinds.add("hero")
    if "enemy" in low or "enemy" in base_low:
        kinds.add("enemy")
    if "wave" in low or "wave" in base_low:
        kinds.add("wave")
    if "map" in low or "campaign" in low or "map" in file_low:
        kinds.add("map_or_campaign")
    return kinds


def inventory(root: Path) -> dict:
    if not root.is_dir():
        raise SystemExit(f"ActionScript export directory not found: {root}")
    classes: dict[str, dict] = {}
    parse_failures: list[str] = []
    for path in sorted(root.rglob("*.as")):
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            parse_failures.append(str(path))
            continue
        matches = list(CLASS_RE.finditer(text))
        if not matches:
            continue
        for m in matches:
            name = clean_name(m.group(1))
            base = clean_name(m.group(2))
            if not name:
                continue
            entry = classes.setdefault(name, {
                "name": name,
                "base": base,
                "files": [],
                "kinds": set(),
            })
            entry["files"].append(str(path.relative_to(root)))
            entry["kinds"].update(classify(name, base, path))
    serial = {}
    for name, entry in classes.items():
        serial[name] = {
            **entry,
            "kinds": sorted(entry["kinds"]),
        }
    counts = Counter(kind for entry in serial.values() for kind in entry["kinds"])
    return {
        "root": str(root),
        "as_files": len(list(root.rglob("*.as"))),
        "class_count": len(serial),
        "kind_counts": dict(sorted(counts.items())),
        "classes": serial,
        "parse_failures": parse_failures,
    }


def namespace_plan(kr1: dict, krf: dict) -> dict[str, str]:
    collisions = sorted(set(kr1["classes"]) & set(krf["classes"]))
    plan = {}
    used = set(kr1["classes"]) | set(krf["classes"])
    for name in collisions:
        candidate = "KR1_" + name
        suffix = 2
        while candidate in used:
            candidate = f"KR1_{name}_{suffix}"
            suffix += 1
        plan[name] = candidate
        used.add(candidate)
    return plan


def compact_inventory(inv: dict) -> dict:
    groups = {}
    for kind in ("level", "tower", "hero", "enemy", "wave", "map_or_campaign"):
        groups[kind] = sorted(
            name for name, entry in inv["classes"].items() if kind in entry["kinds"]
        )
    return {
        "root": inv["root"],
        "as_files": inv["as_files"],
        "class_count": inv["class_count"],
        "kind_counts": inv["kind_counts"],
        "groups": groups,
        "parse_failures": inv["parse_failures"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kr1", required=True, help="FFDec exported scripts directory for Kingdom Rush")
    parser.add_argument("--krf", required=True, help="FFDec exported scripts directory for Frontiers V11/V12")
    parser.add_argument("--output", default="ultimate-inventory.json")
    args = parser.parse_args()

    validate()
    kr1 = inventory(Path(args.kr1))
    krf = inventory(Path(args.krf))
    collisions = sorted(set(kr1["classes"]) & set(krf["classes"]))
    plan = namespace_plan(kr1, krf)

    report = {
        "content_scope": summary(),
        "kr1": compact_inventory(kr1),
        "krf": compact_inventory(krf),
        "collision_count": len(collisions),
        "collisions": collisions,
        "kr1_namespace_plan": plan,
        "notes": [
            "Frontiers remains the runtime/base; namespace KR1 collisions instead of replacing KRF core classes.",
            "A class inventory cannot prove that timeline/sprite assets exist; binary symbol import is audited separately.",
            "Later Frontiers post-campaign/endless maps need a non-Flash source export or reconstruction.",
        ],
    }
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    print(f"wrote {args.output}")
    print(f"KR1 classes: {kr1['class_count']} | KRF classes: {krf['class_count']} | collisions: {len(collisions)}")


if __name__ == "__main__":
    main()
