#!/usr/bin/env python3
"""Generate a compile-only KR1__Level compatibility bridge over Frontiers Level.

The bridge is deliberately conservative: it only declares inherited KR1 Level
members the selected KR1 stage set references that are absent on Frontiers
Level. Missing fields are dynamic (`*`), and missing functions accept rest args
/ return `*`.

The adapter constructor is derived from the exported Frontiers `Level.as`
instead of assuming `Level()` is parameterless. This matters because FFDec
validates the parent-constructor arity while importing the replacement class.

This is a compiler bridge used to expose the next semantic incompatibilities.
It is not considered gameplay-complete until each generated stub is replaced by
an explicit Frontiers-backed implementation or shown to be irrelevant.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


def _split_params(raw: str) -> list[str]:
    """Split an AS3 parameter list at top-level commas only."""
    out: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    escaped = False
    pairs = {"(": ")", "[": "]", "{": "}"}
    closers = set(pairs.values())
    for i, ch in enumerate(raw):
        if quote is not None:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            continue
        if ch in pairs:
            depth += 1
            continue
        if ch in closers:
            depth = max(0, depth - 1)
            continue
        if ch == "," and depth == 0:
            out.append(raw[start:i].strip())
            start = i + 1
    tail = raw[start:].strip()
    if tail:
        out.append(tail)
    return out


def _constructor_from_frontiers(path: Path) -> tuple[str, list[str]]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    # FFDec may place the return annotation and opening brace on the same or a
    # following line, so search across whitespace but stop at the first body.
    m = re.search(
        r"\bfunction\s+Level\s*\((.*?)\)\s*(?::\s*[^\{\r\n]+)?\s*\{",
        text,
        flags=re.S,
    )
    if not m:
        raise SystemExit(f"could not locate Frontiers Level constructor in {path}")
    params = re.sub(r"\s+", " ", m.group(1).strip())
    args: list[str] = []
    for part in _split_params(params):
        p = part.strip()
        if not p:
            continue
        if p.startswith("..."):
            raise SystemExit(
                "Frontiers Level constructor uses a rest parameter; explicit "
                "super forwarding must be implemented before generating adapter"
            )
        name = re.split(r"[:=]", p, maxsplit=1)[0].strip()
        if not name or not re.fullmatch(r"[A-Za-z_$][\w$]*", name):
            raise SystemExit(f"could not parse constructor parameter name from: {part!r}")
        args.append(name)
    return params, args


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--frontiers-level", type=Path, help="exported Frontiers Level.as used to mirror constructor signature")
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    data = json.loads(args.contract.read_text(encoding="utf-8"))
    candidates = data.get("adapter_candidates", {})
    if not isinstance(candidates, dict):
        raise SystemExit("adapter contract missing adapter_candidates")

    if args.frontiers_level:
        ctor_params, ctor_args = _constructor_from_frontiers(args.frontiers_level)
    else:
        # Kept only for backwards-compatible local diagnostics. CI integration
        # probes must pass --frontiers-level so an arity mismatch cannot hide.
        ctor_params, ctor_args = "", []

    super_args = ",".join(ctor_args)
    lines = [
        "package",
        "{",
        "   public class KR1__Level extends Level",
        "   {",
        f"      public function KR1__Level({ctor_params})",
        "      {",
        f"         super({super_args});" if super_args else "         super();",
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
        "frontiers_constructor": {
            "parameters": ctor_params,
            "forwarded_arguments": ctor_args,
            "mirrored_from_source": bool(args.frontiers_level),
        },
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
