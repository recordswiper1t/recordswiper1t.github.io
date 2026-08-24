#!/usr/bin/env python3
"""Repair the six expansion battle controllers' synthetic HUD clips.

V3 created those clips from getQualifiedClassName(unit1). Timeline children in
the original battle HUD have no linkage class, so that expression resolves to
plain flash.display.MovieClip. The resulting instance has no ``select`` child
and PlayerUnit aborts battle initialization on its first ``visible`` access.

V3.7 builds the small second HUD row explicitly and teaches PlayerUnit how to
render an expansion slot without relying on a timeline icon frame.
"""

from pathlib import Path
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: patch_battle_unit_ui_v37.py <ffdec-export-root>")

root = Path(sys.argv[1]) / "scripts" / "Game" / "System" / "Battle"
control_path = root / "BattleControlPlayer.as"
unit_path = root / "PlayerUnit.as"

control = control_path.read_text(encoding="utf-8-sig")
unit = unit_path.read_text(encoding="utf-8-sig")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, got {count}")
    return text.replace(old, new, 1)


control = replace_once(
    control,
    """   import flash.events.MouseEvent;
   import flash.utils.getDefinitionByName;
   import flash.utils.getQualifiedClassName;
""",
    """   import flash.display.MovieClip;
   import flash.events.MouseEvent;
   import flash.text.TextField;
   import flash.text.TextFormat;
""",
    "battle HUD imports",
)

start = control.index("      private function expansionInitUnits() : void")
end = control.index("      private function expansionDestroyUnits() : void", start)
replacement = """      private function expansionCreateUnitClip(REF:*, INDEX:int) : *
      {
         var clip:MovieClip = new MovieClip();
         var selection:MovieClip = new MovieClip();
         var spawn:MovieClip = new MovieClip();
         var bar:MovieClip = new MovieClip();
         var iconLabel:TextField = new TextField();
         var total:TextField = new TextField();
         var format:TextFormat = new TextFormat("_sans",9,16777215,true);
         var width:Number = Math.max(42,REF.width);
         var height:Number = Math.max(38,REF.height);
         clip.graphics.lineStyle(1,13019749,1);
         clip.graphics.beginFill(1118481,0.92);
         clip.graphics.drawRoundRect(0,0,width,height,5,5);
         clip.graphics.endFill();
         selection.graphics.lineStyle(2,16763904,1);
         selection.graphics.drawRoundRect(1,1,width - 2,height - 2,5,5);
         selection.visible = false;
         selection.mouseEnabled = false;
         iconLabel.defaultTextFormat = format;
         iconLabel.width = width;
         iconLabel.height = 18;
         iconLabel.x = 0;
         iconLabel.y = 3;
         iconLabel.selectable = false;
         iconLabel.mouseEnabled = false;
         total.defaultTextFormat = new TextFormat("_sans",8,16777215,false);
         total.width = width;
         total.height = 16;
         total.x = 2;
         total.y = height - 18;
         total.selectable = false;
         total.mouseEnabled = false;
         spawn.graphics.beginFill(3355443,1);
         spawn.graphics.drawRect(2,0,width - 4,3);
         spawn.graphics.endFill();
         bar.graphics.beginFill(5635925,1);
         bar.graphics.drawRect(2,0,width - 4,3);
         bar.graphics.endFill();
         spawn.y = height - 4;
         spawn.addChild(bar);
         spawn.bar = bar;
         clip.addChild(selection);
         clip.addChild(iconLabel);
         clip.addChild(total);
         clip.addChild(spawn);
         clip.select = selection;
         clip.iconLabel = iconLabel;
         clip.total = total;
         clip.spawn = spawn;
         clip.expansionIcon = true;
         clip.buttonMode = true;
         clip.mouseChildren = false;
         clip.x = REF.x;
         clip.y = REF.y - height - 3;
         REF.parent.addChild(clip);
         return clip;
      }

      private function expansionInitUnits() : void
      {
         this.expansionUnits = [];
         this.expansionUnitClips = [];
         var refs:Array = [this.bSys.ui.unit1,this.bSys.ui.unit2,this.bSys.ui.unit3,this.bSys.ui.unit4,this.bSys.ui.unit5,this.bSys.ui.unit6];
         var i:int = 0;
         var slot:int = 0;
         var clip:* = null;
         var unit:* = null;
         var id:int = 0;
         for(i = 0; i < 6; i++)
         {
            slot = i + 7;
            clip = this.expansionCreateUnitClip(refs[i],slot);
            this.expansionUnitClips.push(clip);
            id = slot <= this.mGF.datMgr.expansionArmySlotsUnlocked() ? this.mGF.datMgr.expansionGetUnitEquip(slot) : 0;
            unit = new PlayerUnit(this.mGF,this.bSys,clip,"unit",id,slot + 1);
            this.expansionUnits.push(unit);
         }
      }

"""
control = control[:start] + replacement + control[end:]

unit = replace_once(
    unit,
    """            this.icoClip.icon.gotoAndStop(this.id);
""",
    """            if(this.icoClip.hasOwnProperty("expansionIcon"))
            {
               this.icoClip.iconLabel.htmlText = "<p align='center'><b>" + String(this.id) + "</b></p>";
            }
            else
            {
               this.icoClip.icon.gotoAndStop(this.id);
            }
""",
    "expansion icon rendering",
)

control_path.write_text(control, encoding="utf-8", newline="\n")
unit_path.write_text(unit, encoding="utf-8", newline="\n")

for needle in (
    "private function expansionCreateUnitClip",
    "clip.expansionIcon = true",
    "clip = this.expansionCreateUnitClip(refs[i],slot)",
):
    if needle not in control:
        raise SystemExit(f"missing BattleControlPlayer marker: {needle}")

for needle in (
    'this.icoClip.hasOwnProperty("expansionIcon")',
    "this.icoClip.iconLabel.htmlText",
    "this.icoClip.icon.gotoAndStop(this.id)",
):
    if needle not in unit:
        raise SystemExit(f"missing PlayerUnit marker: {needle}")

print("Epic War 5 V3.7 explicit expansion HUD clips applied")
