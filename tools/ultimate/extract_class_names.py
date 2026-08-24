#!/usr/bin/env python3
"""Extract declared ActionScript class names from an FFDec scripts directory."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


CLASS_RE = re.compile(r"\b(?:public\s+|internal\s+|final\s+|dynamic\s+)*class\s+([^\s{]+)")
PLAIN_IDENTIFIER_RE = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")


def ffdec_raw_identifier(token: str) -> str:
    """Return the ABC local name represented by an FFDec AS3 identifier.

    FFDec wraps names that are not legal ActionScript identifiers in section
    signs, so ``§override do§`` represents the raw ABC string ``override do``.
    The XML merger operates on those raw strings, not on FFDec's source escape.
    """
    if len(token) >= 2 and token.startswith("§") and token.endswith("§"):
        return token[1:-1]
    return token


def namespaced_runtime_name(raw: str, prefix: str) -> str:
    if PLAIN_IDENTIFIER_RE.fullmatch(raw):
        return prefix + raw
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}Esc_{digest}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts")
    parser.add_argument("--prefix", default="KR1__")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    root = Path(args.scripts)
    if not root.is_dir():
        raise SystemExit(f"scripts directory not found: {root}")

    names: set[str] = set()
    for path in root.rglob("*.as"):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for match in CLASS_RE.finditer(text):
            token = match.group(1).strip().rstrip("{")
            if token:
                names.add(ffdec_raw_identifier(token))

    if not names:
        raise SystemExit("no classes detected")
    mapping = {
        name: namespaced_runtime_name(name, args.prefix)
        for name in sorted(names)
    }
    if len(set(mapping.values())) != len(mapping):
        raise SystemExit("namespaced class mapping produced a collision")
    Path(args.output).write_text(json.dumps({
        "prefix": args.prefix,
        "count": len(mapping),
        "classes": mapping,
    }, indent=2), encoding="utf-8", newline="\n")
    print(f"wrote {args.output}: {len(mapping)} classes")


if __name__ == "__main__":
    main()
