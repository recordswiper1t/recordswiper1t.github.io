#!/usr/bin/env python3
"""Add an additive Ultimate campaign selector to the Frontiers world map.

The normal Frontiers map/progression UI remains untouched. A small ULTIMATE
button opens a paged overlay containing every structurally source-ready stage:
19 KR1 publisher-Flash levels and all 15 Frontiers Flash campaign levels.
Blocked later/post-campaign content remains tracked by content_manifest and is
shown as a count, but is not made launchable until real content exists.

The selector calls §_-BQ§.ultimateStartStage(), added by build_campaign_router,
using stable stage IDs plus string runtime class identities. No compile-time
reference to a KR1 class is introduced here.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from campaign_registry import routes, validate as validate_routes


MAP_CLASS = "§class const for§.as"
PAGE_SIZE = 7


def ready_stage_rows() -> list[dict]:
    validate_routes()
    rows = []
    for route in routes(include_custom=False):
        if not route.source_ready or route.kind == "endless":
            continue
        if route.runtime_class is None:
            continue
        source_level = 0
        if route.runtime_class.startswith("KR1__Level"):
            source_level = int(route.runtime_class.removeprefix("KR1__Level"))
        elif route.runtime_class.startswith("Level"):
            source_level = int(route.runtime_class.removeprefix("Level"))
        rows.append({
            "id": route.stage_id,
            "game": route.game,
            "title": route.title,
            "kind": route.kind,
            "runtime_class": route.runtime_class,
            "source_level": source_level,
        })
    return rows


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


def as3_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def patch_map(text: str, stage_rows: list[dict]) -> tuple[str, dict]:
    if "private var ultimateCampaignButton:Sprite" in text:
        return text, {"already_patched": True, "source_ready_stages": len(stage_rows)}

    import_anchor = "   import flash.geom.*;\n"
    text = replace_once(text, import_anchor, import_anchor + "   import flash.text.*;\n", "campaign selector text imports")

    field_anchor = "      private var §extends final§:§const for while§;\n"
    fields = field_anchor + '''      \n      private var ultimateCampaignButton:Sprite;\n      \n      private var ultimateCampaignPanel:Sprite;\n      \n      private var ultimateCampaignPage:int = 0;\n      \n      private var ultimateCampaignRoutes:Array;\n'''
    text = replace_once(text, field_anchor, fields, "campaign selector state")

    ctor_anchor = "         this.§finally for catch§();\n      }\n"
    ctor_new = "         this.§finally for catch§();\n         this.ultimateInstallCampaignButton();\n      }\n"
    text = replace_once(text, ctor_anchor, ctor_new, "campaign selector install")

    route_literals = []
    for row in stage_rows:
        route_literals.append(
            'new Array("{id}","{game}","{title}","{runtime}",{level})'.format(
                id=as3_string(row["id"]),
                game=as3_string(row["game"]),
                title=as3_string(row["title"]),
                runtime=as3_string(row["runtime_class"]),
                level=row["source_level"],
            )
        )
    routes_as3 = ",\n            ".join(route_literals)
    blocked_count = 51 - len(stage_rows)

    method_anchor = '''      public function §while const switch§(param1:int, param2:int) : void\n'''
    methods = f'''      private function ultimateMakeText(param1:String, param2:Number, param3:Number, param4:Number, param5:Number, param6:int = 15) : TextField\n      {{\n         var t:TextField = new TextField();\n         t.defaultTextFormat = new TextFormat("_sans",param6,16777215,true);\n         t.text = param1;\n         t.x = param2;\n         t.y = param3;\n         t.width = param4;\n         t.height = param5;\n         t.selectable = false;\n         t.mouseEnabled = false;\n         return t;\n      }}\n      \n      private function ultimateMakeButton(param1:String, param2:Number, param3:Number, param4:Number, param5:Number, param6:String) : Sprite\n      {{\n         var button:Sprite = new Sprite();\n         button.name = param6;\n         button.x = param2;\n         button.y = param3;\n         button.graphics.beginFill(2236962,0.96);\n         button.graphics.lineStyle(1,13421772,0.9);\n         button.graphics.drawRoundRect(0,0,param4,param5,10,10);\n         button.graphics.endFill();\n         button.addChild(this.ultimateMakeText(param1,10,6,param4 - 20,param5 - 8,14));\n         button.buttonMode = true;\n         button.mouseChildren = false;\n         button.addEventListener(MouseEvent.CLICK,this.ultimateCampaignClick,false,0,true);\n         return button;\n      }}\n      \n      private function ultimateInstallCampaignButton() : void\n      {{\n         if(this.ultimateCampaignButton != null)\n         {{\n            return;\n         }}\n         this.ultimateCampaignRoutes = new Array(\n            {routes_as3}\n         );\n         this.ultimateCampaignButton = this.ultimateMakeButton("ULTIMATE",690,500,96,40,"ultimate_open");\n         this.§package const include§.addChild(this.ultimateCampaignButton);\n      }}\n      \n      private function ultimateCloseCampaignPanel() : void\n      {{\n         if(this.ultimateCampaignPanel != null && this.ultimateCampaignPanel.parent != null)\n         {{\n            this.ultimateCampaignPanel.parent.removeChild(this.ultimateCampaignPanel);\n         }}\n      }}\n      \n      private function ultimateRenderCampaignPanel() : void\n      {{\n         this.ultimateCloseCampaignPanel();\n         var panel:Sprite = new Sprite();\n         panel.x = 70;\n         panel.y = 38;\n         panel.graphics.beginFill(1118481,0.98);\n         panel.graphics.lineStyle(2,13983051,0.9);\n         panel.graphics.drawRoundRect(0,0,660,520,18,18);\n         panel.graphics.endFill();\n         this.ultimateCampaignPanel = panel;\n         this.addChild(panel);\n         var pages:int = Math.ceil(this.ultimateCampaignRoutes.length / {PAGE_SIZE});\n         this.ultimateCampaignPage = Math.max(0,Math.min(pages - 1,this.ultimateCampaignPage));\n         panel.addChild(this.ultimateMakeText("KINGDOM RUSH ULTIMATE — READY STAGES " + (this.ultimateCampaignPage + 1) + "/" + pages,22,14,610,30,20));\n         panel.addChild(this.ultimateMakeText("{len(stage_rows)} source-ready originals; {blocked_count} later/endless stages stay fail-closed until sourced or reconstructed.",22,43,615,24,12));\n         var first:int = this.ultimateCampaignPage * {PAGE_SIZE};\n         var i:int = 0;\n         while(i < {PAGE_SIZE} && first + i < this.ultimateCampaignRoutes.length)\n         {{\n            var row:Array = this.ultimateCampaignRoutes[first + i] as Array;\n            var prefix:String = String(row[1]) == "kr1" ? "KR  | " : "KRF | ";\n            panel.addChild(this.ultimateMakeButton(prefix + String(row[2]),22,78 + i * 51,616,42,"ultimate_stage_" + (first + i)));\n            i++;\n         }}\n         panel.addChild(this.ultimateMakeButton("← PAGE",22,455,150,42,"ultimate_prev"));\n         panel.addChild(this.ultimateMakeButton("CLOSE",255,455,150,42,"ultimate_close"));\n         panel.addChild(this.ultimateMakeButton("PAGE →",488,455,150,42,"ultimate_next"));\n      }}\n      \n      private function ultimateCampaignClick(param1:MouseEvent) : void\n      {{\n         var action:String = Sprite(param1.currentTarget).name;\n         if(action == "ultimate_open")\n         {{\n            this.ultimateCampaignPage = 0;\n            this.ultimateRenderCampaignPanel();\n            return;\n         }}\n         if(action == "ultimate_close")\n         {{\n            this.ultimateCloseCampaignPanel();\n            return;\n         }}\n         if(action == "ultimate_prev")\n         {{\n            this.ultimateCampaignPage--;\n            if(this.ultimateCampaignPage < 0)\n            {{\n               this.ultimateCampaignPage = Math.ceil(this.ultimateCampaignRoutes.length / {PAGE_SIZE}) - 1;\n            }}\n            this.ultimateRenderCampaignPanel();\n            return;\n         }}\n         if(action == "ultimate_next")\n         {{\n            this.ultimateCampaignPage = (this.ultimateCampaignPage + 1) % Math.ceil(this.ultimateCampaignRoutes.length / {PAGE_SIZE});\n            this.ultimateRenderCampaignPanel();\n            return;\n         }}\n         if(action.indexOf("ultimate_stage_") == 0)\n         {{\n            var index:int = int(action.substr(15));\n            if(index < 0 || index >= this.ultimateCampaignRoutes.length)\n            {{\n               return;\n            }}\n            var row:Array = this.ultimateCampaignRoutes[index] as Array;\n            this.ultimateCloseCampaignPanel();\n            this.game.ultimateStartStage(String(row[3]),String(row[0]),int(row[4]),0,false,String(row[1]));\n            this.game.§final throw§();\n         }}\n      }}\n      \n'''
    text = replace_once(text, method_anchor, methods + method_anchor, "campaign selector methods")
    return text, {
        "already_patched": False,
        "source_ready_stages": len(stage_rows),
        "pages": (len(stage_rows) + PAGE_SIZE - 1) // PAGE_SIZE,
        "page_size": PAGE_SIZE,
        "blocked_original_stages": blocked_count,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    stage_rows = ready_stage_rows()
    path = args.scripts / MAP_CLASS
    text, stats = patch_map(read(path), stage_rows)
    write(path, text)
    result = {
        "map_class": MAP_CLASS.removesuffix(".as"),
        "stats": stats,
        "ready_routes": stage_rows,
        "normal_frontiers_map_untouched": True,
        "requires_router_method": "§_-BQ§.ultimateStartStage",
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["stats"], indent=2))


if __name__ == "__main__":
    main()
