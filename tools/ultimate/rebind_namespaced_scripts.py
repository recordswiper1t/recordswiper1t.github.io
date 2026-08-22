#!/usr/bin/env python3
"""Rebind fully-namespaced KR1 content classes to the Frontiers shared core.

The binary XML merge first prefixes *every* KR1 class (for example
`KR1__Level1`, `KR1__EnemyGoblin`, `KR1__Level`). That is deliberately safe but
would otherwise carry a second KR1 engine beside Frontiers.

This pass is applied to an FFDec re-export of that merged SWF. It updates only
KR1 content definitions, replacing references to namespaced *shared/colliding*
core classes with the authoritative Frontiers class names. Shadow KR1 core
classes remain present but are not rewritten/imported, so they become dormant.

A small number of shared names can be excluded from rebinding when an explicit
compatibility shim intentionally keeps that namespaced identity alive. The first
use is `KR1__Level`: KR1 stages keep extending it while the class itself is
replaced with a thin adapter over Frontiers `Level`.

Because all target content classes already exist in the merged SWF, FFDec's
`-importScript` can replace them even though its CLI cannot add brand-new AS3
classes to a SWF.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil


CLASS_RE = re.compile(r"\bclass\s+([^\s{]+)")
IDENT_CHARS = r"A-Za-z0-9_$§"


def load_plan(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("classes")
    if not isinstance(rows, list):
        raise SystemExit(f"invalid port plan: {path}")
    out = {}
    for row in rows:
        if isinstance(row, dict) and row.get("source"):
            out[str(row["source"])] = row
    if not out:
        raise SystemExit(f"empty port plan: {path}")
    return out


def normalize_exclusions(values: list[str], prefix: str) -> set[str]:
    out: set[str] = set()
    for value in values:
        value = value.strip()
        if not value:
            continue
        out.add(value if value.startswith(prefix) else prefix + value)
    return out


def build_rebinder(plan: dict[str, dict], prefix: str, exclusions: set[str]) -> tuple[re.Pattern[str], dict[str, str]]:
    mapping: dict[str, str] = {}
    for source, row in plan.items():
        namespaced = prefix + source
        if namespaced in exclusions:
            continue
        if row.get("policy") == "shadow_definition_keep_refs_on_krf":
            mapping[namespaced] = source
    if not mapping:
        raise SystemExit("port plan contains no shared-core shadow definitions after exclusions")
    alternatives = "|".join(re.escape(x) for x in sorted(mapping, key=len, reverse=True))
    pattern = re.compile(rf"(?<![{IDENT_CHARS}])({alternatives})(?![{IDENT_CHARS}])")
    return pattern, mapping


def declared_class(text: str) -> str | None:
    m = CLASS_RE.search(text)
    return m.group(1).strip().rstrip("{") if m else None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scripts", required=True, help="FFDec scripts dir exported from fully namespaced merged SWF")
    p.add_argument("--plan", required=True, help="kr1-port-plan.json from original KR1/KRF exports")
    p.add_argument("--output", required=True, help="output import root; patched files are written beneath scripts/")
    p.add_argument("--report", required=True)
    p.add_argument("--prefix", default="KR1__")
    p.add_argument(
        "--exclude-rebind",
        action="append",
        default=[],
        help="shared namespaced identity to keep (repeatable), e.g. KR1__Level or Level",
    )
    args = p.parse_args()

    root = Path(args.scripts)
    if not root.is_dir():
        raise SystemExit(f"scripts dir missing: {root}")
    plan = load_plan(Path(args.plan))
    exclusions = normalize_exclusions(args.exclude_rebind, args.prefix)
    pattern, mapping = build_rebinder(plan, args.prefix, exclusions)

    out_root = Path(args.output)
    if out_root.exists():
        shutil.rmtree(out_root)
    out_scripts = out_root / "scripts"
    out_scripts.mkdir(parents=True)

    stats: Counter = Counter()
    changed_classes: list[str] = []
    skipped_shadow_classes: list[str] = []
    unresolved_plan_classes: list[str] = []

    def repl(match: re.Match[str]) -> str:
        stats["reference_tokens_rebound"] += 1
        return mapping[match.group(1)]

    for path in sorted(root.rglob("*.as")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        cls = declared_class(text)
        if not cls or not cls.startswith(args.prefix):
            stats["non_kr1_files_skipped"] += 1
            continue
        source = cls[len(args.prefix):]
        row = plan.get(source)
        if row is None:
            unresolved_plan_classes.append(cls)
            stats["kr1_classes_not_in_plan"] += 1
            continue
        if row.get("policy") == "shadow_definition_keep_refs_on_krf":
            skipped_shadow_classes.append(cls)
            stats["shadow_definitions_skipped"] += 1
            continue

        patched, count = pattern.subn(repl, text)
        retained_adapter_identity = any(name in text for name in exclusions)
        if count == 0 and not retained_adapter_identity:
            stats["content_classes_without_shared_refs"] += 1
            continue
        if count == 0 and retained_adapter_identity:
            stats["content_classes_copied_for_adapter_identity"] += 1

        after_cls = declared_class(patched)
        if after_cls != cls:
            raise SystemExit(f"class identity changed unexpectedly: {cls} -> {after_cls}")

        rel = path.relative_to(root)
        dst = out_scripts / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(patched, encoding="utf-8", newline="\n")
        changed_classes.append(cls)
        stats["content_classes_patched"] += 1

    report = {
        "prefix": args.prefix,
        "shared_core_reference_map_count": len(mapping),
        "excluded_rebinds": sorted(exclusions),
        "stats": dict(stats),
        "changed_classes": changed_classes,
        "skipped_shadow_class_count": len(skipped_shadow_classes),
        "unresolved_plan_classes": unresolved_plan_classes,
        "policy": {
            "content_class_identity_stays_namespaced": True,
            "shared_core_references_rebound_to_frontiers": True,
            "explicit_adapter_identities_may_remain_namespaced": True,
            "classes_relying_only_on_adapter_identity_are_preserved": True,
            "kr1_shadow_core_definitions_left_dormant": True,
        },
    }
    Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps({
        "shared_core_reference_map_count": len(mapping),
        "excluded_rebinds": sorted(exclusions),
        "content_classes_patched": stats["content_classes_patched"],
        "content_classes_copied_for_adapter_identity": stats["content_classes_copied_for_adapter_identity"],
        "reference_tokens_rebound": stats["reference_tokens_rebound"],
        "shadow_definitions_skipped": stats["shadow_definitions_skipped"],
        "unresolved_plan_classes": len(unresolved_plan_classes),
    }, indent=2))
    if not changed_classes:
        raise SystemExit("no KR1 content classes were patched or preserved for an adapter identity")


if __name__ == "__main__":
    main()
