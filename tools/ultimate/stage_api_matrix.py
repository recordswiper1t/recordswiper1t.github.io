#!/usr/bin/env python3
"""Build a KR1 stage -> Frontiers Level compatibility matrix.

The available publisher Flash source contains Level1..Level19. Rather than
invent a separate superclass bridge per stage, this tool determines whether one
namespaced `KR1__Level extends Level` adapter can satisfy the inherited API
surface for all source-ready KR1 stages.

Only member names/signatures are emitted; method bodies are never copied.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from level_api_diff import members, inherited_refs, serial_member_list, read, class_info  # noqa: E402


def locate(root: Path, name: str) -> Path:
    direct = root / name
    if direct.is_file():
        return direct
    hits = list(root.rglob(name))
    if len(hits) != 1:
        raise SystemExit(f"expected exactly one {name} under {root}, got {len(hits)}")
    return hits[0]


def stage_contract(stage_text: str, kr1_members: dict, krf_members: dict) -> dict:
    stage_members = members(stage_text)
    refs = inherited_refs(stage_text)
    kr1_names = set(kr1_members)
    krf_names = set(krf_members)
    own = set(stage_members)
    inherited_this = set(refs["this_refs_not_declared_locally"]) & kr1_names
    inherited_super = set(refs["super_refs"]) & kr1_names
    inherited_unqualified = set(refs["unqualified_calls_not_declared_locally"]) & kr1_names
    direct = inherited_this | inherited_super | inherited_unqualified
    framework_or_ancestor = sorted(
        (set(refs["this_refs_not_declared_locally"]) | set(refs["super_refs"])) - kr1_names
    )
    missing = sorted(x for x in direct if x not in krf_names and x not in own)
    shared = sorted(x for x in direct if x in krf_names)
    return {
        "class": class_info(stage_text),
        "declared_member_count": len(own),
        "direct_kr1_level_refs": sorted(direct),
        "framework_or_ancestor_refs_not_in_kr1_level": framework_or_ancestor,
        "shared_frontiers_refs": shared,
        "missing_frontiers_refs": missing,
        "confirmed_inherited_unqualified_calls": sorted(inherited_unqualified),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kr1-scripts", type=Path, required=True)
    ap.add_argument("--krf-scripts", type=Path, required=True)
    ap.add_argument("--first", type=int, default=1)
    ap.add_argument("--last", type=int, default=19)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--union-contract", type=Path, help="contract consumable by build_level_adapter.py")
    args = ap.parse_args()

    kr1_root = args.kr1_scripts
    krf_root = args.krf_scripts
    kr1_level_text = read(locate(kr1_root, "Level.as"))
    krf_level_text = read(locate(krf_root, "Level.as"))
    kr1m = members(kr1_level_text)
    krfm = members(krf_level_text)

    stages = {}
    frequency = Counter()
    framework_frequency = Counter()
    missing_levels = []
    for n in range(args.first, args.last + 1):
        name = f"Level{n}.as"
        try:
            path = locate(kr1_root, name)
        except SystemExit:
            missing_levels.append(n)
            continue
        contract = stage_contract(read(path), kr1m, krfm)
        stages[f"Level{n}"] = contract
        frequency.update(contract["missing_frontiers_refs"])
        framework_frequency.update(contract["framework_or_ancestor_refs_not_in_kr1_level"])

    union_missing = sorted(frequency)
    union_candidates = {
        name: {
            "kr1_signatures": serial_member_list(kr1m.get(name, [])),
            "krf_same_name_signatures": serial_member_list(krfm.get(name, [])),
            "referenced_by_stage_count": frequency[name],
            "referenced_by_stages": [
                stage for stage, row in stages.items()
                if name in row["missing_frontiers_refs"]
            ],
        }
        for name in union_missing
    }

    payload = {
        "range": [args.first, args.last],
        "source_stage_count": len(stages),
        "missing_stage_numbers": missing_levels,
        "kr1_level_member_count": len(kr1m),
        "krf_level_member_count": len(krfm),
        "shared_level_member_count": len(set(kr1m) & set(krfm)),
        "union_missing_frontiers_ref_count": len(union_missing),
        "union_missing_frontiers_refs": union_missing,
        "missing_ref_frequency": dict(sorted(frequency.items(), key=lambda kv: (-kv[1], kv[0]))),
        "framework_or_ancestor_ref_frequency": dict(sorted(framework_frequency.items(), key=lambda kv: (-kv[1], kv[0]))),
        "stages": stages,
        "adapter_candidates": union_candidates,
        "policy": {
            "single_kr1_level_adapter_target": True,
            "frontiers_level_is_authoritative": True,
            "framework_inherited_members_are_not_adapter_stubs": True,
            "source_bodies_not_emitted": True,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.union_contract:
        union_contract = {
            "stage": {"class": f"Level{args.first}-Level{args.last}", "declared_member_count": None},
            "stage_refs_missing_on_krf": union_missing,
            "adapter_candidates": union_candidates,
            "source_stage_count": len(stages),
            "generated_from": "stage_api_matrix",
        }
        args.union_contract.parent.mkdir(parents=True, exist_ok=True)
        args.union_contract.write_text(json.dumps(union_contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "source_stage_count": len(stages),
        "missing_stage_numbers": missing_levels,
        "union_missing_frontiers_ref_count": len(union_missing),
        "most_common_missing_refs": frequency.most_common(20),
        "most_common_framework_or_ancestor_refs": framework_frequency.most_common(20),
    }, indent=2))

    if missing_levels:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
