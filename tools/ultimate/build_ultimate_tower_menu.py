#!/usr/bin/env python3
"""Patch the enhanced Frontiers runtime with the first Ultimate KR1 tower surface.

This patch deliberately uses string/reflection based construction for the eight
namespaced KR1 tier-4 classes. That keeps the Frontiers source compilable before
those classes are present, while the final merged SWF can resolve them after the
KR1 XML/tag import and tower-core rebind.

The first integration surface is intentionally additive:
- the normal four Frontiers build families are untouched;
- the existing V11/V12 sandbox special pages are preserved;
- a new `Kingdom Rush towers ->` page exposes all eight KR1 tier-4 branches;
- Ctrl+C/Ctrl+V recognises the namespaced KR1 tower identities immediately;
- ability-rank cloning remains a separate gate until exact KR1 upgrade fields
  are structurally audited and given `qolBlueprintActions()` implementations.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


KR1_TOWERS = [
    ("ultimate_kr1_rangers_hideout", "KR1__TowerArcherRanger", "tw_archer", "Rangers Hideout"),
    ("ultimate_kr1_musketeer_garrison", "KR1__TowerArcherMusketeer", "tw_archer", "Musketeer Garrison"),
    ("ultimate_kr1_holy_order", "KR1__TowerSoldierPaladin", "tw_soldier", "Holy Order"),
    ("ultimate_kr1_barbarian_mead_hall", "KR1__TowerSoldierBarbarian", "tw_soldier", "Barbarian Mead Hall"),
    ("ultimate_kr1_arcane_wizard", "KR1__TowerMageArcane", "tw_mage", "Arcane Wizard"),
    ("ultimate_kr1_sorcerer_mage", "KR1__TowerMageSorcerer", "tw_mage", "Sorcerer Mage"),
    ("ultimate_kr1_tesla_x104", "KR1__TowerEngineerTesla", "tw_engineer", "Tesla x104"),
    ("ultimate_kr1_big_bertha", "KR1__TowerEngineerBfg", "tw_engineer", "500mm Big Bertha"),
]


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"missing source: {path}")
    return path.read_text(encoding="utf-8-sig", errors="strict")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def patch_level(text: str) -> tuple[str, dict]:
    marker = 'case "KR1__TowerArcherRanger":'
    if marker in text:
        return text, {"already_patched": True, "clipboard_routes_added": 8}

    anchor = '''            case "TowerSoldierTemplar":\n               return "qol_templar";\n'''
    cases = ''.join(
        f'''            case "{cls}":\n               return "{action}";\n'''
        for action, cls, _icon, _title in KR1_TOWERS
    )
    text = replace_once(text, anchor, anchor + cases, "KR1 clipboard root actions")
    return text, {"already_patched": False, "clipboard_routes_added": len(KR1_TOWERS)}


def menu_entry(action: str, icon: str, title: str, slot: int) -> str:
    return f'''new Array("{action}","{icon}",0,false,0,0,0,{slot},"TooltipBasic",{{\n               "title":"{title}",\n               "text":"Ultimate KR1 tower. Final campaign pricing and exact ability-rank clipboard support are verified separately."\n            }})'''


def patch_holder(text: str) -> tuple[str, dict]:
    if 'private function ultimatePlaceKR1Tower' in text:
        return text, {"already_patched": True, "tower_actions_added": 8}

    # Add a navigation entry to the existing advanced-normal-towers page. Slots
    # 5 and 6 are free in V11/V12, so this does not displace any existing item.
    nav_anchor = '''            }),new Array("qol_specials3","tw_clean",0,false,0,0,0,7,"TooltipBasic",{\n               "title":"More advanced towers →",\n               "text":"Open DWAARP and Battle-Mecha."\n            }),new Array("qol_specials","tw_clean",0,false,0,0,0,8,"TooltipBasic",{'''
    nav_replacement = '''            }),new Array("ultimate_kr1_towers","tw_clean",0,false,0,0,0,5,"TooltipBasic",{\n               "title":"Kingdom Rush towers →",\n               "text":"Open all eight original Kingdom Rush tier-4 branches."\n            }),new Array("qol_specials3","tw_clean",0,false,0,0,0,7,"TooltipBasic",{\n               "title":"More advanced towers →",\n               "text":"Open DWAARP and Battle-Mecha."\n            }),new Array("qol_specials","tw_clean",0,false,0,0,0,8,"TooltipBasic",{'''
    text = replace_once(text, nav_anchor, nav_replacement, "Ultimate tower page navigation")

    # Insert the reflection-based constructor beside the existing placement
    # helper. Constructor fallbacks are intentionally runtime-safe; final tower
    # probe verifies which signature is actually selected after rebind.
    helper_anchor = '''      private function qolPlaceSpecial(param1:§_-5u§) : void\n      {\n         this.cRoot.entities.addChild(param1);\n         this.cRoot.towers[param1] = param1;\n         this.destroyThis();\n      }\n      \n'''
    helper = helper_anchor + '''      private function ultimatePlaceKR1Tower(param1:String) : void\n      {\n         var towerClass:Class = null;\n         var candidate:Object = null;\n         var tower:§_-5u§ = null;\n         var invested:int = 0;\n         try\n         {\n            towerClass = Class(flash.utils.getDefinitionByName(param1));\n         }\n         catch(errorLookup:Error)\n         {\n            return;\n         }\n         try\n         {\n            candidate = new towerClass(this.x,this.y + this.yAdjust,this.§_-EV§,0,this.canBuildBarracks);\n         }\n         catch(errorFive:Error)\n         {\n            try\n            {\n               candidate = new towerClass(this.x,this.y + this.yAdjust,this.§_-EV§,0);\n            }\n            catch(errorFour:Error)\n            {\n               try\n               {\n                  candidate = new towerClass(this.x,this.y + this.yAdjust,this.§_-EV§);\n               }\n               catch(errorThree:Error)\n               {\n                  return;\n               }\n            }\n         }\n         if(!(candidate is §_-5u§))\n         {\n            return;\n         }\n         tower = §_-5u§(candidate);\n         if("§_-6f§" in candidate)\n         {\n            invested = Math.max(0,int(candidate["§_-6f§"]));\n         }\n         if(invested > this.cRoot.cash)\n         {\n            return;\n         }\n         if(invested > 0)\n         {\n            this.cRoot.updateCash(-invested);\n         }\n         this.qolPlaceSpecial(tower);\n      }\n      \n'''
    text = replace_once(text, helper_anchor, helper, "KR1 reflection placement helper")

    entries = []
    for idx, (action, _cls, icon, title) in enumerate(KR1_TOWERS, start=1):
        entries.append(menu_entry(action, icon, title, idx))
    page = ','.join(entries)
    page_block = f'''         if(param1 == "ultimate_kr1_towers")\n         {{\n            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array({page}));\n            this.cRoot.quickMenu.show(this.cRoot.§else const native§);\n            return;\n         }}\n'''

    action_blocks = ''.join(
        f'''         if(param1 == "{action}")\n         {{\n            this.ultimatePlaceKR1Tower("{cls}");\n            return;\n         }}\n'''
        for action, cls, _icon, _title in KR1_TOWERS
    )

    action_anchor = '''         if(param1 == "qol_dwarf")\n         {'''
    text = replace_once(
        text,
        action_anchor,
        page_block + action_blocks + action_anchor,
        "KR1 page and placement actions",
    )
    return text, {"already_patched": False, "tower_actions_added": len(KR1_TOWERS)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts", type=Path, help="FFDec scripts directory containing Level.as and TowerHolder.as")
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    level_path = args.scripts / "Level.as"
    holder_path = args.scripts / "TowerHolder.as"
    level, level_stats = patch_level(read(level_path))
    holder, holder_stats = patch_holder(read(holder_path))
    write(level_path, level)
    write(holder_path, holder)

    result = {
        "kr1_tier4_routes": len(KR1_TOWERS),
        "level": level_stats,
        "tower_holder": holder_stats,
        "actions": [x[0] for x in KR1_TOWERS],
        "runtime_classes": [x[1] for x in KR1_TOWERS],
        "policy": {
            "normal_frontiers_build_menu_unchanged": True,
            "kr1_classes_resolved_by_name": True,
            "no_compile_time_kr1_dependency": True,
            "direct_build_cost_from_imported_tower_invested_cost_when_available": True,
            "ability_rank_clipboard_support_complete": False,
            "four_way_tier3_upgrade_ui_complete": False,
        },
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
