#!/usr/bin/env python3
"""Prepare an owned Kingdom Rush Frontiers Steam install for the full-content mod port.

This tool never modifies the original install and never writes game contents into the
repository automatically. It accepts either the Steam executable (when it is readable
as a ZIP/SFX archive) or an extracted `kr2` directory, copies/extracts into a caller-
chosen work directory, and writes a hash/candidate inventory for the Lua port.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

FEATURE_TERMS = {
    "levels": ["level", "stage", "campaign", "map", "elite"],
    "waves": ["wave", "waves", "spawn", "spawner"],
    "enemies": ["enemy", "enemies", "creep", "unit"],
    "heroes": ["hero", "heroes"],
    "upgrades": ["upgrade", "upgrades", "stars"],
    "economy": ["gold", "cash", "lives", "life"],
    "speed": ["speed", "timescale", "time_scale"],
    "victory": ["victory", "win", "gameover", "game_over", "end_level"],
    "save": ["save", "slot", "profile", "storage"],
    "towers": ["tower", "towers", "build", "building"],
    "ui": ["menu", "pause", "settings", "hud", "button"],
}

LEVEL_RE = re.compile(r"(?:level|stage)[_\- ]?(\d{1,2})", re.IGNORECASE)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract_kr2(exe: Path, out: Path) -> Path:
    if not zipfile.is_zipfile(exe):
        raise SystemExit(
            f"{exe} is not readable as a ZIP/SFX archive. Extract the installed game "
            "with a local archive tool and rerun this script with the extracted kr2 directory."
        )

    target = out / "kr2"
    target.mkdir(parents=True, exist_ok=True)
    root = target.resolve()

    with zipfile.ZipFile(exe) as zf:
        members = [m for m in zf.infolist() if m.filename.replace("\\", "/").startswith("kr2/")]
        if not members:
            raise SystemExit("Archive opened successfully, but no kr2/ directory was found.")
        for member in members:
            rel = Path(member.filename.replace("\\", "/")).relative_to("kr2")
            dest = (target / rel).resolve()
            if dest != root and root not in dest.parents:
                raise SystemExit(f"Refusing unsafe archive path: {member.filename}")
            if member.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst)
    return target


def copy_extracted_kr2(src: Path, out: Path) -> Path:
    target = out / "kr2"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(src, target)
    return target


def text_preview(path: Path, limit: int = 512_000) -> str:
    try:
        raw = path.read_bytes()[:limit]
        return raw.decode("utf-8", errors="ignore").lower()
    except OSError:
        return ""


def classify(path: Path, root: Path) -> dict:
    rel = path.relative_to(root).as_posix()
    low_name = rel.lower()
    body = text_preview(path) if path.suffix.lower() in {".lua", ".txt", ".json", ".cfg"} else ""
    haystack = low_name + "\n" + body

    matches = []
    for feature, terms in FEATURE_TERMS.items():
        if any(term in haystack for term in terms):
            matches.append(feature)

    levels = sorted({int(x) for x in LEVEL_RE.findall(haystack) if int(x) <= 99})
    return {
        "path": rel,
        "size": path.stat().st_size,
        "sha256": sha256(path),
        "feature_matches": matches,
        "level_numbers_seen": levels,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path, help="Owned Steam EXE or extracted kr2 directory")
    ap.add_argument("--out", type=Path, required=True, help="Work directory outside the Git repository")
    args = ap.parse_args()

    source = args.source.expanduser().resolve()
    out = args.out.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        raise SystemExit(f"Source does not exist: {source}")

    if source.is_dir():
        if source.name.lower() != "kr2":
            nested = source / "kr2"
            if nested.is_dir():
                source = nested
            else:
                raise SystemExit("Directory input must be kr2/ or contain a kr2/ directory.")
        game_root = copy_extracted_kr2(source, out)
        source_kind = "extracted-kr2"
        source_hash = None
    else:
        source_kind = "steam-exe"
        source_hash = sha256(source)
        game_root = safe_extract_kr2(source, out)

    files = [p for p in game_root.rglob("*") if p.is_file()]
    inventory = [classify(p, game_root) for p in files]

    lua_files = [x for x in inventory if x["path"].lower().endswith(".lua")]
    detected_levels = sorted({n for x in inventory for n in x["level_numbers_seen"]})
    feature_candidates = {
        feature: [x["path"] for x in inventory if feature in x["feature_matches"]][:200]
        for feature in FEATURE_TERMS
    }

    report = {
        "source_kind": source_kind,
        "source_sha256": source_hash,
        "game_root": str(game_root),
        "file_count": len(files),
        "lua_file_count": len(lua_files),
        "detected_level_numbers": detected_levels,
        "has_post_campaign_level_markers": any(n > 15 for n in detected_levels),
        "feature_candidates": feature_candidates,
        "files": inventory,
    }

    report_path = out / "krf-steam-inventory.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Prepared: {game_root}")
    print(f"Files: {len(files)} ({len(lua_files)} Lua)")
    if detected_levels:
        print("Level markers seen:", ", ".join(map(str, detected_levels)))
    else:
        print("Level markers seen: none found by filename/text heuristic")
    print("Post-campaign markers (>15):", "yes" if report["has_post_campaign_level_markers"] else "not detected")
    print(f"Inventory: {report_path}")
    print("Next: use the inventory to implement and verify PORT-MANIFEST.json against this exact owned build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
