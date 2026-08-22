#!/usr/bin/env python3
"""Build a KR1__Level bridge using only required members from namespaced KR1 source.

The source is expected to come from a transient FFDec export of the already
namespaced structural merge. Only members named by the stage adapter contract
are copied into a subclass of the authoritative Frontiers Level. This keeps the
Frontiers runtime for shared behavior while preserving KR1 implementations for
members Frontiers does not expose under the same API name.

No publisher source is stored by this tool; it operates on caller-supplied local
exports and writes a generated build artifact/report.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_level_adapter import _constructor_from_frontiers  # noqa: E402
from level_api_diff import FUNC_RE, VAR_RE  # noqa: E402
from level_semantic_match import find_matching_brace  # noqa: E402


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def extract_field(text: str, name: str) -> str | None:
    for m in VAR_RE.finditer(text):
        if m.group(3) != name:
            continue
        start = text.rfind("\n", 0, m.start()) + 1
        semi = text.find(";", m.end())
        if semi < 0:
            return None
        chunk = text[start:semi + 1].strip()
        # The original class used public members for the stage contract. Keep
        # declarations concrete instead of degrading them to dynamic `*`.
        return "      " + chunk
    return None


def extract_function(text: str, name: str) -> str | None:
    for m in FUNC_RE.finditer(text):
        if m.group(2) != name:
            continue
        start = text.rfind("\n", 0, m.start()) + 1
        brace = text.find("{", m.end())
        if brace < 0:
            return None
        end = find_matching_brace(text, brace)
        if end is None:
            return None
        chunk = text[start:end + 1].strip()
        # A method may have overridden the old KR1 ancestor but is absent from
        # Frontiers Level by definition of this contract, so `override` is not
        # valid on the generated bridge.
        chunk = re.sub(r"\boverride\s+", "", chunk, count=1)
        return "\n".join("      " + line.strip() if line.strip() else "" for line in chunk.splitlines())
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--namespaced-kr1-level", type=Path, required=True)
    ap.add_argument("--frontiers-level", type=Path, required=True)
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    source = read(args.namespaced_kr1_level)
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    candidates = contract.get("adapter_candidates", {})
    if not isinstance(candidates, dict):
        raise SystemExit("contract missing adapter_candidates")

    ctor_params, ctor_args = _constructor_from_frontiers(args.frontiers_level)
    super_args = ",".join(ctor_args)
    chunks: list[str] = []
    copied: list[dict] = []
    missing: list[str] = []

    for name in sorted(candidates):
        rows = candidates[name].get("kr1_signatures", []) if isinstance(candidates[name], dict) else []
        kinds = {str(r.get("kind")) for r in rows if isinstance(r, dict)}
        if "function" in kinds:
            chunk = extract_function(source, name)
            kind = "function"
        else:
            chunk = extract_field(source, name)
            kind = "field"
        if chunk is None:
            missing.append(name)
            continue
        chunks.append(chunk)
        copied.append({"name": name, "kind": kind})

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
    for chunk in chunks:
        lines.append(chunk)
        lines.append("")
    lines += ["   }", "}", ""]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    report = {
        "copied_member_count": len(copied),
        "copied_members": copied,
        "missing_members": missing,
        "frontiers_constructor": {"parameters": ctor_params, "forwarded_arguments": ctor_args},
        "policy": {
            "frontiers_level_is_parent": True,
            "only_contract_missing_members_copied": True,
            "source_is_namespaced_merge_export": True,
            "generated_source_not_committed": True,
        },
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
