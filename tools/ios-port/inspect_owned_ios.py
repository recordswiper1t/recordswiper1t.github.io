#!/usr/bin/env python3
"""Inventory an owned Kingdom Rush Frontiers iOS app without decrypting it.

Input may be an IPA (ordinary ZIP container) or an extracted .app/Payload directory.
The tool records metadata, hashes, file types, likely script/data candidates, and
post-campaign level markers. It never modifies the input, never decrypts the main
Mach-O executable, and never writes proprietary file contents to the report.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import plistlib
import re
import sys
import zipfile
from pathlib import Path
from typing import BinaryIO, Iterable

TEXT_EXTS = {
    ".lua", ".luac", ".json", ".plist", ".xml", ".txt", ".cfg", ".ini",
    ".csv", ".atlas", ".fnt", ".shader", ".glsl", ".dat"
}
SCRIPTISH_EXTS = {".lua", ".luac", ".js", ".json", ".plist", ".xml", ".dat", ".bin", ".pak"}
ARCHIVE_EXTS = {".zip", ".pak", ".bundle", ".obb", ".dat"}

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

LEVEL_RE = re.compile(r"(?:level|stage)[_\- .]?(\d{1,2})", re.IGNORECASE)
KNOWN_EXTRA_STAGES = {
    "port_tortuga": ["port tortuga", "port_tortuga", "porttortuga"],
    "storm_atoll": ["storm atoll", "storm_atoll", "stormatoll"],
    "sunken_citadel": ["sunken citadel", "sunken_citadel", "sunkencitadel"],
    "bonesburg": ["bonesburg"],
    "desecrated_grove": ["desecrated grove", "desecrated_grove", "desecratedgrove"],
    "dusk_chateau": ["dusk chateau", "dusk_chateau", "duskchateau"],
    "darklight_depths": ["darklight depths", "darklight_depths", "darklightdepths"],
}


def digest_stream(stream: BinaryIO) -> str:
    h = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(chunk)
    return h.hexdigest()


def decode_preview(raw: bytes) -> str:
    # We intentionally use only a bounded preview for heuristic classification.
    return raw[:512_000].decode("utf-8", errors="ignore").lower()


def classify_text(name: str, preview: str) -> tuple[list[str], list[int], list[str]]:
    haystack = (name + "\n" + preview).lower()
    features = [feature for feature, terms in FEATURE_TERMS.items() if any(t in haystack for t in terms)]
    levels = sorted({int(x) for x in LEVEL_RE.findall(haystack) if 1 <= int(x) <= 99})
    extras = [stage for stage, terms in KNOWN_EXTRA_STAGES.items() if any(t in haystack for t in terms)]
    return features, levels, extras


def nested_zip_names(raw: bytes, suffix: str) -> list[str]:
    if suffix not in ARCHIVE_EXTS and not raw.startswith(b"PK\x03\x04"):
        return []
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            return zf.namelist()[:500]
    except (zipfile.BadZipFile, OSError):
        return []


def summarize_blob(name: str, size: int, sha256: str, preview_raw: bytes = b"") -> dict:
    suffix = Path(name).suffix.lower()
    preview = decode_preview(preview_raw) if suffix in TEXT_EXTS else ""
    features, levels, extras = classify_text(name, preview)
    nested = nested_zip_names(preview_raw, suffix)
    nested_text = "\n".join(nested).lower()
    if nested_text:
        n_features, n_levels, n_extras = classify_text(name, nested_text)
        features = sorted(set(features + n_features))
        levels = sorted(set(levels + n_levels))
        extras = sorted(set(extras + n_extras))
    return {
        "path": name,
        "size": size,
        "sha256": sha256,
        "extension": suffix,
        "script_or_data_candidate": suffix in SCRIPTISH_EXTS or bool(nested),
        "feature_matches": features,
        "level_numbers_seen": levels,
        "extra_stage_markers": extras,
        "nested_archive_member_names": nested,
    }


def find_app_prefix(names: Iterable[str]) -> str:
    candidates = []
    for name in names:
        normalized = name.replace("\\", "/")
        if normalized.startswith("Payload/") and ".app/" in normalized:
            prefix = normalized.split(".app/", 1)[0] + ".app/"
            candidates.append(prefix)
    if not candidates:
        raise SystemExit("IPA opened, but no Payload/*.app directory was found.")
    return sorted(set(candidates), key=len)[0]


def read_ipa(source: Path) -> tuple[dict, list[dict]]:
    with zipfile.ZipFile(source) as zf:
        names = zf.namelist()
        app_prefix = find_app_prefix(names)
        info_name = app_prefix + "Info.plist"
        info = {}
        if info_name in names:
            try:
                info = plistlib.loads(zf.read(info_name))
            except Exception:
                info = {"plist_parse_error": True}

        files = []
        for zi in zf.infolist():
            if zi.is_dir() or not zi.filename.startswith(app_prefix):
                continue
            rel = zi.filename[len(app_prefix):]
            with zf.open(zi) as stream:
                sha = digest_stream(stream)
            preview_raw = b""
            suffix = Path(rel).suffix.lower()
            if suffix in TEXT_EXTS or suffix in ARCHIVE_EXTS or zi.file_size <= 2_000_000:
                try:
                    preview_raw = zf.read(zi)[:2_000_000]
                except Exception:
                    preview_raw = b""
            files.append(summarize_blob(rel, zi.file_size, sha, preview_raw))
        return info, files


def locate_app_dir(source: Path) -> Path:
    if source.suffix.lower() == ".app" and source.is_dir():
        return source
    if source.is_dir():
        apps = sorted(source.glob("Payload/*.app")) + sorted(source.glob("*.app"))
        if apps:
            return apps[0]
    raise SystemExit("Directory input must be an .app directory or contain Payload/*.app.")


def read_app_dir(source: Path) -> tuple[dict, list[dict]]:
    app = locate_app_dir(source)
    info = {}
    plist_path = app / "Info.plist"
    if plist_path.is_file():
        try:
            info = plistlib.loads(plist_path.read_bytes())
        except Exception:
            info = {"plist_parse_error": True}

    files = []
    for path in app.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(app).as_posix()
        with path.open("rb") as stream:
            sha = digest_stream(stream)
        preview_raw = b""
        suffix = path.suffix.lower()
        if suffix in TEXT_EXTS or suffix in ARCHIVE_EXTS or path.stat().st_size <= 2_000_000:
            try:
                preview_raw = path.read_bytes()[:2_000_000]
            except OSError:
                pass
        files.append(summarize_blob(rel, path.stat().st_size, sha, preview_raw))
    return info, files


def safe_plist_summary(info: dict) -> dict:
    keys = [
        "CFBundleDisplayName", "CFBundleName", "CFBundleIdentifier",
        "CFBundleShortVersionString", "CFBundleVersion", "CFBundleExecutable",
        "MinimumOSVersion", "DTPlatformVersion", "DTSDKName"
    ]
    return {k: info.get(k) for k in keys if k in info}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path, help="Owned IPA or extracted .app/Payload directory")
    ap.add_argument("--out", type=Path, required=True, help="JSON inventory output path")
    args = ap.parse_args()

    source = args.source.expanduser().resolve()
    out = args.out.expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Source does not exist: {source}")

    if source.is_file():
        if not zipfile.is_zipfile(source):
            raise SystemExit("File input must be an ordinary ZIP-format IPA. This tool does not decrypt executables.")
        info, files = read_ipa(source)
        source_kind = "ipa"
        with source.open("rb") as f:
            source_sha = digest_stream(f)
    else:
        info, files = read_app_dir(source)
        source_kind = "app-directory"
        source_sha = None

    detected_levels = sorted({n for f in files for n in f["level_numbers_seen"]})
    extra_markers = sorted({m for f in files for m in f["extra_stage_markers"]})
    candidates = [f for f in files if f["script_or_data_candidate"]]
    by_feature = {
        feature: [f["path"] for f in files if feature in f["feature_matches"]][:250]
        for feature in FEATURE_TERMS
    }

    executable_name = info.get("CFBundleExecutable") if isinstance(info, dict) else None
    executable_entry = next((f for f in files if f["path"] == executable_name), None)

    report = {
        "tool_scope": "resource inventory only; no FairPlay/DRM decryption",
        "source_kind": source_kind,
        "source_sha256": source_sha,
        "bundle": safe_plist_summary(info if isinstance(info, dict) else {}),
        "file_count": len(files),
        "script_or_data_candidate_count": len(candidates),
        "detected_level_numbers": detected_levels,
        "known_extra_stage_markers": extra_markers,
        "has_post_campaign_evidence": any(n > 15 for n in detected_levels) or bool(extra_markers),
        "main_executable": executable_entry,
        "feature_candidates": by_feature,
        "candidate_files": candidates,
        "files": files,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    bundle = report["bundle"]
    print("Bundle:", bundle.get("CFBundleIdentifier", "unknown"))
    print("Version:", bundle.get("CFBundleShortVersionString", "unknown"))
    print("Files:", report["file_count"])
    print("Script/data candidates:", report["script_or_data_candidate_count"])
    print("Level numbers seen:", detected_levels or "none")
    print("Extra-stage markers:", extra_markers or "none")
    print("Post-campaign evidence:", "yes" if report["has_post_campaign_evidence"] else "not detected")
    print("Inventory:", out)
    print("No executable decryption was attempted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
