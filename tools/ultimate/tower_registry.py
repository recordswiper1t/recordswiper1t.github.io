#!/usr/bin/env python3
"""Canonical runtime identities for all 16 Ultimate tier-4 tower branches.

Stable IDs come from roster_manifest. Runtime class names are verified against
the KR1 publisher/KRF structural inventories. KR1 classes are the namespaced
identities that exist after the Stage-1 binary merge.

`ultimate_action` is deliberately independent from legacy V11 qol action names;
the eventual four-way tower menu and clipboard can use one stable vocabulary.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json

from roster_manifest import TOWERS, validate as validate_roster


@dataclass(frozen=True)
class TowerRoute:
    id: str
    game: str
    family: str
    title: str
    runtime_class: str
    source_class: str
    ultimate_action: str
    legacy_qol_action: str | None
    tier3_family_class: str


SOURCE_CLASSES = {
    "kr1-rangers-hideout": "TowerArcherRanger",
    "kr1-musketeer-garrison": "TowerArcherMusketeer",
    "krf-crossbow-fort": "TowerArcherCrossbow",
    "krf-tribal-axethrowers": "TowerArcherTotem",

    "kr1-holy-order": "TowerSoldierPaladin",
    "kr1-barbarian-mead-hall": "TowerSoldierBarbarian",
    "krf-knights-templar": "TowerSoldierTemplar",
    "krf-assassins-guild": "TowerSoldierAssassin",

    "kr1-arcane-wizard": "TowerMageArcane",
    "kr1-sorcerer-mage": "TowerMageSorcerer",
    "krf-archmage-tower": "TowerMageArchmage",
    "krf-necromancer-tower": "TowerMageNecromancer",

    "kr1-tesla-x104": "TowerEngineerTesla",
    "kr1-big-bertha": "TowerEngineerBfg",
    "krf-dwaarp": "TowerEngineerDwaarp",
    "krf-battle-mecha-t200": "TowerEngineerMech",
}

LEGACY_QOL = {
    "krf-crossbow-fort": "qol_crossbow",
    "krf-tribal-axethrowers": "qol_totem",
    "krf-knights-templar": "qol_templar",
    "krf-assassins-guild": "qol_assassin",
    "krf-archmage-tower": "qol_archmage",
    "krf-necromancer-tower": "qol_necro",
    "krf-dwaarp": "qol_dwaarp",
    "krf-battle-mecha-t200": "qol_mecha",
}

TIER3_FAMILY = {
    "archer": "TowerArcher",
    "barracks": "TowerSoldier",
    "mage": "TowerMage",
    "artillery": "TowerEngineer",
}


def action_for(tower_id: str) -> str:
    return "ultimate_" + tower_id.replace("-", "_")


def route_for(tower) -> TowerRoute:
    source = SOURCE_CLASSES[tower.id]
    return TowerRoute(
        id=tower.id,
        game=tower.game,
        family=tower.family,
        title=tower.title,
        runtime_class=("KR1__" + source) if tower.game == "kr1" else source,
        source_class=source,
        ultimate_action=action_for(tower.id),
        legacy_qol_action=LEGACY_QOL.get(tower.id),
        tier3_family_class=TIER3_FAMILY[tower.family],
    )


def routes() -> list[TowerRoute]:
    validate_roster()
    return [route_for(t) for t in TOWERS]


def validate() -> None:
    rows = routes()
    ids = [r.id for r in rows]
    runtime = [r.runtime_class for r in rows]
    actions = [r.ultimate_action for r in rows]
    if len(rows) != 16:
        raise SystemExit(f"expected 16 tier-4 routes, got {len(rows)}")
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate tower IDs")
    if len(runtime) != len(set(runtime)):
        raise SystemExit("duplicate runtime tower class identities")
    if len(actions) != len(set(actions)):
        raise SystemExit("duplicate Ultimate tower actions")
    if set(SOURCE_CLASSES) != set(ids):
        raise SystemExit("source class map does not exactly cover roster tower IDs")
    for family in TIER3_FAMILY:
        group = [r for r in rows if r.family == family]
        if len(group) != 4 or {r.game for r in group} != {"kr1", "krf"}:
            raise SystemExit(f"{family}: expected two KR1 and two KRF tier-4 branches")
    for row in rows:
        if row.game == "kr1" and not row.runtime_class.startswith("KR1__"):
            raise SystemExit(f"{row.id}: KR1 runtime class must be namespaced")
        if row.game == "krf" and row.runtime_class.startswith("KR1__"):
            raise SystemExit(f"{row.id}: KRF runtime class must not be namespaced")


def payload() -> dict:
    validate()
    rows = routes()
    return {
        "summary": {
            "tier4_routes": len(rows),
            "families": 4,
            "choices_per_family": 4,
            "kr1_routes": sum(r.game == "kr1" for r in rows),
            "krf_routes": sum(r.game == "krf" for r in rows),
            "legacy_qol_actions_reused": sum(r.legacy_qol_action is not None for r in rows),
            "new_kr1_actions_needed": sum(r.game == "kr1" for r in rows),
        },
        "routes": [asdict(r) for r in rows],
        "families": {
            family: [asdict(r) for r in rows if r.family == family]
            for family in ("archer", "barracks", "mage", "artillery")
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    data = payload()
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data["summary"], indent=2))


if __name__ == "__main__":
    main()
