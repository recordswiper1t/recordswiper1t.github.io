#!/usr/bin/env python3
"""Launch the newest optimized Kingdom Rush Frontiers mod in native Ruffle.

Windows avoids Vulkan by default because current Ruffle/wgpu builds can panic in
the Vulkan command backend on some drivers. The launcher prefers DX12 and retries
OpenGL when DX12 exits unsuccessfully. Use --vulkan only for explicit testing.
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
V11_SWF = ROOT / "assets" / "kingdom-rush-frontiers-v11.swf"
V10_SWF = ROOT / "assets" / "kingdom-rush-frontiers-v10.swf"
V9_SWF = ROOT / "assets" / "kingdom-rush-frontiers-v9.swf"
V8_SWF = ROOT / "assets" / "kingdom-rush-frontiers-v8.swf"
V7_SWF = ROOT / "assets" / "kingdom-rush-frontiers-v5.swf"
SWF = next((p for p in (V11_SWF, V10_SWF, V9_SWF, V8_SWF, V7_SWF) if p.exists()), V11_SWF)
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
        return ["macos", "darwin", "osx"], ["aarch64", "arm64", "universal"] if machine in {"arm64", "aarch64"} else ["x86_64", "x64", "universal"]
    if system == "linux":
        return ["linux"], ["aarch64", "arm64"] if machine in {"arm64", "aarch64"} else ["x86_64", "x64", "64"]
    raise SystemExit(f"Unsupported operating system: {platform.system()}")


def score_asset(name: str) -> int:
    low = name.lower()
    os_words, arch_words = platform_patterns()
    if not any(word in low for word in os_words) or not any(word in low for word in arch_words):
        return -1
    if not (low.endswith(".zip") or low.endswith(".tar.gz") or low.endswith(".tgz")):
        return -1
    score = 10 + (5 if "desktop" in low else 0) + (2 if any(x in low for x in ("x86_64", "aarch64", "arm64")) else 0)
    if "extension" in low or "web" in low:
        score -= 20
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
        raise SystemExit("Could not find a native Ruffle archive for this system.")
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
        if archive.name.lower().endswith(".zip"):
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(staging)
        else:
            with tarfile.open(archive, "r:gz") as tf:
                tf.extractall(staging)
        if CACHE.exists():
            shutil.rmtree(CACHE)
        shutil.copytree(staging, CACHE)
        marker.write_text(tag + "\n", encoding="utf-8")
    return find_executable(CACHE)


def run_ruffle(exe: Path, backend: str | None, extra: list[str]) -> int:
    env = os.environ.copy()
    cmd = [str(exe)]
    if backend:
        env["WGPU_BACKEND"] = backend
        cmd += ["--graphics", backend]
    cmd += [str(SWF), *extra]
    return subprocess.call(cmd, cwd=str(ROOT), env=env)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run optimized Kingdom Rush Frontiers in native Ruffle")
    parser.add_argument("--stable", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--vulkan", action="store_true", help="Explicitly test Vulkan on Windows")
    parser.add_argument("--gl", action="store_true", help="Force OpenGL")
    parser.add_argument("ruffle_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not SWF.exists():
        raise SystemExit(f"Missing game SWF: {SWF}")
    if args.refresh and CACHE.exists():
        shutil.rmtree(CACHE)
    exe = install("stable" if args.stable else "nightly")
    extra = args.ruffle_args[1:] if args.ruffle_args and args.ruffle_args[0] == "--" else args.ruffle_args
    backend = None
    if platform.system().lower() == "windows":
        backend = "vulkan" if args.vulkan else ("gl" if args.gl else "dx12")
    print(f"Launching {SWF.name} with native Ruffle" + (f" ({backend})" if backend else ""))
    code = run_ruffle(exe, backend, extra)
    if code != 0 and platform.system().lower() == "windows" and backend not in {"vulkan", "gl"}:
        print(f"Ruffle exited with code {code}; retrying with OpenGL.")
        code = run_ruffle(exe, "gl", extra)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
