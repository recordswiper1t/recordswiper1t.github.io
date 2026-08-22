#!/usr/bin/env python3
"""Reproducible preparation pipeline for Kingdom Rush Ultimate.

This intentionally refuses to fake a successful merge. It exports the supplied
binaries, audits both ActionScript trees, validates the full content manifest,
and creates a deterministic work bundle that the port patches consume.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content_manifest import STAGES, summary, validate  # noqa: E402
from preflight import inspect_swf  # noqa: E402


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def export_scripts(ffdec: Path, swf: Path, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    run([
        "java", "-Xmx4g", "-jar", str(ffdec),
        "-onerror", "ignore", "-timeout", "90", "-exportFileTimeout", "180",
        "-export", "script", str(out), str(swf),
    ])
    scripts = out / "scripts"
    if not scripts.is_dir() or not any(scripts.rglob("*.as")):
        raise SystemExit(f"FFDec export produced no ActionScript: {swf}")
    return scripts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ffdec", required=True, help="path to ffdec.jar")
    parser.add_argument("--frontiers", default="assets/kingdom-rush-frontiers-v12.swf")
    parser.add_argument("--kingdom-rush", required=True, dest="kr1")
    parser.add_argument("--frontiers-extra-export", help="optional exported later KRF content")
    parser.add_argument("--work", default="work/ultimate")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    validate()
    ffdec = Path(args.ffdec).resolve()
    if not ffdec.is_file():
        raise SystemExit(f"ffdec.jar not found: {ffdec}")

    frontiers = Path(args.frontiers)
    if not frontiers.exists() and frontiers.name.endswith("v12.swf"):
        fallback = frontiers.with_name("kingdom-rush-frontiers-v11.swf")
        if fallback.exists():
            frontiers = fallback
    kr1 = Path(args.kr1)

    fr_info = inspect_swf(frontiers)
    kr_info = inspect_swf(kr1)
    if not fr_info["valid_swf"]:
        raise SystemExit(f"invalid/missing Frontiers runtime: {frontiers}")
    if not kr_info["valid_swf"]:
        raise SystemExit(f"invalid/missing Kingdom Rush source: {kr1}")

    work = Path(args.work).resolve()
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)

    tmp_ctx = None
    if args.keep_temp:
        temp_root = work / "exports"
        temp_root.mkdir()
    else:
        tmp_ctx = tempfile.TemporaryDirectory(prefix="kr-ultimate-")
        temp_root = Path(tmp_ctx.name)

    krf_scripts = export_scripts(ffdec, frontiers.resolve(), temp_root / "krf")
    kr1_scripts = export_scripts(ffdec, kr1.resolve(), temp_root / "kr1")

    report_path = work / "ultimate-inventory.json"
    run([
        sys.executable, str(HERE / "audit_exports.py"),
        "--kr1", str(kr1_scripts), "--krf", str(krf_scripts),
        "--output", str(report_path),
    ])

    extra_path = Path(args.frontiers_extra_export).resolve() if args.frontiers_extra_export else None
    later_needed = [
        s.id for s in STAGES
        if s.game == "krf" and s.source_requirement == "non_flash_or_reconstruction"
    ]
    readiness = {
        "content_scope": summary(),
        "frontiers_runtime": fr_info,
        "kingdom_rush_source": kr_info,
        "frontiers_later_content": {
            "required_stage_ids": later_needed,
            "source_export": str(extra_path) if extra_path else None,
            "source_export_exists": bool(extra_path and extra_path.is_dir()),
        },
        "inventory": str(report_path),
        "runtime_policy": "KRF V12/V11 is authoritative; KR1 content is namespaced/imported into it",
        "merge_state": "source_inventory_ready",
        "next_gate": "namespace/import KR1 binary symbols and stage dependencies, then port later KRF maps",
    }
    (work / "BUILD-READINESS.json").write_text(json.dumps(readiness, indent=2), encoding="utf-8", newline="\n")

    # Preserve the exported scripts in the requested work directory only when
    # explicitly requested; otherwise the source export is temporary.
    if args.keep_temp:
        readiness["exports"] = str(temp_root)

    if tmp_ctx is not None:
        tmp_ctx.cleanup()

    print(f"Prepared Ultimate merge audit in {work}")
    if not readiness["frontiers_later_content"]["source_export_exists"]:
        print("NOTE: later Frontiers post-campaign/endless content still needs a compatible source export or reconstruction.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
