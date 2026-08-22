#!/usr/bin/env python3
"""Generate a compile-only KR1__Level compatibility bridge over Frontiers Level.

The bridge is deliberately conservative: it only declares inherited KR1 Level
members Southport references that are absent on Frontiers Level. Missing fields
are dynamic (`*`), and missing functions accept rest args / return `*`.

This is a compiler bridge used to expose the next semantic incompatibilities.
It is not considered gameplay-complete until each generated stub is replaced by
an explicit Frontiers-backed implementation or shown to be irrelevant.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    data = json.loads(args.contract.read_text(encoding="utf-8"))
    candidates = data.get("adapter_candidates", {})
    if not isinstance(candidates, dict):
        raise SystemExit("adapter contract missing adapter_candidates")

    lines = [
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
    generated = []
    unresolved = []
    seen = set()

    for name in sorted(candidates):
        rows = candidates[name].get("kr1_signatures", []) if isinstance(candidates[name], dict) else []
        if not rows:
            unresolved.append(name)
            continue
        # A name should not be emitted twice even if the decompiler produced
        # multiple signature-like rows for the same member.
        if name in seen:
            continue
        seen.add(name)
        kinds = {str(r.get("kind")) for r in rows if isinstance(r, dict)}
        if "function" in kinds:
            lines += [
                f"      public function {name}(...args) : *",
                "      {",
                "         return null;",
                "      }",
                "",
            ]
            generated.append({"name": name, "kind": "function", "strategy": "rest_args_null_stub"})
        else:
            lines.append(f"      public var {name}:* = null;")
            lines.append("")
            generated.append({"name": name, "kind": "field", "strategy": "dynamic_null_stub"})

    lines += ["   }", "}", ""]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")

    report = {
        "generated_member_count": len(generated),
        "generated_members": generated,
        "unresolved_members": unresolved,
        "policy": {
            "extends_frontiers_level": True,
            "compile_bridge_only": True,
            "no_kr1_method_bodies_copied": True,
            "stubs_require_semantic_replacement_before_playable": True,
        },
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if unresolved:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
