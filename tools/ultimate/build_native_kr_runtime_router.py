#!/usr/bin/env python3
"""Route KR rows through the intact namespaced KR engine inside one SWF.

Unlike the historical semantic-Level bridge, this does not recompile any KR
ABC.  Frontiers creates the original KR Game controller dynamically, removes
its map, and asks that controller to launch its own native LevelN class.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


GAME_CLASS = "§_-BQ§.as"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def patch(text: str) -> str:
    if "ultimateNativeKRGame" in text:
        return text
    text = replace_once(
        text,
        "   import flash.events.*;\n",
        "   import flash.events.*;\n   import flash.display.DisplayObject;\n",
        "DisplayObject import",
    )
    text = replace_once(
        text,
        '      public var ultimateSourceLevel:int = 0;\n',
        '      public var ultimateSourceLevel:int = 0;\n      \n      public var ultimateNativeKRGame:Object;\n      \n      public var ultimateNativeKRMain:Object;\n',
        "native KR controller field",
    )
    old = '''      public function ultimateStartStage(param1:String, param2:String, param3:int, param4:int = 0, param5:Boolean = false, param6:String = "kr1") : void
      {
         var levelClass:Class = getDefinitionByName(param1) as Class;
         if(levelClass == null)
         {
            return;
         }
         this.ultimateStageId = param2;
         this.ultimateStageGame = param6;
         this.ultimateSourceLevel = param3;
         this.currentLevel = param3;
         this.addChildAt(new levelClass(this,param4,param5),0);
      }
'''
    new = '''      public function ultimateStartStage(param1:String, param2:String, param3:int, param4:int = 0, param5:Boolean = false, param6:String = "kr1") : void
      {
         this.ultimateStageId = param2;
         this.ultimateStageGame = param6;
         this.ultimateSourceLevel = param3;
         this.currentLevel = param3;
         if(param6 == "kr1")
         {
            this.ultimateNativeKRMain = new (getDefinitionByName("KR1__Defense") as Class)();
            this.ultimateNativeKRMain["_-5I"]();
            this.ultimateNativeKRMain["_-GL"]();
            this.ultimateNativeKRMain["_-1s"]();
            this.ultimateNativeKRMain["_-Q5"]();
            this.ultimateNativeKRGame = new (getDefinitionByName("KR1__Game") as Class)(this.ultimateNativeKRMain,"krultimate_slot1");
            this.ultimateNativeKRMain["addChildAt"](this.ultimateNativeKRGame,0);
            if(this.ultimateNativeKRGame["map"] != null)
            {
               this.ultimateNativeKRGame["_-Ax"]();
            }
            this.ultimateNativeKRGame["startLevel"](param3,param4);
            this.addChild(this.ultimateNativeKRMain as DisplayObject);
            this.addEventListener(Event.ENTER_FRAME,this.ultimateMonitorNativeKR);
            return;
         }
         var levelClass:Class = getDefinitionByName(param1) as Class;
         if(levelClass != null)
         {
            this.addChildAt(new levelClass(this,param4,param5),0);
         }
      }

      private function ultimateMonitorNativeKR(param1:Event) : void
      {
         if(this.ultimateNativeKRGame == null || this.ultimateNativeKRGame["map"] == null)
         {
            return;
         }
         this.removeEventListener(Event.ENTER_FRAME,this.ultimateMonitorNativeKR);
         if(this.ultimateNativeKRMain != null && (this.ultimateNativeKRMain as DisplayObject).parent == this)
         {
            this.removeChild(this.ultimateNativeKRMain as DisplayObject);
         }
         this.ultimateNativeKRGame = null;
         this.ultimateNativeKRMain = null;
         this.§var const finally§(null);
      }
'''
    return replace_once(text, old, new, "native KR stage router")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    path = args.scripts / GAME_CLASS
    text = path.read_text(encoding="utf-8-sig")
    patched = patch(text)
    path.write_text(patched, encoding="utf-8", newline="\n")
    report = {
        "class": GAME_CLASS.removesuffix(".as"),
        "native_kr_controller": "KR1__Game",
        "kr_abc_recompiled": False,
        "native_level_launch": True,
        "shared_map_return": True,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
