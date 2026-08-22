#!/usr/bin/env python3
"""Canonical content scope for Kingdom Rush Ultimate.

This manifest is deliberately independent of obfuscated ActionScript class names.
The import/audit tooling maps these stable IDs onto whatever classes/symbols are
present in each source build.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from typing import Optional


@dataclass(frozen=True)
class Stage:
    id: str
    game: str
    title: str
    kind: str
    order: int
    unlock_after: Optional[str] = None
    source_requirement: str = "embedded"
    aliases: tuple[str, ...] = ()


KR_MAIN = [
    "Southport", "The Farmlands", "Pagras", "Twin Rivers", "Silveroak Forest",
    "The Citadel", "Coldstep Mines", "Icewind Pass", "Stormcloud Temple",
    "The Wastes", "Forsaken Valley", "The Dark Tower",
]

KRF_MAIN = [
    "Hammerhold", "Sandhawk Hamlet", "Sape Oasis", "Dunes of Despair",
    "Buccaneer's Den", "The Gates of Nazeru", "Crimson Valley",
    "Snapvine Bridge", "Lost Jungle", "Ma'qwa Urqu", "Temple of Saqra",
    "The Underpass", "Beresad's Lair", "The Dark Descent", "Emberspike Depths",
]


def slug(value: str) -> str:
    out = []
    for ch in value.lower():
        if ch.isalnum():
            out.append(ch)
        elif not out or out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def main_chain(game: str, titles: list[str]) -> list[Stage]:
    stages: list[Stage] = []
    previous = None
    for index, title in enumerate(titles, 1):
        sid = f"{game}-{slug(title)}"
        stages.append(Stage(sid, game, title, "main", index, previous))
        previous = sid
    return stages


STAGES: list[Stage] = []
STAGES += main_chain("kr1", KR_MAIN)

# KR1 post-campaign / elite content. Premium/mobile/modern builds may expose
# these differently, but the combined game treats them all as normal stages.
KR_DARK_TOWER = "kr1-the-dark-tower"
KR_ELITE = [
    ("Sarelgaz's Lair", KR_DARK_TOWER),
    ("Ruins of Acaroth", KR_DARK_TOWER),
    ("Rotten Forest", KR_DARK_TOWER),
    ("Fungal Forest", "kr1-rotten-forest"),
    ("Hushwood", KR_DARK_TOWER),
    ("Bandit's Lair", "kr1-hushwood"),
    ("Glacial Heights", KR_DARK_TOWER),
    ("Ha'Kraj Plateau", "kr1-glacial-heights"),
    ("Pit of Fire", KR_DARK_TOWER),
    ("Pandaemonium", "kr1-pit-of-fire"),
    ("Rotwick", KR_DARK_TOWER),
    ("Ancient Necropolis", "kr1-rotwick"),
    ("Nightfang Swale", "kr1-ancient-necropolis"),
    ("Castle Blackburn", "kr1-nightfang-swale"),
]
for i, (title, unlock) in enumerate(KR_ELITE, 1):
    STAGES.append(Stage(f"kr1-{slug(title)}", "kr1", title, "post_campaign", i, unlock))

STAGES.append(Stage(
    "kr1-rage-valley", "kr1", "Rage Valley", "endless", 1,
    "kr1-the-citadel", source_requirement="non_flash_or_reconstruction",
))

STAGES += main_chain("krf", KRF_MAIN)

# Frontiers' later post-campaign stages are not embedded in the Flash build
# used by the existing V11/V12 mod. They therefore need a supplied compatible
# source export or a reconstruction pass before they can be imported.
KRF_FINAL = "krf-emberspike-depths"
KRF_POST = [
    ("Port Tortuga", KRF_FINAL),
    ("Storm Atoll", "krf-port-tortuga"),
    ("The Sunken Citadel", "krf-storm-atoll"),
    ("Bonesburg", KRF_FINAL),
    ("Desecrated Grove", "krf-bonesburg"),
    ("Dusk Chateau", "krf-desecrated-grove"),
    ("Darklight Depths", KRF_FINAL),
]
for i, (title, unlock) in enumerate(KRF_POST, 1):
    STAGES.append(Stage(
        f"krf-{slug(title)}", "krf", title, "post_campaign", i, unlock,
        source_requirement="non_flash_or_reconstruction",
    ))

STAGES += [
    Stage(
        "krf-ruins-of-nasde", "krf", "Ruins of Nas'de", "endless", 1,
        "krf-the-gates-of-nazeru", source_requirement="non_flash_or_reconstruction",
    ),
    Stage(
        "krf-temple-of-evil", "krf", "Temple of Evil", "endless", 2,
        "krf-temple-of-saqra", source_requirement="non_flash_or_reconstruction",
        aliases=("Temple of Ethereal Evil",),
    ),
]

# Existing custom V12 content is retained as a bonus stage/mode, not counted as
# an original-game campaign map.
CUSTOM_STAGES = [
    Stage(
        "krf-v12-the-last-rift", "krf", "The Last Rift", "custom", 1,
        "krf-emberspike-depths", source_requirement="v12_branch",
    )
]


def validate() -> None:
    ids = [s.id for s in STAGES]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate stage IDs in manifest")
    known = set(ids)
    for stage in STAGES:
        if stage.unlock_after and stage.unlock_after not in known:
            raise SystemExit(f"{stage.id}: missing unlock target {stage.unlock_after}")
    expected = {
        ("kr1", "main"): 12,
        ("kr1", "post_campaign"): 14,
        ("kr1", "endless"): 1,
        ("krf", "main"): 15,
        ("krf", "post_campaign"): 7,
        ("krf", "endless"): 2,
    }
    for key, count in expected.items():
        actual = sum(1 for s in STAGES if (s.game, s.kind) == key)
        if actual != count:
            raise SystemExit(f"{key}: expected {count}, got {actual}")


def summary() -> dict[str, int]:
    return {
        "kr1_main": sum(s.game == "kr1" and s.kind == "main" for s in STAGES),
        "kr1_post_campaign": sum(s.game == "kr1" and s.kind == "post_campaign" for s in STAGES),
        "kr1_endless": sum(s.game == "kr1" and s.kind == "endless" for s in STAGES),
        "krf_main": sum(s.game == "krf" and s.kind == "main" for s in STAGES),
        "krf_post_campaign": sum(s.game == "krf" and s.kind == "post_campaign" for s in STAGES),
        "krf_endless": sum(s.game == "krf" and s.kind == "endless" for s in STAGES),
        "original_campaign_and_post": sum(s.kind in {"main", "post_campaign"} for s in STAGES),
        "original_all_including_endless": len(STAGES),
        "custom_bonus": len(CUSTOM_STAGES),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-custom", action="store_true")
    args = parser.parse_args()
    validate()
    stages = STAGES + (CUSTOM_STAGES if args.include_custom else [])
    if args.json:
        print(json.dumps({"summary": summary(), "stages": [asdict(s) for s in stages]}, indent=2))
    else:
        print(json.dumps(summary(), indent=2))


if __name__ == "__main__":
    main()
