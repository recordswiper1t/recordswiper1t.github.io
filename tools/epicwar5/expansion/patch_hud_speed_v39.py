#!/usr/bin/env python3
"""Epic War 5 V3.9: native-looking compact slots and faster safe speeds."""

from __future__ import annotations

import argparse
from pathlib import Path


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"missing source: {path}")
    return path.read_text(encoding="utf-8-sig")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def block(text: str, start: str, end: str, replacement: str, label: str) -> str:
    a = text.find(start)
    b = text.find(end, a + 1)
    if a < 0 or b < 0:
        raise SystemExit(f"{label}: block anchors missing")
    return text[:a] + replacement + text[b:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("export_root", type=Path)
    args = parser.parse_args()
    game = args.export_root / "scripts" / "Game"

    control_path = game / "System" / "Battle" / "BattleControlPlayer.as"
    control = read(control_path)
    replacement = r'''      private function expansionCreateUnitClip(REF:*, INDEX:int) : *
      {
         var clip:MovieClip = new MovieClip();
         var selection:MovieClip = new MovieClip();
         var spawn:MovieClip = new MovieClip();
         var bar:MovieClip = new MovieClip();
         var slotLabel:TextField = new TextField();
         var unitName:TextField = new TextField();
         var total:TextField = new TextField();
         var layout:int = INDEX - 7;
         var diameter:Number = 46;
         var radius:Number = diameter * 0.5;
         clip.graphics.lineStyle(3,7697781,1);
         clip.graphics.beginFill(1250586,0.98);
         clip.graphics.drawCircle(radius,radius,radius - 2);
         clip.graphics.endFill();
         clip.graphics.lineStyle(1,14671839,0.75);
         clip.graphics.drawCircle(radius,radius,radius - 5);
         selection.graphics.lineStyle(3,16763904,1);
         selection.graphics.drawCircle(radius,radius,radius - 1);
         selection.visible = false;
         selection.mouseEnabled = false;
         slotLabel.defaultTextFormat = new TextFormat("_sans",10,16763904,true);
         slotLabel.text = String(INDEX);
         slotLabel.width = 18;
         slotLabel.height = 16;
         slotLabel.x = 4;
         slotLabel.y = 1;
         slotLabel.selectable = false;
         slotLabel.mouseEnabled = false;
         unitName.defaultTextFormat = new TextFormat("_sans",7,16777215,true);
         unitName.text = "LOCKED";
         unitName.width = 42;
         unitName.height = 15;
         unitName.x = 2;
         unitName.y = 15;
         unitName.selectable = false;
         unitName.mouseEnabled = false;
         total.defaultTextFormat = new TextFormat("_sans",8,14540253,true);
         total.text = "—";
         total.width = 40;
         total.height = 14;
         total.x = 3;
         total.y = 27;
         total.selectable = false;
         total.mouseEnabled = false;
         spawn.graphics.beginFill(3289650,1);
         spawn.graphics.drawRoundRect(0,0,30,4,3,3);
         spawn.graphics.endFill();
         bar.graphics.beginFill(5635925,1);
         bar.graphics.drawRoundRect(0,0,30,4,3,3);
         bar.graphics.endFill();
         spawn.x = 8;
         spawn.y = 39;
         spawn.addChild(bar);
         spawn.bar = bar;
         clip.addChild(selection);
         clip.addChild(slotLabel);
         clip.addChild(unitName);
         clip.addChild(total);
         clip.addChild(spawn);
         clip.select = selection;
         clip.iconLabel = slotLabel;
         clip.unitName = unitName;
         clip.total = total;
         clip.spawn = spawn;
         clip.expansionIcon = true;
         clip.expansionSlot = INDEX;
         clip.buttonMode = true;
         clip.mouseChildren = false;
         // A compact alternating crest: /\/\/\ .  It sits above the six
         // original portraits and stops before the wave/speed controls.
         clip.x = 232 + layout * 51;
         clip.y = layout % 2 == 0 ? 482 : 461;
         this.bSys.ui.addChild(clip);
         return clip;
      }

'''
    control = block(
        control,
        "      private function expansionCreateUnitClip",
        "      private function expansionInitUnits",
        replacement,
        "compact expansion slots",
    )
    write(control_path, control)

    unit_path = game / "System" / "Battle" / "PlayerUnit.as"
    unit = read(unit_path)
    unit = once(
        unit,
        "               this.icoClip.unitName.text = this.name_id.toUpperCase();\n",
        "               this.icoClip.unitName.text = this.name_id.length > 7 ? this.name_id.substr(0,7).toUpperCase() : this.name_id.toUpperCase();\n",
        "short circular-slot unit label",
    )
    unit = unit.replace(
        'this.icoClip.total.text = "Slot " + this.icoClip.expansionSlot;',
        'this.icoClip.total.text = this.icoClip.expansionUnlocked ? "EMPTY" : "LOCKED";',
    )
    write(unit_path, unit)

    battle_path = game / "System" / "Battle" / "BattleSystem.as"
    battle = read(battle_path)
    battle = once(
        battle,
        "      private var sandboxStatus:TextField = null;\n",
        "      private var sandboxStatus:TextField = null;\n      \n      private var sandboxWinCommitted:Boolean = false;\n",
        "instant-win reentry guard",
    )
    battle = once(
        battle,
        '''      private function sandboxSpeedText() : String
      {
         return this.sandboxSpeedIndex == 0 ? "1x" : (this.sandboxSpeedIndex == 1 ? "2x" : "4x");
      }
''',
        '''      private function sandboxSpeedText() : String
      {
         return this.sandboxSpeedIndex == 0 ? "1x" : (this.sandboxSpeedIndex == 1 ? "2x" : (this.sandboxSpeedIndex == 2 ? "4x" : (this.sandboxSpeedIndex == 3 ? "6x" : "8x")));
      }

      private function sandboxApplySpeed(LOAD:int = -1) : void
      {
         var rate:int = this.sandboxSpeedIndex == 0 ? 24 : (this.sandboxSpeedIndex == 1 ? 48 : (this.sandboxSpeedIndex == 2 ? 96 : (this.sandboxSpeedIndex == 3 ? 144 : 192)));
         if(LOAD >= 320) rate = Math.min(rate,48);
         else if(LOAD >= 225) rate = Math.min(rate,72);
         else if(LOAD >= 165) rate = Math.min(rate,96);
         this.mGF.stageRoot.stage.frameRate = rate;
         if(rate > 24 || LOAD >= 165)
         {
            this.mGF.stageRoot.stage.quality = "low";
            this._adaptive_quality_low = true;
         }
      }
''',
        "five Epic War speed tiers",
    )
    battle = once(
        battle,
        '''      private function sandboxCycleSpeed() : void
      {
         this.sandboxSpeedIndex = (this.sandboxSpeedIndex + 1) % 3;
         this.mGF.stageRoot.stage.frameRate = this.sandboxSpeedIndex == 0 ? 24 : (this.sandboxSpeedIndex == 1 ? 48 : 96);
         this.sandboxRefresh("Battle speed " + this.sandboxSpeedText());
      }
''',
        '''      private function sandboxCycleSpeed() : void
      {
         this.sandboxSpeedIndex = (this.sandboxSpeedIndex + 1) % 5;
         this.sandboxApplySpeed();
         this.sandboxRefresh("Battle speed " + this.sandboxSpeedText() + " (adaptive under load)");
      }
''',
        "cycle Epic War speeds",
    )
    battle = once(
        battle,
        "         var load:int = int(this.mGF.contUNIT.numChildren + this.mGF.contEFFECT.numChildren + this.mGF.contFILTER.numChildren + this.mGF.contINFO.numChildren);\n",
        "         var load:int = int(this.mGF.contUNIT.numChildren + this.mGF.contEFFECT.numChildren + this.mGF.contFILTER.numChildren + this.mGF.contINFO.numChildren);\n         if(this.sandboxSpeedIndex > 0) this.sandboxApplySpeed(load);\n",
        "adaptive requested speed application",
    )
    battle = once(
        battle,
        '''      private function sandboxInstantWin() : void
      {
         this.battle_result = "win";
         this.battle_boss_kill = Math.max(this.battle_boss_kill,1);
         this.sandboxRefresh("Battle marked won");
      }
''',
        '''      private function sandboxInstantWin() : void
      {
         if(this.sandboxWinCommitted)
         {
            return;
         }
         this.sandboxWinCommitted = true;
         this.battle_result = "win";
         this.battle_boss_kill = Math.max(this.battle_boss_kill,1);
         this.sandboxRefresh("Victory complete");
         if(this.playerMgr != null)
         {
            this.playerMgr.removeControl();
            this.playerMgr.setStateControl("");
         }
         this.showBattleResult();
      }
''',
        "truly immediate Epic War victory result",
    )
    write(battle_path, battle)

    for path, needles in {
        control_path: ["drawCircle(radius,radius", "clip.x = 232 + layout * 51", "layout % 2 == 0 ? 482 : 461"],
        unit_path: ["this.name_id.substr(0,7)", '"EMPTY" : "LOCKED"'],
        battle_path: ["sandboxApplySpeed", "% 5", '"6x"', '"8x"', "sandboxWinCommitted", 'this.showBattleResult();'],
    }.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path.name}")
    print("Epic War 5 V3.9 compact crest HUD + 1x/2x/4x/6x/8x adaptive speed applied")


if __name__ == "__main__":
    main()
