#!/usr/bin/env python3
"""Reproducible preparation/build pipeline for Kingdom Rush Ultimate.

The default mode performs source inventory only. `--structural-merge` additionally
builds the collision-safe Stage-1 SWF: Frontiers remains the document/runtime and
all KR1 definitions/code are imported under a `KR1__` namespace with remapped SWF
character IDs. That output is intentionally marked *not gameplay ready* until the
shared-core rebind/adapters pass.
"""
from __future__ import annotations

import argparse
import hashlib
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


def run(cmd: list[str], *, stdout=None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True, stdout=stdout)


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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def structural_merge(
    ffdec: Path,
    frontiers: Path,
    kr1: Path,
    kr1_scripts: Path,
    work: Path,
    temp_root: Path,
    prefix: str,
) -> dict:
    structural = work / "structural"
    structural.mkdir(parents=True, exist_ok=True)
    class_map = structural / "kr1-class-map.json"
    merge_report = structural / "merge-report.json"
    merged_swf = structural / "kingdom-rush-ultimate-structural.swf"

    run([
        sys.executable, str(HERE / "extract_class_names.py"), str(kr1_scripts),
        "--prefix", prefix, "--output", str(class_map),
    ])

    kr1_xml = temp_root / "kr1.xml"
    krf_xml = temp_root / "krf.xml"
    merged_xml = temp_root / "ultimate-merged.xml"
    run(["java", "-Xmx6g", "-jar", str(ffdec), "-swf2xml", str(kr1), str(kr1_xml)])
    run(["java", "-Xmx6g", "-jar", str(ffdec), "-swf2xml", str(frontiers), str(krf_xml)])
    run([
        sys.executable, str(HERE / "merge_swf_xml.py"),
        "--base", str(krf_xml), "--source", str(kr1_xml),
        "--class-map", str(class_map), "--output", str(merged_xml),
        "--report", str(merge_report),
    ])
    run(["java", "-Xmx8g", "-jar", str(ffdec), "-xml2swf", str(merged_xml), str(merged_swf)])

    info = inspect_swf(merged_swf)
    if not info["valid_swf"]:
        raise SystemExit("Stage-1 XML merge did not produce a valid SWF")

    verify_root = temp_root / "verify-structural"
    verify_scripts = export_scripts(ffdec, merged_swf, verify_root)
    required = [
        verify_scripts / "Level.as",
        verify_scripts / "Level15.as",
        verify_scripts / f"{prefix}Level1.as",
        verify_scripts / f"{prefix}Level13.as",
        verify_scripts / f"{prefix}Level19.as",
        verify_scripts / f"{prefix}TowerArcherRanger.as",
        verify_scripts / f"{prefix}TowerEngineerTesla.as",
    ]
    missing = [str(p.relative_to(verify_scripts)) for p in required if not p.is_file()]
    if missing:
        raise SystemExit(f"Stage-1 merge re-export missing required classes: {missing}")

    level_text = (verify_scripts / "Level.as").read_text(encoding="utf-8-sig", errors="replace")
    if "qolTowerClipboard" not in level_text:
        raise SystemExit("Stage-1 merge lost Frontiers sandbox/clipboard marker")
    level15_text = (verify_scripts / "Level15.as").read_text(encoding="utf-8-sig", errors="replace")
    last_rift_preserved = "THE LAST RIFT" in level15_text
    if frontiers.name.endswith("v12.swf") and not last_rift_preserved:
        raise SystemExit("Stage-1 merge lost V12 Last Rift marker")

    result = {
        "path": str(merged_swf),
        "size": merged_swf.stat().st_size,
        "sha256": sha256(merged_swf),
        "valid_swf": True,
        "prefix": prefix,
        "frontiers_mod_marker_preserved": True,
        "last_rift_preserved": last_rift_preserved,
        "verified_namespaced_classes": [p.stem for p in required[2:]],
        "merge_report": str(merge_report),
        "gameplay_ready": False,
        "next_gate": "shared-core rebind and Southport adapter/runtime verification",
    }
    (structural / "STRUCTURAL-MERGE.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8", newline="\n"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ffdec", required=True, help="path to ffdec.jar")
    parser.add_argument("--frontiers", default="assets/kingdom-rush-frontiers-v12.swf")
    parser.add_argument("--kingdom-rush", required=True, dest="kr1")
    parser.add_argument("--frontiers-extra-export", help="optional exported later KRF content")
    parser.add_argument("--work", default="work/ultimate")
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--structural-merge", action="store_true", help="also build collision-safe namespaced Stage-1 SWF")
    parser.add_argument("--kr1-prefix", default="KR1__")
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
    frontiers = frontiers.resolve()
    kr1 = Path(args.kr1).resolve()

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

    krf_scripts = export_scripts(ffdec, frontiers, temp_root / "krf")
    kr1_scripts = export_scripts(ffdec, kr1, temp_root / "kr1")

    report_path = work / "ultimate-inventory.json"
    run([
        sys.executable, str(HERE / "audit_exports.py"),
        "--kr1", str(kr1_scripts), "--krf", str(krf_scripts),
        "--output", str(report_path),
    ])

    port_plan = work / "kr1-port-plan.json"
    run([
        sys.executable, str(HERE / "port_plan.py"),
        "--kr1", str(kr1_scripts), "--krf", str(krf_scripts),
        "--output", str(port_plan),
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
        "port_plan": str(port_plan),
        "runtime_policy": "KRF V12/V11 is authoritative; KR1 content is collision-safe namespaced then selectively rebound",
        "merge_state": "source_inventory_ready",
        "next_gate": "build Stage-1 namespaced structural merge, then rebind Southport to Frontiers shared core",
    }

    if args.structural_merge:
        readiness["structural_merge"] = structural_merge(
            ffdec, frontiers, kr1, kr1_scripts, work, temp_root, args.kr1_prefix
        )
        readiness["merge_state"] = "structural_merge_ready"
        readiness["next_gate"] = "shared-core Southport rebind/adapters; output is not gameplay-ready yet"

    if args.keep_temp:
        readiness["exports"] = str(temp_root)

    (work / "BUILD-READINESS.json").write_text(
        json.dumps(readiness, indent=2), encoding="utf-8", newline="\n"
    )

    if tmp_ctx is not None:
        tmp_ctx.cleanup()

    print(f"Prepared Ultimate build in {work}")
    if args.structural_merge:
        print("Stage-1 structural SWF built and re-export verified; gameplay-ready remains false until rebind/adapters pass.")
    if not readiness["frontiers_later_content"]["source_export_exists"]:
        print("NOTE: later Frontiers post-campaign/endless content still needs a compatible source export or reconstruction.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
