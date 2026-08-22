#!/usr/bin/env python3
"""Extract non-expressive structural signatures from FFDec ActionScript exports.

The output is intentionally metadata only: class names and cross-class references
needed to map imported stages. It never emits decompiled method bodies.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


LEVEL_FILE_RE = re.compile(r"^Level(\d+)\.as$", re.I)
TOKEN_PATTERNS = {
    "enemies": re.compile(r"\bEnemy[A-Za-z0-9_]*\b"),
    "towers": re.compile(r"\bTower[A-Za-z0-9_]*\b"),
    "heroes": re.compile(r"\bSoldierHero[A-Za-z0-9_]*\b"),
    "soldiers": re.compile(r"\bSoldier[A-Za-z0-9_]*\b"),
    "sounds": re.compile(r"\bSound_[A-Za-z0-9_]*\b"),
    "levels": re.compile(r"\bLevel\d+\b"),
}

# Terms helpful for distinguishing post-campaign stages without copying prose.
STAGE_MARKERS = (
    "Sarelgaz", "Acaroth", "Rotten", "Fungal", "Bandit", "Troll",
    "Yeti", "Demon", "Veznan", "Necromancer", "Zombie", "Spider",
    "Boss", "Forest", "Ice", "Lava", "Pand", "Blackburn", "Nightfang",
)


def signature(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    item = {"class": path.stem}
    for key, pattern in TOKEN_PATTERNS.items():
        values = sorted(set(pattern.findall(text)))
        if key == "levels":
            values = [x for x in values if x.lower() != path.stem.lower()]
        item[key] = values
    low = text.lower()
    item["markers"] = sorted({m for m in STAGE_MARKERS if m.lower() in low})
    # Counts are useful complexity signals and reveal no code.
    item["source_chars"] = len(text)
    item["method_keyword_count"] = len(re.findall(r"\bfunction\b", text))
    return item


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", help="FFDec scripts directory")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(args.scripts)
    if not root.is_dir():
        raise SystemExit(f"scripts directory not found: {root}")

    rows = []
    for path in sorted(root.rglob("Level*.as")):
        m = LEVEL_FILE_RE.match(path.name)
        if not m:
            continue
        row = signature(path)
        row["number"] = int(m.group(1))
        rows.append(row)
    rows.sort(key=lambda x: x["number"])

    out = {
        "level_count": len(rows),
        "level_numbers": [r["number"] for r in rows],
        "levels": rows,
    }
    Path(args.output).write_text(json.dumps(out, indent=2), encoding="utf-8", newline="\n")
    print(f"wrote {args.output}: {len(rows)} level classes")


if __name__ == "__main__":
    main()
