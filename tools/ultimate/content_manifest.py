#!/usr/bin/env python3
"""Canonical content scope for Kingdom Rush Ultimate.

Stable stage IDs are separated from whatever obfuscated/native source names a
particular release uses. `source_locator` records source material that has
actually been structurally verified; missing later content stays fail-closed.
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
    source_locator: Optional[str] = None


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


def main_chain(game: str, titles: list[str], source_requirement: str) -> list[Stage]:
    stages: list[Stage] = []
    previous = None
    for index, title in enumerate(titles, 1):
        sid = f"{game}-{slug(title)}"
        stages.append(Stage(
            sid, game, title, "main", index, previous,
            source_requirement=source_requirement,
            source_locator=f"Level{index}",
        ))
        previous = sid
    return stages


STAGES: list[Stage] = []
STAGES += main_chain("kr1", KR_MAIN, "publisher_flash")

# The historical Armor Games publisher SWF was structurally audited with
# FFDec 26.2.1. Besides Level1-Level12, it contains Level13-Level19. Enemy and
# marker signatures identify those seven extra classes as the stages below.
# Do not label later KR1 stages embedded: they are absent from this source.
KR_DARK_TOWER = "kr1-the-dark-tower"
KR_ELITE = [
    # title, unlock_after, verified source class (None => external/reconstruct)
    ("Sarelgaz's Lair", KR_DARK_TOWER, "Level13"),
    ("Ruins of Acaroth", KR_DARK_TOWER, "Level14"),
    ("Rotten Forest", KR_DARK_TOWER, "Level15"),
    ("Fungal Forest", "kr1-rotten-forest", None),
    ("Hushwood", KR_DARK_TOWER, "Level16"),
    ("Bandit's Lair", "kr1-hushwood", "Level17"),
    ("Glacial Heights", KR_DARK_TOWER, "Level18"),
    ("Ha'Kraj Plateau", "kr1-glacial-heights", "Level19"),
    ("Pit of Fire", KR_DARK_TOWER, None),
    ("Pandaemonium", "kr1-pit-of-fire", None),
    ("Rotwick", KR_DARK_TOWER, None),
    ("Ancient Necropolis", "kr1-rotwick", None),
    ("Nightfang Swale", "kr1-ancient-necropolis", None),
    ("Castle Blackburn", "kr1-nightfang-swale", None),
]
for i, (title, unlock, locator) in enumerate(KR_ELITE, 1):
    STAGES.append(Stage(
        f"kr1-{slug(title)}", "kr1", title, "post_campaign", i, unlock,
        source_requirement="publisher_flash" if locator else "non_flash_or_reconstruction",
        source_locator=locator,
    ))

STAGES.append(Stage(
    "kr1-rage-valley", "kr1", "Rage Valley", "endless", 1,
    "kr1-the-citadel", source_requirement="non_flash_or_reconstruction",
))

STAGES += main_chain("krf", KRF_MAIN, "frontiers_flash")

# Frontiers' later post-campaign stages are not embedded in the Flash build
# used by the existing V11/V12 mod. They need a compatible owned-source export
# or reconstruction inside the Frontiers Flash runtime.
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

    verified_kr_levels = {
        int(s.source_locator.removeprefix("Level"))
        for s in STAGES
        if s.game == "kr1" and s.source_locator and s.source_locator.startswith("Level")
    }
    if verified_kr_levels != set(range(1, 20)):
        raise SystemExit(f"KR1 publisher-source Level1-19 coverage mismatch: {sorted(verified_kr_levels)}")


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
        "verified_kr1_publisher_levels": sum(s.source_requirement == "publisher_flash" for s in STAGES),
        "missing_or_reconstruction": sum(s.source_requirement == "non_flash_or_reconstruction" for s in STAGES),
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
