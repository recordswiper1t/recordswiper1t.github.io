#!/usr/bin/env python3
"""Launch the released Flash strategy mods in native Ruffle.

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
CACHE = ROOT / ".native" / "ruffle"
RELEASES_API = "https://api.github.com/repos/ruffle-rs/ruffle/releases?per_page=30"

KRF_CANDIDATES = [
    ROOT / "assets" / "kingdom-rush-frontiers-v12-1.swf",
    ROOT / "assets" / "kingdom-rush-frontiers-v12.swf",
    ROOT / "assets" / "kingdom-rush-frontiers-v11.swf",
    ROOT / "assets" / "kingdom-rush-frontiers-v10.swf",
    ROOT / "assets" / "kingdom-rush-frontiers-v9.swf",
    ROOT / "assets" / "kingdom-rush-frontiers-v8.swf",
    ROOT / "assets" / "kingdom-rush-frontiers-v5.swf",
]
GAME_FILES = {
    "stickwar": ROOT / "assets" / "stick-war-complete-v1.swf",
    "epicwar5": ROOT / "assets" / "epic-war-5-sandbox-v2.swf",
    "epicwar5-expansion": ROOT / "assets" / "epic-war-5-expansion-v331.swf",
}
GAME_ALIASES = {
    "krf": "krf",
    "kingdom-rush": "krf",
    "frontiers": "krf",
    "stickwar": "stickwar",
    "stick-war": "stickwar",
    "sw": "stickwar",
    "epicwar5": "epicwar5",
    "epic-war-5": "epicwar5",
    "ew5": "epicwar5",
    "epicwar5-expansion": "epicwar5-expansion",
    "epic-war-5-expansion": "epicwar5-expansion",
    "ew5-expansion": "epicwar5-expansion",
}
GAME_LABELS = {
    "krf": "Kingdom Rush Frontiers",
    "stickwar": "Super Stick War (SW1 + SW2)",
    "epicwar5": "Epic War 5 (stable V1.05-based build)",
    "epicwar5-expansion": "Epic War 5 Expansion (experimental)",
}


def request_json(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "strategy-mod-native-launcher"})
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
    with tempfile.TemporaryDirectory(prefix="strategy-mod-ruffle-") as tmp:
        archive = Path(tmp) / asset["name"]
        req = urllib.request.Request(asset["browser_download_url"], headers={"User-Agent": "strategy-mod-native-launcher"})
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


def choose_game(value: str) -> tuple[str, Path]:
    key = GAME_ALIASES.get(value.lower())
    if not key:
        raise SystemExit(f"Unknown game {value!r}. Choose krf, stickwar, epicwar5, or epicwar5-expansion.")
    if key == "krf":
        swf = next((p for p in KRF_CANDIDATES if p.exists()), KRF_CANDIDATES[0])
    else:
        swf = GAME_FILES[key]
    if not swf.exists():
        raise SystemExit(f"Missing game SWF: {swf}")
    return key, swf


def run_ruffle(exe: Path, swf: Path, backend: str | None, extra: list[str]) -> int:
    env = os.environ.copy()
    cmd = [str(exe)]
    if backend:
        env["WGPU_BACKEND"] = backend
        cmd += ["--graphics", backend]
    cmd += [str(swf), *extra]
    return subprocess.call(cmd, cwd=str(ROOT), env=env)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the released strategy mods in native Ruffle")
    parser.add_argument("--game", default="krf", help="krf, stickwar, epicwar5, or epicwar5-expansion (default: krf)")
    parser.add_argument("--stable", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--vulkan", action="store_true", help="Explicitly test Vulkan on Windows")
    parser.add_argument("--gl", action="store_true", help="Force OpenGL")
    parser.add_argument("--dx12", action="store_true", help="Force DirectX 12 on Windows")
    parser.add_argument("ruffle_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    game, swf = choose_game(args.game)
    if args.refresh and CACHE.exists():
        shutil.rmtree(CACHE)
    exe = install("stable" if args.stable else "nightly")
    extra = args.ruffle_args[1:] if args.ruffle_args and args.ruffle_args[0] == "--" else args.ruffle_args
    backend = None
    if platform.system().lower() == "windows":
        backend = "vulkan" if args.vulkan else ("gl" if args.gl else "dx12")
        if args.dx12:
            backend = "dx12"
    print(f"Launching {GAME_LABELS[game]}: {swf.name}" + (f" ({backend})" if backend else ""))
    code = run_ruffle(exe, swf, backend, extra)
    if code != 0 and platform.system().lower() == "windows" and backend not in {"vulkan", "gl"}:
        print(f"Ruffle exited with code {code}; retrying with OpenGL.")
        code = run_ruffle(exe, swf, "gl", extra)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
