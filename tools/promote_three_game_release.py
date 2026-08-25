#!/usr/bin/env python3
"""Promote the verified V17/V3.1/V4.3 assets across every public entry point."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def rewrite(relative: str, replacements: list[tuple[str, str]]) -> None:
    path = ROOT / relative
    original = path.read_text(encoding="utf-8")
    text = original
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
        elif new not in text:
            raise SystemExit(f"{relative}: neither old nor new release marker exists: {old!r}")
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    # Self-host the current stable Ruffle runtime.  The public CDN remains an
    # emergency option documented in the build manifest, not a hard startup
    # dependency for every visit.
    for path in ROOT.rglob("*.html"):
        original = path.read_text(encoding="utf-8")
        text = original
        old = "https://unpkg.com/@ruffle-rs/ruffle@0.5.0"
        if old in text:
            text = text.replace(old, "/vendor/ruffle/0.5.0/ruffle.js")
        # Do not let Ruffle consume the first in-game click merely to satisfy
        # browser audio autoplay. Sound remains available from the player menu.
        text = text.replace("unmuteOverlay:'visible'", "unmuteOverlay:'hidden'")
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")

    rewrite("ultimate/play.html", [
        ("Combined Ultimate V16", "Combined Ultimate V17"),
        ("kingdom-rush-ultimate-v16.swf?v=16-native-crossover-r1", "kingdom-rush-ultimate-v17.swf?v=17-direct-map-r1"),
        ("kingdom-rush-ultimate-v16.swf", "kingdom-rush-ultimate-v17.swf"),
        ("Loading native maps, unified star ledger and stateful crossover war rooms…", "Opening the saved native map, unified star ledger and stateful crossover war rooms…"),
    ])
    rewrite("stickwar-complete/index.html", [
        ("Complete Expansion V3</title>", "Complete Expansion V3.1</title>"),
        ("COMPLETE EXPANSION V3</span>", "COMPLETE EXPANSION V3.1</span>"),
        ("stick-war-complete-v3.swf?v=3-objectives-atlas-forge-r1", "stick-war-complete-v31.swf?v=31-direct-lab-forge-r2"),
        ("super-stick-war-v3.swf", "super-stick-war-v31.swf"),
    ])
    rewrite("iphone/stickwar.html", [
        ("COMPLETE EXPANSION V3</div>", "COMPLETE EXPANSION V3.1</div>"),
        ("stick-war-complete-v3.swf?v=iphone-v3-objectives-forge", "stick-war-complete-v31.swf?v=iphone-v31-direct-lab-r2"),
        ("super-stick-war-v3.swf", "super-stick-war-v31.swf"),
        ("Super Stick War V3 • objectives + atlas + soldier-card sandbox", "Super Stick War V3.1 • direct lab + objectives + soldier-card sandbox"),
    ])
    rewrite("epicwar5-expansion/index.html", [
        ("Expansion V4.2", "Expansion V4.3"),
        ("EXPANSION V4.2", "EXPANSION V4.3"),
        ("epic-war-5-expansion-v42.swf?v=42-direct-access-r1", "epic-war-5-expansion-v43.swf?v=43-forge-palette-r1"),
        ("epic-war-5-expansion-v42.swf", "epic-war-5-expansion-v43.swf"),
        ("quality:'high'", "quality:quality()"),
    ])
    rewrite("iphone/epicwar5.html", [
        ("Expansion V4.2", "Expansion V4.3"),
        ("epic-war-5-expansion-v42.swf?v=iphone-exp-v42-r1", "epic-war-5-expansion-v43.swf?v=iphone-exp-v43-r1"),
        ("epic-war-5-expansion-v42.swf", "epic-war-5-expansion-v43.swf"),
        ("direct campaign + authored warfronts + 8×", "direct campaign + polished Forge + 8×"),
    ])

    for relative in ("index.html", "games/index.html", "README.md", "desktop/README.md", "docs/KINGDOM_RUSH_ULTIMATE.md", "docs/KINGDOM_RUSH_ULTIMATE_STATUS.md"):
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("KR + KRF V16", "KR + KRF V17").replace("Ultimate V16", "Ultimate V17")
        text = re.sub(r"Complete Expansion V3(?!\.1)", "Complete Expansion V3.1", text)
        text = text.replace("Expansion V4.2", "Expansion V4.3").replace("V4.2", "V4.3")
        text = text.replace("kingdom-rush-ultimate-v16.swf", "kingdom-rush-ultimate-v17.swf")
        text = text.replace("stick-war-complete-v3.swf", "stick-war-complete-v31.swf")
        text = text.replace("epic-war-5-expansion-v42.swf", "epic-war-5-expansion-v43.swf")
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8", newline="\n")

    for relative in ("desktop/run-native.ps1", "desktop/run_native.py"):
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        text = text.replace("kingdom-rush-ultimate-v16.swf", "kingdom-rush-ultimate-v17.swf")
        text = text.replace("stick-war-complete-v3.swf", "stick-war-complete-v31.swf")
        text = text.replace("epic-war-5-expansion-v42.swf", "epic-war-5-expansion-v43.swf")
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8", newline="\n")

    print("Promoted KR Ultimate V17, Super Stick War V3.1 and Epic War 5 V4.3 across public launchers")


if __name__ == "__main__":
    main()
