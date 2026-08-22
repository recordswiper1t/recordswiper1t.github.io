#!/usr/bin/env python3
"""Stable tower/hero IDs for the combined KR1 + Frontiers runtime."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Tower:
    id: str
    game: str
    family: str
    title: str
    tier: int = 4


@dataclass(frozen=True)
class Hero:
    id: str
    game: str
    title: str
    role: str = "selectable"
    source_requirement: str = "audit_source"


TOWERS = [
    Tower("kr1-rangers-hideout", "kr1", "archer", "Ranger's Hideout"),
    Tower("kr1-musketeer-garrison", "kr1", "archer", "Musketeer Garrison"),
    Tower("krf-crossbow-fort", "krf", "archer", "Crossbow Fort"),
    Tower("krf-tribal-axethrowers", "krf", "archer", "Tribal Axethrowers"),

    Tower("kr1-holy-order", "kr1", "barracks", "Holy Order"),
    Tower("kr1-barbarian-mead-hall", "kr1", "barracks", "Barbarian Mead Hall"),
    Tower("krf-knights-templar", "krf", "barracks", "Knights Templar"),
    Tower("krf-assassins-guild", "krf", "barracks", "Assassin's Guild"),

    Tower("kr1-arcane-wizard", "kr1", "mage", "Arcane Wizard"),
    Tower("kr1-sorcerer-mage", "kr1", "mage", "Sorcerer Mage"),
    Tower("krf-archmage-tower", "krf", "mage", "Archmage Tower"),
    Tower("krf-necromancer-tower", "krf", "mage", "Necromancer Tower"),

    Tower("kr1-tesla-x104", "kr1", "artillery", "Tesla x104"),
    Tower("kr1-big-bertha", "kr1", "artillery", "500mm Big Bertha"),
    Tower("krf-dwaarp", "krf", "artillery", "DWAARP"),
    Tower("krf-battle-mecha-t200", "krf", "artillery", "Battle-Mecha T200"),
]

KR1_HEROES = [
    "Gerald Lightseeker", "Alleria Swiftwind", "Malik Hammerfury",
    "Bolin Farslayer", "Magnus Spellbane", "Ignus", "King Denas",
    "Elora Wintersong", "Ingvar Bearclaw", "Hacksaw", "Oni", "Thor", "Ten'Shí",
]

KRF_HEROES = [
    "Alric", "Mirage", "Cronan", "Bruxa", "Captain Blackthorne", "Nivus",
    "Dierdre", "Grawl", "Sha'tra", "Karkinos", "Kutsao", "Dante", "Kahz",
    "Saitam", "Ashbite", "Bonehart",
]

KRF_STAGE_HEROES = ["Rurin Longbeard", "The Black Corsair", "Lucrezia"]


def hero_id(game: str, title: str) -> str:
    chars = []
    for ch in title.lower():
        if ch.isalnum():
            chars.append(ch)
        elif not chars or chars[-1] != "-":
            chars.append("-")
    return f"{game}-" + "".join(chars).strip("-")


HEROES = [Hero(hero_id("kr1", h), "kr1", h) for h in KR1_HEROES]
HEROES += [Hero(hero_id("krf", h), "krf", h) for h in KRF_HEROES]
HEROES += [Hero(hero_id("krf", h), "krf", h, role="stage_secondary") for h in KRF_STAGE_HEROES]


def validate() -> None:
    tower_ids = [x.id for x in TOWERS]
    hero_ids = [x.id for x in HEROES]
    if len(tower_ids) != len(set(tower_ids)):
        raise SystemExit("duplicate tower IDs")
    if len(hero_ids) != len(set(hero_ids)):
        raise SystemExit("duplicate hero IDs")
    families = {family: [t for t in TOWERS if t.family == family] for family in ("archer", "barracks", "mage", "artillery")}
    for family, towers in families.items():
        if len(towers) != 4:
            raise SystemExit(f"{family}: expected four tier-4 choices, got {len(towers)}")
    if len([h for h in HEROES if h.game == "kr1" and h.role == "selectable"]) != 13:
        raise SystemExit("expected 13 selectable KR1 heroes")
    if len([h for h in HEROES if h.game == "krf" and h.role == "selectable"]) != 16:
        raise SystemExit("expected 16 selectable KRF heroes")
    if len([h for h in HEROES if h.role == "stage_secondary"]) != 3:
        raise SystemExit("expected three Frontiers secondary stage heroes")


def main() -> None:
    validate()
    out = {
        "summary": {
            "tier4_towers": len(TOWERS),
            "tier4_choices_per_family": 4,
            "selectable_kr1_heroes": 13,
            "selectable_krf_heroes": 16,
            "selectable_heroes_total": 29,
            "krf_secondary_stage_heroes": 3,
        },
        "towers": [asdict(x) for x in TOWERS],
        "heroes": [asdict(x) for x in HEROES],
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
