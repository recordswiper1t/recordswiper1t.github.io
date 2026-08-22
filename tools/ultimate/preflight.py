#!/usr/bin/env python3
"""Preflight the source material needed for a real KR1 + KRF merge.

No game binaries are downloaded by this script. Point it at copies you are
legally entitled to use. The existing Frontiers mod remains the authoritative
runtime/base; KR1 and later Frontiers content are import sources only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from content_manifest import STAGES, summary, validate


SWF_MAGIC = {b"FWS", b"CWS", b"ZWS"}


def inspect_swf(path: Path) -> dict:
    result = {"path": str(path), "exists": path.is_file(), "valid_swf": False}
    if not path.is_file():
        return result
    with path.open("rb") as fh:
        magic = fh.read(3)
    result["valid_swf"] = magic in SWF_MAGIC
    result["size"] = path.stat().st_size
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    result["sha256"] = digest.hexdigest()
    return result


def select_frontiers(path: Path) -> Path:
    """Prefer V12.1, then V12, then V11 when using the default release path."""
    if path.exists():
        return path
    if path.name == "kingdom-rush-frontiers-v12-1.swf":
        for name in ("kingdom-rush-frontiers-v12.swf", "kingdom-rush-frontiers-v11.swf"):
            fallback = path.with_name(name)
            if fallback.exists():
                return fallback
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontiers",
        default="assets/kingdom-rush-frontiers-v12-1.swf",
        help="current V12.1 release if available; V12 then V11 are supported fallbacks",
    )
    parser.add_argument(
        "--kingdom-rush",
        dest="kr1",
        help="local original Kingdom Rush SWF; do not fetch from unofficial mirrors",
    )
    parser.add_argument(
        "--frontiers-extra-export",
        help="optional directory containing later/non-Flash Frontiers stage exports",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    validate()
    frontiers = select_frontiers(Path(args.frontiers))

    report = {
        "scope": summary(),
        "frontiers": inspect_swf(frontiers),
        "kingdom_rush": inspect_swf(Path(args.kr1)) if args.kr1 else {"path": None, "exists": False, "valid_swf": False},
        "frontiers_extra_export": {
            "path": args.frontiers_extra_export,
            "exists": bool(args.frontiers_extra_export and Path(args.frontiers_extra_export).is_dir()),
        },
        "missing_source_groups": [],
    }

    if not report["frontiers"]["valid_swf"]:
        report["missing_source_groups"].append("frontiers_runtime")
    if not report["kingdom_rush"]["valid_swf"]:
        report["missing_source_groups"].append("kingdom_rush_original")

    needs_extra = any(
        s.game == "krf" and s.source_requirement == "non_flash_or_reconstruction"
        for s in STAGES
    )
    if needs_extra and not report["frontiers_extra_export"]["exists"]:
        report["missing_source_groups"].append("frontiers_post_campaign_and_endless")

    report["ready_for_full_binary_merge"] = not report["missing_source_groups"]

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Kingdom Rush Ultimate preflight")
        print(f"  Frontiers runtime: {'OK' if report['frontiers']['valid_swf'] else 'MISSING'} - {report['frontiers']['path']}")
        print(f"  KR1 source:        {'OK' if report['kingdom_rush']['valid_swf'] else 'MISSING'} - {report['kingdom_rush']['path']}")
        print(f"  KRF later stages:  {'OK' if report['frontiers_extra_export']['exists'] else 'SOURCE/RECONSTRUCTION NEEDED'}")
        print(f"  Full merge ready:  {'YES' if report['ready_for_full_binary_merge'] else 'NO'}")
        if report["missing_source_groups"]:
            print("  Blockers: " + ", ".join(report["missing_source_groups"]))
    return 0 if report["ready_for_full_binary_merge"] else 2


if __name__ == "__main__":
    sys.exit(main())
