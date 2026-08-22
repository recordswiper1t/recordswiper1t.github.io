#!/usr/bin/env python3
"""Launch the optimized Kingdom Rush Frontiers V8 mod in native Ruffle.

The launcher prefers the verified V8 SWF and falls back to the historical V7
asset only if V8 is missing. Ruffle is downloaded once and cached locally.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
V8_SWF = ROOT / "assets" / "kingdom-rush-frontiers-v8.swf"
V7_SWF = ROOT / "assets" / "kingdom-rush-frontiers-v5.swf"
SWF = V9_SWF if V9_SWF.exists() else (V8_SWF if V8_SWF.exists() else V7_SWF)
CACHE = ROOT / ".native" / "ruffle"
RELEASES_API = "https://api.github.com/repos/ruffle-rs/ruffle/releases?per_page=30"


def request_json(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "krf-native-launcher"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def platform_patterns() -> tuple[list[str], list[str]]:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "windows":
        return ["windows"], ["x86_64", "x64", "64"]
    if system == "darwin":
        if machine in {"arm64", "aarch64"}:
            return ["macos", "darwin", "osx"], ["aarch64", "arm64", "universal"]
        return ["macos", "darwin", "osx"], ["x86_64", "x64", "universal"]
    if system == "linux":
        if machine in {"arm64", "aarch64"}:
            return ["linux"], ["aarch64", "arm64"]
        return ["linux"], ["x86_64", "x64", "64"]
    raise SystemExit(f"Unsupported operating system: {platform.system()}")


def score_asset(name: str) -> int:
    low = name.lower()
    os_words, arch_words = platform_patterns()
    if not any(word in low for word in os_words) or not any(word in low for word in arch_words):
        return -1
    if not (low.endswith(".zip") or low.endswith(".tar.gz") or low.endswith(".tgz")):
        return -1
    score = 10
    if "desktop" in low:
        score += 5
    if "extension" in low or "web" in low:
        score -= 20
    if "x86_64" in low or "aarch64" in low or "arm64" in low:
        score += 2
    return score


def choose_release(channel: str):
    releases = request_json(RELEASES_API)
    candidates = []
    for rel in releases:
        if rel.get("draft"):
            continue
        if channel == "stable" and rel.get("prerelease"):
            continue
        if channel == "nightly" and not rel.get("prerelease"):
            continue
        candidates.append(rel)
    if not candidates:
        raise SystemExit(f"No Ruffle {channel} release found.")
    return candidates[0]


def choose_asset(release):
    ranked = sorted(((score_asset(a.get("name", "")), a) for a in release.get("assets", [])), key=lambda item: item[0], reverse=True)
    if not ranked or ranked[0][0] < 0:
        names = ", ".join(a.get("name", "?") for a in release.get("assets", []))
        raise SystemExit(f"Could not find a desktop Ruffle build for this laptop. Assets: {names}")
    return ranked[0][1]


def find_executable(folder: Path) -> Path:
    names = {"ruffle.exe"} if os.name == "nt" else {"ruffle"}
    matches = [p for p in folder.rglob("*") if p.is_file() and p.name.lower() in names]
    if not matches:
        raise SystemExit("Downloaded Ruffle archive did not contain a desktop executable.")
    exe = sorted(matches, key=lambda p: len(p.parts))[0]
    if os.name != "nt":
        exe.chmod(exe.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return exe


def install(channel: str) -> Path:
    release = choose_release(channel)
    asset = choose_asset(release)
    tag = release.get("tag_name", "unknown")
    marker = CACHE / "VERSION"
    if marker.exists() and marker.read_text(encoding="utf-8").strip() == tag:
        try:
            return find_executable(CACHE)
        except SystemExit:
            pass
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="krf-ruffle-") as tmp:
        archive = Path(tmp) / asset["name"]
        req = urllib.request.Request(asset["browser_download_url"], headers={"User-Agent": "krf-native-launcher"})
        with urllib.request.urlopen(req, timeout=120) as src, archive.open("wb") as dst:
            shutil.copyfileobj(src, dst)
        staging = Path(tmp) / "unpacked"
        staging.mkdir()
        low = archive.name.lower()
        if low.endswith(".zip"):
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(staging)
        elif low.endswith((".tar.gz", ".tgz")):
            with tarfile.open(archive, "r:gz") as tf:
                tf.extractall(staging)
        else:
            raise SystemExit(f"Unsupported Ruffle archive: {archive.name}")
        if CACHE.exists():
            shutil.rmtree(CACHE)
        shutil.copytree(staging, CACHE)
        marker.write_text(tag + "\n", encoding="utf-8")
    return find_executable(CACHE)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run optimized Kingdom Rush Frontiers V8 in native Ruffle")
    parser.add_argument("--stable", action="store_true", help="Use the latest stable Ruffle instead of nightly")
    parser.add_argument("--refresh", action="store_true", help="Redownload Ruffle")
    parser.add_argument("ruffle_args", nargs=argparse.REMAINDER, help="Extra arguments forwarded to Ruffle after --")
    args = parser.parse_args()
    if not SWF.exists():
        raise SystemExit(f"Missing game SWF: {SWF}")
    if args.refresh and CACHE.exists():
        shutil.rmtree(CACHE)
    channel = "stable" if args.stable else "nightly"
    exe = install(channel)
    extra = args.ruffle_args[1:] if args.ruffle_args and args.ruffle_args[0] == "--" else args.ruffle_args
    version = "V8 optimized" if SWF == V8_SWF else "V7 fallback"
    print(f"Launching Kingdom Rush Frontiers {version} with native Ruffle ({channel})")
    print(f"Game: {SWF}")
    print(f"Ruffle: {exe}")
    return subprocess.call([str(exe), str(SWF), *extra], cwd=str(ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
