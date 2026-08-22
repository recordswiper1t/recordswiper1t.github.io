#!/usr/bin/env python3
"""Extract declared ActionScript class names from an FFDec scripts directory."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


CLASS_RE = re.compile(r"\b(?:public\s+|internal\s+|final\s+|dynamic\s+)*class\s+([^\s{]+)")


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
            name = match.group(1).strip().rstrip("{")
            if name:
                names.add(name)

    if not names:
        raise SystemExit("no classes detected")
    mapping = {name: args.prefix + name for name in sorted(names)}
    Path(args.output).write_text(json.dumps({
        "prefix": args.prefix,
        "count": len(mapping),
        "classes": mapping,
    }, indent=2), encoding="utf-8", newline="\n")
    print(f"wrote {args.output}: {len(mapping)} classes")


if __name__ == "__main__":
    main()
