#!/usr/bin/env python3
"""Build the first playable-integration candidate: KR1 Southport via KRF Level.

Input is a Stage-1 fully-namespaced merged SWF produced by build_ultimate.py
--structural-merge, plus the original KR1/KRF ActionScript exports used to create
its port policy.

This tool does not claim gameplay correctness. It proves the repeatable binary
sequence:
  1. export the merged SWF;
  2. derive Southport's KR1-vs-KRF Level API contract;
  3. replace existing KR1__Level with a thin Frontiers-Level compile bridge;
  4. rebind KR1__Level1 shared references while retaining that adapter identity;
  5. replace both already-existing classes with FFDec -importScript;
  6. re-export and verify the inheritance and V11/V12 enhancement markers.

Generated adapter stubs are explicitly reported as semantic TODOs. A successful
compile is an integration milestone, not a playable-stage certification.
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


def run(cmd: list[str], *, allow_fail: bool = False, stdout=None) -> int:
    print("+", " ".join(map(str, cmd)))
    p = subprocess.run(cmd, stdout=stdout)
    if p.returncode and not allow_fail:
        raise SystemExit(f"command failed ({p.returncode}): {' '.join(map(str, cmd))}")
    return p.returncode


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require(path: Path, label: str) -> Path:
    if not path.exists():
        raise SystemExit(f"missing {label}: {path}")
    return path


def locate(root: Path, filename: str) -> Path:
    exact = root / filename
    if exact.is_file():
        return exact
    hits = list(root.rglob(filename))
    if len(hits) != 1:
        raise SystemExit(f"expected exactly one {filename} under {root}, found {len(hits)}")
    return hits[0]


def export_scripts(ffdec: Path, swf: Path, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    log = out.parent / f"{out.name}-export.log"
    with log.open("wb") as fh:
        run([
            "java", "-Xmx6g", "-jar", str(ffdec),
            "-onerror", "ignore", "-timeout", "90", "-exportFileTimeout", "180",
            "-export", "script", str(out), str(swf),
        ], allow_fail=True, stdout=fh)
    scripts = out / "scripts"
    if not scripts.is_dir() or not any(scripts.rglob("*.as")):
        raise SystemExit(f"FFDec export produced no scripts: {swf}")
    return scripts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ffdec", type=Path, required=True)
    ap.add_argument("--merged-swf", type=Path, required=True, help="Stage-1 namespaced merged SWF")
    ap.add_argument("--kr1-scripts", type=Path, required=True, help="original KR1 FFDec scripts directory")
    ap.add_argument("--krf-scripts", type=Path, required=True, help="enhanced KRF FFDec scripts directory")
    ap.add_argument("--port-plan", type=Path, required=True)
    ap.add_argument("--output", type=Path, default=Path("work/ultimate/southport-adapter"))
    ap.add_argument("--keep-temp", action="store_true")
    args = ap.parse_args()

    ffdec = require(args.ffdec.resolve(), "ffdec.jar")
    merged = require(args.merged_swf.resolve(), "Stage-1 merged SWF")
    kr1_scripts = require(args.kr1_scripts.resolve(), "KR1 scripts")
    krf_scripts = require(args.krf_scripts.resolve(), "KRF scripts")
    port_plan = require(args.port_plan.resolve(), "port plan")

    output = args.output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    reports = output / "reports"
    reports.mkdir()

    temp_ctx = None
    if args.keep_temp:
        temp = output / "temp"
        temp.mkdir()
    else:
        temp_ctx = tempfile.TemporaryDirectory(prefix="kr-ultimate-southport-")
        temp = Path(temp_ctx.name)

    merged_export = export_scripts(ffdec, merged, temp / "merged-export")
    locate(merged_export, "KR1__Level1.as")
    locate(merged_export, "KR1__Level.as")
    locate(merged_export, "Level.as")

    kr1_level = locate(kr1_scripts, "Level.as")
    kr1_level1 = locate(kr1_scripts, "Level1.as")
    krf_level = locate(krf_scripts, "Level.as")

    api_contract = reports / "southport-level-api.json"
    api_skeleton = reports / "KR1__Level-adapter-skeleton.as"
    run([
        sys.executable, str(HERE / "level_api_diff.py"),
        "--kr1-level", str(kr1_level),
        "--krf-level", str(krf_level),
        "--kr1-stage", str(kr1_level1),
        "--output", str(api_contract),
        "--skeleton", str(api_skeleton),
    ])

    import_root = temp / "adapter-import"
    import_scripts = import_root / "scripts"
    import_scripts.mkdir(parents=True)
    adapter = import_scripts / "KR1__Level.as"
    adapter_report = reports / "level-adapter-build.json"
    adapter_code = run([
        sys.executable, str(HERE / "build_level_adapter.py"),
        "--contract", str(api_contract),
        "--frontiers-level", str(krf_level),
        "--output", str(adapter),
        "--report", str(adapter_report),
    ], allow_fail=True)
    if adapter_code != 0:
        raise SystemExit("adapter generator reported unresolved Southport inherited members")

    rebind_root = temp / "rebind"
    rebind_report = reports / "rebind-report.json"
    run([
        sys.executable, str(HERE / "rebind_namespaced_scripts.py"),
        "--scripts", str(merged_export),
        "--plan", str(port_plan),
        "--exclude-rebind", "KR1__Level",
        "--output", str(rebind_root),
        "--report", str(rebind_report),
    ])
    rebound_level1 = locate(rebind_root / "scripts", "KR1__Level1.as")
    level1_text = rebound_level1.read_text(encoding="utf-8-sig", errors="replace")
    if "extends KR1__Level" not in level1_text:
        raise SystemExit("Southport no longer extends the KR1__Level compatibility identity")
    shutil.copy2(rebound_level1, import_scripts / "KR1__Level1.as")

    candidate = output / "kingdom-rush-ultimate-southport-adapter.swf"
    import_log = reports / "import-adapter.log"
    with import_log.open("wb") as fh:
        code = run([
            "java", "-Xmx8g", "-jar", str(ffdec), "-onerror", "abort",
            "-importScript", str(merged), str(candidate), str(import_root),
        ], allow_fail=True, stdout=fh)
    if code != 0:
        result = {
            "compile_success": False,
            "exit_code": code,
            "stage": "kr1-southport",
            "meaning": "compatibility bridge exposed further compile/API mismatches",
            "gameplay_ready": False,
        }
        (reports / "SOUTHPORT-ADAPTER.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 3

    if not candidate.is_file() or candidate.stat().st_size < 3:
        raise SystemExit("FFDec reported success but candidate SWF is missing/empty")
    if candidate.read_bytes()[:3] not in (b"FWS", b"CWS", b"ZWS"):
        raise SystemExit("candidate does not have a valid SWF signature")

    verify_scripts = export_scripts(ffdec, candidate, temp / "verify")
    adapter_verify = locate(verify_scripts, "KR1__Level.as").read_text(encoding="utf-8-sig", errors="replace")
    stage_verify = locate(verify_scripts, "KR1__Level1.as").read_text(encoding="utf-8-sig", errors="replace")
    krf_verify = locate(verify_scripts, "Level.as").read_text(encoding="utf-8-sig", errors="replace")
    level15_verify = locate(verify_scripts, "Level15.as").read_text(encoding="utf-8-sig", errors="replace")

    checks = {
        "adapter_extends_frontiers_level": "class KR1__Level extends Level" in adapter_verify,
        "southport_extends_adapter": "extends KR1__Level" in stage_verify,
        "frontiers_clipboard_marker_preserved": "qolTowerClipboard" in krf_verify,
        "last_rift_marker_preserved_if_present_in_base": "THE LAST RIFT" in level15_verify,
    }
    if not checks["adapter_extends_frontiers_level"] or not checks["southport_extends_adapter"] or not checks["frontiers_clipboard_marker_preserved"]:
        raise SystemExit(f"post-import verification failed: {checks}")

    api = json.loads(api_contract.read_text(encoding="utf-8"))
    adapter_data = json.loads(adapter_report.read_text(encoding="utf-8"))
    result = {
        "compile_success": True,
        "stage": "kr1-southport",
        "candidate_swf": str(candidate),
        "candidate_sha256": sha256(candidate),
        "candidate_size": candidate.stat().st_size,
        "checks": checks,
        "frontiers_constructor_forwarding": adapter_data.get("frontiers_constructor", {}),
        "missing_frontiers_level_members_bridged": len(api.get("stage_refs_missing_on_krf", [])),
        "generated_compile_stub_count": adapter_data.get("generated_member_count", 0),
        "semantic_adapter_todos": [x.get("name") for x in adapter_data.get("generated_members", [])],
        "gameplay_ready": False,
        "next_gate": "replace generated compile stubs with explicit Frontiers-backed semantics, then runtime-test Southport",
    }
    (reports / "SOUTHPORT-ADAPTER.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))

    if temp_ctx is not None:
        temp_ctx.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
