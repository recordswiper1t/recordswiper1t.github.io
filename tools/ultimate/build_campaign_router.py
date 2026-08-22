#!/usr/bin/env python3
"""Add stable Ultimate stage identity/routing to the enhanced Frontiers runtime.

Frontiers already instantiates `LevelN` dynamically in the game controller. The
combined runtime needs the same mechanism to accept namespaced KR1 classes
without reusing numeric level numbers as persistent identity.

Important compatibility rule: imported KR1 stages retain their original
`game.currentLevel` number because stage code may depend on it. KRF-only base
Level branches that cast to native `Level1` are therefore guarded by
`ultimateStageGame != "kr1"`.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


KRF_MAIN_IDS = [
    "krf-hammerhold",
    "krf-sandhawk-hamlet",
    "krf-sape-oasis",
    "krf-dunes-of-despair",
    "krf-buccaneer-s-den",
    "krf-the-gates-of-nazeru",
    "krf-crimson-valley",
    "krf-snapvine-bridge",
    "krf-lost-jungle",
    "krf-ma-qwa-urqu",
    "krf-temple-of-saqra",
    "krf-the-underpass",
    "krf-beresad-s-lair",
    "krf-the-dark-descent",
    "krf-emberspike-depths",
]


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


def patch_game(text: str) -> tuple[str, dict]:
    if "public var ultimateStageId:String" in text:
        return text, {"already_patched": True}

    field_anchor = "      public var currentLevel:int;\n"
    fields = field_anchor + '''      \n      public var ultimateStageId:String = "";\n      \n      public var ultimateStageGame:String = "krf";\n      \n      public var ultimateSourceLevel:int = 0;\n'''
    text = replace_once(text, field_anchor, fields, "Ultimate stage identity fields")

    legacy_tail = '''         this.addChildAt(new _loc19_(this,param2,param3),0);\n         this.currentLevel = param1;\n      }\n'''
    legacy_new = '''         this.addChildAt(new _loc19_(this,param2,param3),0);\n         this.currentLevel = param1;\n         this.ultimateSourceLevel = param1;\n         this.ultimateStageGame = "krf";\n         this.ultimateStageId = this.ultimateKrfMainStageId(param1);\n      }\n'''
    text = replace_once(text, legacy_tail, legacy_new, "legacy KRF stage identity")

    insert_anchor = '''      public function §var const finally§(param1:*) : void\n'''
    cases = "\n".join(
        f'''            case {idx}:\n               return "{stage_id}";'''
        for idx, stage_id in enumerate(KRF_MAIN_IDS, 1)
    )
    methods = f'''      public function ultimateStartStage(param1:String, param2:String, param3:int, param4:int = 0, param5:Boolean = false, param6:String = "kr1") : void\n      {{\n         var levelClass:Class = getDefinitionByName(param1) as Class;\n         if(levelClass == null)\n         {{\n            return;\n         }}\n         this.ultimateStageId = param2;\n         this.ultimateStageGame = param6;\n         this.ultimateSourceLevel = param3;\n         this.currentLevel = param3;\n         this.addChildAt(new levelClass(this,param4,param5),0);\n      }}\n      \n      public function ultimateKrfMainStageId(param1:int) : String\n      {{\n         switch(param1)\n         {{\n{cases}\n            default:\n               return "krf-level-" + param1;\n         }}\n      }}\n      \n'''
    text = replace_once(text, insert_anchor, methods + insert_anchor, "Ultimate string stage router")
    return text, {"already_patched": False, "krf_main_ids": len(KRF_MAIN_IDS)}


def patch_level(text: str) -> tuple[str, dict]:
    changes = 0

    old = "         if(this.game.currentLevel == 1)\n"
    new = '         if(this.game.ultimateStageGame != "kr1" && this.game.currentLevel == 1)\n'
    if old in text:
        text = replace_once(text, old, new, "KRF Level1 tutorial guard A")
        changes += 1

    old = "         if(this.game.currentLevel == 1 && this.§_-g3§ == 3)\n"
    new = '         if(this.game.ultimateStageGame != "kr1" && this.game.currentLevel == 1 && this.§_-g3§ == 3)\n'
    if old in text:
        text = replace_once(text, old, new, "KRF Level1 tutorial guard B")
        changes += 1

    old = "               switch(this.game.currentLevel)\n"
    new = '               switch(this.game.ultimateStageGame == "kr1" ? 0 : this.game.currentLevel)\n'
    if old in text:
        text = replace_once(text, old, new, "Frontiers dragon map-position guard")
        changes += 1

    v11_key = '''      private function qolTimeAttackKey() : String\n      {\n         return getQualifiedClassName(this) + ":" + String(this.mode);\n      }\n'''
    v12_key = '''      private function qolTimeAttackKey() : String\n      {\n         var key:String = getQualifiedClassName(this) + ":" + String(this.mode);\n         if(this is Level15 && Level15.qolV12PostBossActive)\n         {\n            key += ":postboss";\n         }\n         return key;\n      }\n'''
    stable_v11 = '''      private function qolTimeAttackKey() : String\n      {\n         var stageKey:String = this.game != null && this.game.ultimateStageId != "" ? this.game.ultimateStageId : getQualifiedClassName(this);\n         return stageKey + ":" + String(this.mode);\n      }\n'''
    stable_v12 = '''      private function qolTimeAttackKey() : String\n      {\n         var stageKey:String = this.game != null && this.game.ultimateStageId != "" ? this.game.ultimateStageId : getQualifiedClassName(this);\n         var key:String = stageKey + ":" + String(this.mode);\n         if(this is Level15 && Level15.qolV12PostBossActive)\n         {\n            key += ":postboss";\n         }\n         return key;\n      }\n'''
    if v12_key in text:
        text = replace_once(text, v12_key, stable_v12, "stable V12 Time Attack stage key")
        changes += 1
    elif v11_key in text:
        text = replace_once(text, v11_key, stable_v11, "stable V11 Time Attack stage key")
        changes += 1
    elif "this.game.ultimateStageId" not in text:
        raise SystemExit("stable Time Attack key: unrecognised enhanced runtime function shape")

    return text, {"guard_or_key_changes": changes}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    game_path = args.scripts / "§_-BQ§.as"
    level_path = args.scripts / "Level.as"
    game, game_stats = patch_game(read(game_path))
    level, level_stats = patch_level(read(level_path))
    write(game_path, game)
    write(level_path, level)

    result = {
        "game_controller": "§_-BQ§",
        "game": game_stats,
        "level": level_stats,
        "stable_stage_id_field": "ultimateStageId",
        "stage_game_field": "ultimateStageGame",
        "source_level_field": "ultimateSourceLevel",
        "string_router": "ultimateStartStage",
        "policy": {
            "kr1_currentLevel_preserved": True,
            "frontiers_level1_casts_guarded": True,
            "frontiers_dragon_special_offsets_disabled_on_kr1": True,
            "time_attack_key_uses_stable_stage_id": True,
            "v12_last_rift_postboss_key_preserved": True,
        },
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
