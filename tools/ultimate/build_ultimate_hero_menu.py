#!/usr/bin/env python3
"""Add the first combined KR1/KRF hero selector to enhanced Frontiers.

This is intentionally additive and fail-safe:
- all existing V11/V12 Frontiers hero behavior remains intact;
- nine heroes verified in the KR1 publisher Flash build are added as optional
  extra heroes, default OFF so an unmerged Frontiers SWF behaves exactly as
  before;
- KR1 classes are resolved with getDefinitionByName, so the patch compiles
  before the namespaced classes are physically merged;
- the four KR1 heroes absent from the publisher Flash source stay in the locked
  roster but are not falsely exposed as playable.

A later gate can promote any KR1 hero to the primary/persistent hero slot after
its movement/combat/skill compatibility is runtime-tested.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


KRF_EXISTING = [
    ("alric", "Alric"),
    ("mirage", "Mirage"),
    ("captain", "Blackthorne"),
    ("cronan", "Cronan"),
    ("shatra", "Sha'tra"),
    ("grawl", "Grawl"),
    ("nivus", "Nivus"),
    ("dierdre", "Dierdre"),
    ("ashbite", "Ashbite"),
    ("rurin", "Rurin Longbeard"),
]

KR1_READY = [
    ("kr1_gerald", "Gerald", "KR1__SoldierHeroGerald"),
    ("kr1_alleria", "Alleria", "KR1__SoldierHeroAlleria"),
    ("kr1_malik", "Malik", "KR1__SoldierHeroMalik"),
    ("kr1_bolin", "Bolin", "KR1__SoldierHeroBolin"),
    ("kr1_magnus", "Magnus", "KR1__SoldierHeroMagnus"),
    ("kr1_ignus", "Ignus", "KR1__SoldierHeroIgnus"),
    ("kr1_denas", "King Denas", "KR1__SoldierHeroDenas"),
    ("kr1_elora", "Elora", "KR1__SoldierHeroFrost"),
    ("kr1_ingvar", "Ingvar", "KR1__SoldierHeroViking"),
]

PAGE_SIZE = 8


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"missing source: {path}")
    return path.read_text(encoding="utf-8-sig")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def replace_function(text: str, signature: str, replacement: str, label: str) -> str:
    start = text.find(signature)
    if start < 0:
        raise SystemExit(f"{label}: signature missing")
    brace = text.find("{", start)
    depth = 0
    i = brace
    in_string = False
    escape = False
    quote = ""
    while i < len(text):
        c = text[i]
        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                quote = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[:start] + replacement + text[i + 1:]
        i += 1
    raise SystemExit(f"{label}: unterminated function")


def patch(text: str) -> tuple[str, dict]:
    if "private function ultimateMakeKR1Hero" in text:
        return text, {"already_patched": True, "kr1_ready_heroes": len(KR1_READY)}

    field_anchor = "      private var qolEnemyPage:int = 0;\n"
    text = replace_once(
        text,
        field_anchor,
        field_anchor + "      \n      private var qolHeroPage:int = 0;\n",
        "hero page state",
    )

    all_names = KRF_EXISTING + [(k, title) for k, title, _cls in KR1_READY]
    as3_names = ",".join(f'["{key}","{title.replace(chr(34), chr(92)+chr(34))}"]' for key, title in all_names)

    page2_signature = "      private function qolRenderSettings() : void\n"
    # Replace only the page-2 body inside the existing renderer; all other
    # sandbox pages remain untouched.
    old_page = '''         else if(this.qolSettingsPage == 2)\n         {\n            this.qolEnsureHeroSelection();\n            this.qolSettings.addChild(this.qolLabel("HEROES",28,16,22));\n            var heroNames:Array = [["alric","Alric"],["mirage","Mirage"],["captain","Blackthorne"],["cronan","Cronan"],["shatra","Sha\\'tra"],["grawl","Grawl"],["nivus","Nivus"],["dierdre","Dierdre"],["ashbite","Ashbite"],["rurin","Rurin Longbeard"]];\n            var hi:int = 0;\n            while(hi < heroNames.length)\n            {\n               this.qolSettings.addChild(this.qolButton(this.qolHeroLabel(heroNames[hi][0],heroNames[hi][1]),hi % 2 == 0 ? 28 : 302,72 + int(hi / 2) * 47,250,"hero_" + heroNames[hi][0]));\n               hi++;\n            }\n            var allHeroesOn:Boolean = this.qolAllHeroesEnabled();\n            this.qolSettings.addChild(this.qolButton(allHeroesOn ? "TURN ALL HEROES OFF" : "TURN ALL HEROES ON",28,320,524,"heroes_all"));\n            this.qolSettings.addChild(this.qolButton("REMOVE ALL HEROES NOW",28,374,250,"heroes_remove"));\n            this.qolSettings.addChild(this.qolButton("← Dashboard",302,374,250,"page_main"));\n         }\n'''
    new_page = f'''         else if(this.qolSettingsPage == 2)\n         {{\n            this.qolEnsureHeroSelection();\n            var heroNames:Array = [{as3_names}];\n            var heroPages:int = Math.ceil(heroNames.length / {PAGE_SIZE});\n            this.qolHeroPage = Math.max(0,Math.min(heroPages - 1,this.qolHeroPage));\n            this.qolSettings.addChild(this.qolLabel("HEROES — PAGE " + (this.qolHeroPage + 1) + "/" + heroPages,28,16,22));\n            var heroFirst:int = this.qolHeroPage * {PAGE_SIZE};\n            var hi:int = 0;\n            while(hi < {PAGE_SIZE} && heroFirst + hi < heroNames.length)\n            {{\n               var heroRow:Array = heroNames[heroFirst + hi] as Array;\n               this.qolSettings.addChild(this.qolButton(this.qolHeroLabel(String(heroRow[0]),String(heroRow[1])),hi % 2 == 0 ? 28 : 302,68 + int(hi / 2) * 47,250,"hero_" + String(heroRow[0])));\n               hi++;\n            }}\n            this.qolSettings.addChild(this.qolButton("← Hero page",28,264,150,"hero_page_prev"));\n            this.qolSettings.addChild(this.qolButton("Hero page →",402,264,150,"hero_page_next"));\n            var allHeroesOn:Boolean = this.qolAllHeroesEnabled();\n            this.qolSettings.addChild(this.qolButton(allHeroesOn ? "TURN ALL HEROES OFF" : "TURN ALL HEROES ON",28,318,524,"heroes_all"));\n            this.qolSettings.addChild(this.qolLabel("KR1 publisher heroes default OFF; Hacksaw / Oni / Thor / Ten'Shí await later source.",28,369,13));\n            this.qolSettings.addChild(this.qolButton("REMOVE ALL HEROES NOW",28,400,250,"heroes_remove"));\n            this.qolSettings.addChild(this.qolButton("← Dashboard",302,400,250,"page_main"));\n         }}\n'''
    if old_page not in text:
        raise SystemExit("hero settings page: expected V11/V12 categorized UI shape")
    text = text.replace(old_page, new_page, 1)

    click_anchor = '''         else if(action.indexOf("hero_") == 0) this.qolToggleHero(action.substr(5));\n'''
    if click_anchor not in text:
        # Some V11 exports use braces rather than the compact V11 ui_perf shape.
        click_anchor = '''         else if(action.indexOf("hero_") == 0)\n         {\n            this.qolToggleHero(action.substr(5));\n         }\n'''
    click_new = click_anchor + f'''         else if(action == "hero_page_prev")\n         {{\n            this.qolHeroPage = (this.qolHeroPage + Math.ceil({len(all_names)} / {PAGE_SIZE}) - 1) % Math.ceil({len(all_names)} / {PAGE_SIZE});\n         }}\n         else if(action == "hero_page_next")\n         {{\n            this.qolHeroPage = (this.qolHeroPage + 1) % Math.ceil({len(all_names)} / {PAGE_SIZE});\n         }}\n'''
    text = replace_once(text, click_anchor, click_new, "hero page click actions")

    make_signature = "      private function qolMakeHero(param1:String, param2:int) : §dynamic const class§\n"
    class_cases = "\n".join(
        f'''            case "{key}":\n               return this.ultimateMakeKR1Hero("{cls}",p);'''
        for key, _title, cls in KR1_READY
    )
    helper_and_factory = f'''      private function ultimateMakeKR1Hero(param1:String, param2:Point) : §dynamic const class§\n      {{\n         var heroClass:Class = null;\n         var candidate:Object = null;\n         try\n         {{\n            heroClass = Class(getDefinitionByName(param1));\n         }}\n         catch(errorLookup:Error)\n         {{\n            return null;\n         }}\n         try\n         {{\n            candidate = new heroClass(param2,param2,null,param2);\n         }}\n         catch(errorFour:Error)\n         {{\n            try\n            {{\n               candidate = new heroClass(param2,param2,null);\n            }}\n            catch(errorThree:Error)\n            {{\n               try\n               {{\n                  candidate = new heroClass(param2,param2);\n               }}\n               catch(errorTwo:Error)\n               {{\n                  return null;\n               }}\n            }}\n         }}\n         if(candidate is §dynamic const class§)\n         {{\n            return §dynamic const class§(candidate);\n         }}\n         return null;\n      }}\n      \n      private function qolMakeHero(param1:String, param2:int) : §dynamic const class§\n      {{\n         var p:Point = new Point(this.§_-R4§[0].x + param2 % 3 * 28 - 28,this.§_-R4§[0].y + int(param2 / 3) * 28);\n         switch(param1)\n         {{\n            case "alric":\n               return new SoldierHeroAlric(p,p,null,p);\n            case "mirage":\n               return new SoldierHeroMirage(p,p,null,p);\n            case "captain":\n               return new SoldierHeroCaptain(p,p,null,p);\n            case "cronan":\n               return new SoldierHeroCronan(p,p,null,p);\n            case "shatra":\n               return new SoldierHeroAlien(p,p,null,p);\n            case "grawl":\n               return new §else const static§(p,p,null,p);\n            case "nivus":\n               return new SoldierHeroNivus(p,p,null,p);\n            case "dierdre":\n               return new SoldierHeroDierdre(p,p,null,p);\n            case "ashbite":\n               return new SoldierHeroDragon(p,p,null,p);\n            case "rurin":\n               return new §switch for super§(p,p,null,p);\n{class_cases}\n            default:\n               return null;\n         }}\n      }}\n'''
    text = replace_function(text, make_signature, helper_and_factory, "KR1 reflection hero factory")

    existing_roster = 'var roster:Array = ["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite","rurin"];'
    combined_keys = [key for key, _title in KRF_EXISTING] + [key for key, _title, _cls in KR1_READY]
    combined_roster = 'var roster:Array = [' + ",".join(f'"{k}"' for k in combined_keys) + '];'
    # This exact roster occurs in qolSpawnExtraHeroes and qolEnsureHeroSelection.
    if text.count(existing_roster) != 2:
        raise SystemExit(f"hero roster arrays: expected two anchors, found {text.count(existing_roster)}")
    text = text.replace(existing_roster, combined_roster, 1)

    # In selection initialization, keep legacy Frontiers defaults ON but add KR1
    # heroes OFF. Replacing the second roster wholesale would set all 19 ON.
    second_index = text.find(existing_roster)
    if second_index < 0:
        raise SystemExit("hero selection initialization roster anchor missing")
    ensure_block = '''var roster:Array = ["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite","rurin"];\n         for each(var heroName in roster)\n         {\n            Level.qolHeroEnabled[heroName] = true;\n         }'''
    ensure_new = '''var roster:Array = ["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite","rurin"];\n         for each(var heroName in roster)\n         {\n            Level.qolHeroEnabled[heroName] = true;\n         }\n         var kr1Roster:Array = [''' + ",".join(f'"{k}"' for k, _title, _cls in KR1_READY) + '''];\n         for each(heroName in kr1Roster)\n         {\n            Level.qolHeroEnabled[heroName] = false;\n         }'''
    text = replace_once(text, ensure_block, ensure_new, "KR1 hero defaults")

    return text, {
        "already_patched": False,
        "frontiers_existing_hero_toggles": len(KRF_EXISTING),
        "kr1_ready_hero_toggles": len(KR1_READY),
        "hero_toggle_total": len(all_names),
        "pages": (len(all_names) + PAGE_SIZE - 1) // PAGE_SIZE,
        "kr1_default_enabled": False,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    path = args.scripts / "Level.as"
    text, stats = patch(read(path))
    write(path, text)
    result = {
        "stats": stats,
        "kr1_ready": [
            {"key": key, "title": title, "runtime_class": cls}
            for key, title, cls in KR1_READY
        ],
        "later_or_missing_kr1": ["Hacksaw", "Oni", "Thor", "Ten'Shí"],
        "policy": {
            "existing_frontiers_behavior_preserved": True,
            "kr1_heroes_default_off": True,
            "kr1_classes_resolved_by_name": True,
            "primary_hero_persistence_not_yet_changed": True,
            "runtime_skill_compatibility_requires_merged_probe": True,
        },
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
