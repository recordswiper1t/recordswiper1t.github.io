#!/usr/bin/env python3
"""Runtime/source identities for the combined Ultimate hero roster.

The canonical roster remains 13 KR1 + 16 Frontiers selectable heroes. This file
adds the source reality needed by the binary port: the historical Armor Games
KR1 SWF contains nine of the thirteen KR1 selectable heroes as explicit
SoldierHero classes. The four later/missing heroes remain locked in scope but
are not falsely marked source-ready.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json

from roster_manifest import HEROES, validate as validate_roster


@dataclass(frozen=True)
class HeroRoute:
    id: str
    game: str
    title: str
    role: str
    source_class: str | None
    runtime_class: str | None
    source_ready: bool
    source_requirement: str


KR1_SOURCE_CLASSES = {
    "Gerald Lightseeker": "SoldierHeroGerald",
    "Alleria Swiftwind": "SoldierHeroAlleria",
    "Malik Hammerfury": "SoldierHeroMalik",
    "Bolin Farslayer": "SoldierHeroBolin",
    "Magnus Spellbane": "SoldierHeroMagnus",
    "Ignus": "SoldierHeroIgnus",
    "King Denas": "SoldierHeroDenas",
    "Elora Wintersong": "SoldierHeroFrost",
    "Ingvar Bearclaw": "SoldierHeroViking",
}

KR1_LATER_OR_MISSING = {"Hacksaw", "Oni", "Thor", "Ten'Shí"}


def route(hero) -> HeroRoute:
    if hero.game == "kr1":
        source = KR1_SOURCE_CLASSES.get(hero.title)
        ready = source is not None
        return HeroRoute(
            id=hero.id,
            game=hero.game,
            title=hero.title,
            role=hero.role,
            source_class=source,
            runtime_class=("KR1__" + source) if source else None,
            source_ready=ready,
            source_requirement="publisher_flash" if ready else "later_compatible_source_or_reconstruction",
        )
    # Frontiers exact class identities are audited separately because several
    # premium heroes are obfuscated in the available Flash build and the later
    # full 16-hero roster is not wholly embedded there.
    return HeroRoute(
        id=hero.id,
        game=hero.game,
        title=hero.title,
        role=hero.role,
        source_class=None,
        runtime_class=None,
        source_ready=False,
        source_requirement="frontiers_runtime_mapping_or_later_source",
    )


def routes() -> list[HeroRoute]:
    validate_roster()
    return [route(h) for h in HEROES]


def validate() -> None:
    rows = routes()
    kr1 = [r for r in rows if r.game == "kr1" and r.role == "selectable"]
    if len(kr1) != 13:
        raise SystemExit(f"expected 13 KR1 selectable heroes, got {len(kr1)}")
    ready = [r for r in kr1 if r.source_ready]
    blocked = [r for r in kr1 if not r.source_ready]
    if len(ready) != 9:
        raise SystemExit(f"expected nine source-ready publisher KR1 heroes, got {len(ready)}")
    if {r.title for r in blocked} != KR1_LATER_OR_MISSING:
        raise SystemExit("KR1 later/missing hero set drifted")
    runtime = [r.runtime_class for r in ready]
    if len(runtime) != len(set(runtime)):
        raise SystemExit("duplicate KR1 hero runtime identities")


def payload() -> dict:
    validate()
    rows = routes()
    kr1 = [r for r in rows if r.game == "kr1" and r.role == "selectable"]
    return {
        "summary": {
            "selectable_total": len([r for r in rows if r.role == "selectable"]),
            "kr1_selectable": len(kr1),
            "kr1_publisher_source_ready": sum(r.source_ready for r in kr1),
            "kr1_later_or_missing": sum(not r.source_ready for r in kr1),
            "frontiers_selectable_scope": len([r for r in rows if r.game == "krf" and r.role == "selectable"]),
            "frontiers_stage_secondary_scope": len([r for r in rows if r.game == "krf" and r.role == "stage_secondary"]),
        },
        "routes": [asdict(r) for r in rows],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    data = payload()
    print(json.dumps(data if args.json else data["summary"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
