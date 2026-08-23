#!/usr/bin/env python3
"""Polish the Expansion V3.7 battle HUD and replace the debug sandbox overlay.

V3.8 keeps the wider battlefield view, moves slots 7-12 into an unclipped second
HUD row, gives empty/locked slots readable states, adds a compact clickable
sandbox palette, and gives sandbox-spawned armies real forward orders.
"""

from pathlib import Path
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: patch_ui_sandbox_v38.py <ffdec-export-root>")

root = Path(sys.argv[1]) / "scripts" / "Game"


def read(rel: str) -> str:
    path = root / rel
    if not path.is_file():
        raise SystemExit(f"missing source: {path}")
    return path.read_text(encoding="utf-8-sig")


def write(rel: str, text: str) -> None:
    (root / rel).write_text(text, encoding="utf-8", newline="\n")


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 match, got {count}")
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# 1. Twelve-slot battle HUD: render slots 7-12 in the UI's own coordinate
# system so timeline-parent masks cannot clip or stack them. Empty and locked
# slots stay visible and every equipped slot shows its actual unit name.
# ---------------------------------------------------------------------------
control = read("System/Battle/BattleControlPlayer.as")
control = once(
    control,
    "   import flash.display.MovieClip;\n",
    "   import flash.display.MovieClip;\n   import flash.geom.Point;\n",
    "BattleControlPlayer Point import",
)
start = control.index("      private function expansionCreateUnitClip")
end = control.index("      private function expansionInitUnits", start)
control = control[:start] + r'''      private function expansionCreateUnitClip(REF:*, INDEX:int) : *
      {
         var clip:MovieClip = new MovieClip();
         var selection:MovieClip = new MovieClip();
         var spawn:MovieClip = new MovieClip();
         var bar:MovieClip = new MovieClip();
         var slotLabel:TextField = new TextField();
         var unitName:TextField = new TextField();
         var total:TextField = new TextField();
         var point:Point = REF.localToGlobal(new Point(0,0));
         point = this.bSys.ui.globalToLocal(point);
         var width:Number = Math.max(58,Math.min(72,REF.width));
         var height:Number = 48;
         clip.graphics.lineStyle(1,13983051,0.95);
         clip.graphics.beginFill(1052688,0.96);
         clip.graphics.drawRoundRect(0,0,width,height,7,7);
         clip.graphics.endFill();
         selection.graphics.lineStyle(3,16763904,1);
         selection.graphics.drawRoundRect(1,1,width - 2,height - 2,7,7);
         selection.visible = false;
         selection.mouseEnabled = false;
         slotLabel.defaultTextFormat = new TextFormat("_sans",10,16763904,true);
         slotLabel.text = String(INDEX);
         slotLabel.width = 16;
         slotLabel.height = 18;
         slotLabel.x = 4;
         slotLabel.y = 2;
         slotLabel.selectable = false;
         slotLabel.mouseEnabled = false;
         unitName.defaultTextFormat = new TextFormat("_sans",9,16777215,true);
         unitName.text = "LOCKED";
         unitName.width = width - 20;
         unitName.height = 18;
         unitName.x = 19;
         unitName.y = 3;
         unitName.selectable = false;
         unitName.mouseEnabled = false;
         total.defaultTextFormat = new TextFormat("_sans",9,14540253,false);
         total.text = "Slot " + INDEX;
         total.width = width - 8;
         total.height = 16;
         total.x = 4;
         total.y = 22;
         total.selectable = false;
         total.mouseEnabled = false;
         spawn.graphics.beginFill(3355443,1);
         spawn.graphics.drawRect(4,0,width - 8,4);
         spawn.graphics.endFill();
         bar.graphics.beginFill(5635925,1);
         bar.graphics.drawRect(0,0,width - 8,4);
         bar.graphics.endFill();
         spawn.y = height - 7;
         spawn.x = 0;
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
         clip.x = point.x + (REF.width - width) * 0.5;
         clip.y = point.y - height - 6;
         this.bSys.ui.addChild(clip);
         return clip;
      }

''' + control[end:]
control = once(
    control,
    "            clip = this.expansionCreateUnitClip(refs[i],slot);\n            this.expansionUnitClips.push(clip);\n            id = int(slot <= this.mGF.datMgr.expansionArmySlotsUnlocked() ? this.mGF.datMgr.expansionGetUnitEquip(slot) : 0);\n",
    "            clip = this.expansionCreateUnitClip(refs[i],slot);\n            this.expansionUnitClips.push(clip);\n            clip.expansionUnlocked = slot <= this.mGF.datMgr.expansionArmySlotsUnlocked();\n            id = int(clip.expansionUnlocked ? this.mGF.datMgr.expansionGetUnitEquip(slot) : 0);\n",
    "expansion slot unlock state",
)
write("System/Battle/BattleControlPlayer.as", control)

unit = read("System/Battle/PlayerUnit.as")
unit = once(
    unit,
    "         this.icoClip.visible = false;\n         this.icoClip.select.visible = false;\n",
    "         this.icoClip.visible = false;\n         this.icoClip.select.visible = false;\n         if(this.icoClip.hasOwnProperty(\"expansionIcon\"))\n         {\n            this.icoClip.visible = true;\n         }\n",
    "expansion placeholder visibility",
)
unit = once(
    unit,
    '''            if(this.icoClip.hasOwnProperty("expansionIcon"))
            {
               this.icoClip.iconLabel.htmlText = "<p align=\\'center\\'><b>" + String(this.id) + "</b></p>";
            }
            else
            {
               this.icoClip.icon.gotoAndStop(this.id);
            }
''',
    '''            if(this.icoClip.hasOwnProperty("expansionIcon"))
            {
               this.icoClip.unitName.text = this.name_id.toUpperCase();
               this.icoClip.alpha = 1;
            }
            else
            {
               this.icoClip.icon.gotoAndStop(this.id);
            }
''',
    "expansion unit name",
)
unit = once(
    unit,
    '         trace("uI = " + UNITID + " uN = " + this.name_id + " uT = " + this.type);\n',
    '''         if(this.icoClip.hasOwnProperty("expansionIcon") && this.name_id == "")
         {
            this.icoClip.unitName.text = this.icoClip.expansionUnlocked ? "EMPTY" : "LOCKED";
            this.icoClip.total.text = "Slot " + this.icoClip.expansionSlot;
            this.icoClip.spawn.visible = false;
            this.icoClip.alpha = this.icoClip.expansionUnlocked ? 0.92 : 0.82;
         }
         trace("uI = " + UNITID + " uN = " + this.name_id + " uT = " + this.type);
''',
    "expansion empty state",
)
write("System/Battle/PlayerUnit.as", unit)


# ---------------------------------------------------------------------------
# 2. Sandbox army movement: make CharacterMgr return spawned clips, then issue
# explicit forward orders to the far side instead of stopping in midfield.
# ---------------------------------------------------------------------------
characters = read("System/GameObject/CharacterMgr.as")
characters = once(
    characters,
    '         clip.commandMove("ally",GROUP,X);\n      }\n      \n      public function createPlayerUnitNPC',
    '         clip.commandMove("ally",GROUP,X);\n         return clip;\n      }\n      \n      public function createPlayerUnitNPC',
    "return sandbox ally clip",
)
characters = once(
    characters,
    '         clip.setScaleMult(MULT_SCALE);\n      }\n      \n      public function createEnemyPortal',
    '         clip.setScaleMult(MULT_SCALE);\n         return clip;\n      }\n      \n      public function createEnemyPortal',
    "return sandbox enemy clip",
)
write("System/GameObject/CharacterMgr.as", characters)

# Expansion difficulty bands call this legacy name for odd-numbered tiers.
# The original sound manager exposes the same track as playBgmBattle(), so add
# the missing compatibility alias instead of allowing battle initialization to
# abort before waves and sandbox controls are installed.
sound = read("Manager/SoundManager.as")
sound = once(
    sound,
    "      public function playBgmBattle2() : *\n",
    '''      public function playBgmBattle1() : *
      {
         return this.playBgmBattle();
      }

      public function playBgmBattle2() : *
''',
    "Expansion battle music compatibility alias",
)
write("Manager/SoundManager.as", sound)

# Keep the production Pages whitelist and also permit loopback for repeatable
# browser certification of the exact release bytes before publishing.
host = read("Manager/HostManager.as")
host = once(
    host,
    '         else if(this._host_address.lastIndexOf("recordswiper1t.github.io") > -1)\n',
    '         else if(this._host_address.lastIndexOf("recordswiper1t.github.io") > -1 || this._host_address.lastIndexOf("127.0.0.1") > -1 || this._host_address.lastIndexOf("localhost") > -1)\n',
    "loopback runtime certification whitelist",
)
write("Manager/HostManager.as", host)


# ---------------------------------------------------------------------------
# 3. Replace the three-line keyboard cheat sheet with a compact, collapsible,
# clickable control palette. Keyboard shortcuts remain available.
# ---------------------------------------------------------------------------
battle = read("System/Battle/BattleSystem.as")
battle = once(
    battle,
    "   import flash.events.KeyboardEvent;\n",
    "   import flash.display.MovieClip;\n   import flash.events.KeyboardEvent;\n   import flash.events.MouseEvent;\n",
    "sandbox display imports",
)
battle = once(
    battle,
    "      private var sandboxHud:TextField = null;\n      \n      private var sandboxHudVisible:Boolean = true;\n",
    "      private var sandboxPanel:MovieClip = null;\n      \n      private var sandboxToggleButton:MovieClip = null;\n      \n      private var sandboxStatus:TextField = null;\n      \n      private var sandboxHudVisible:Boolean = false;\n",
    "sandbox UI fields",
)
battle = once(
    battle,
    '''         if(this.sandboxHud != null && this.sandboxHud.parent != null)
         {
            this.sandboxHud.parent.removeChild(this.sandboxHud);
         }
         this.sandboxHud = null;
''',
    '''         if(this.sandboxPanel != null && this.sandboxPanel.parent != null)
         {
            this.sandboxPanel.parent.removeChild(this.sandboxPanel);
         }
         if(this.sandboxToggleButton != null && this.sandboxToggleButton.parent != null)
         {
            this.sandboxToggleButton.parent.removeChild(this.sandboxToggleButton);
         }
         this.sandboxPanel = null;
         this.sandboxToggleButton = null;
         this.sandboxStatus = null;
''',
    "sandbox UI destroy",
)

start = battle.index("      private function sandboxInstall()")
end = battle.index("      public function showBattleMenu()", start)
sandbox_methods = r'''      private function sandboxMakeButton(LABEL:String, ACTION:String, X:Number, Y:Number, WIDTH:Number = 86) : MovieClip
      {
         var button:MovieClip = new MovieClip();
         var label:TextField = new TextField();
         button.name = ACTION;
         button.x = X;
         button.y = Y;
         button.graphics.lineStyle(1,10066329,1);
         button.graphics.beginFill(2236962,0.98);
         button.graphics.drawRoundRect(0,0,WIDTH,27,7,7);
         button.graphics.endFill();
         label.defaultTextFormat = new TextFormat("_sans",10,16777215,true);
         label.text = LABEL;
         label.width = WIDTH;
         label.height = 22;
         label.y = 5;
         label.selectable = false;
         label.mouseEnabled = false;
         button.addChild(label);
         button.buttonMode = true;
         button.mouseChildren = false;
         button.addEventListener(MouseEvent.CLICK,this.sandboxClick,false,0,true);
         return button;
      }

      private function sandboxInstall() : void
      {
         this.mGF.stageRoot.stage.addEventListener(KeyboardEvent.KEY_DOWN,this.sandboxKey,false,0,true);
         this.sandboxToggleButton = this.sandboxMakeButton("SANDBOX","sandbox_toggle",648,20,142);
         this.mGF.stageRoot.addChild(this.sandboxToggleButton);
         this.sandboxPanel = new MovieClip();
         this.sandboxPanel.x = 598;
         this.sandboxPanel.y = 60;
         this.sandboxPanel.graphics.lineStyle(2,13983051,0.95);
         this.sandboxPanel.graphics.beginFill(657930,0.96);
         this.sandboxPanel.graphics.drawRoundRect(0,0,194,349,12,12);
         this.sandboxPanel.graphics.endFill();
         var title:TextField = new TextField();
         title.defaultTextFormat = new TextFormat("_sans",14,16763904,true);
         title.text = "SANDBOX CONTROLS";
         title.width = 178;
         title.height = 24;
         title.x = 9;
         title.y = 7;
         title.selectable = false;
         title.mouseEnabled = false;
         this.sandboxPanel.addChild(title);
         this.sandboxStatus = new TextField();
         this.sandboxStatus.defaultTextFormat = new TextFormat("_sans",10,15658734,false);
         this.sandboxStatus.width = 176;
         this.sandboxStatus.height = 61;
         this.sandboxStatus.x = 9;
         this.sandboxStatus.y = 30;
         this.sandboxStatus.multiline = true;
         this.sandboxStatus.wordWrap = true;
         this.sandboxStatus.selectable = false;
         this.sandboxStatus.mouseEnabled = false;
         this.sandboxPanel.addChild(this.sandboxStatus);
         this.sandboxPanel.addChild(this.sandboxMakeButton("PREV UNIT","sandbox_prev",8,91));
         this.sandboxPanel.addChild(this.sandboxMakeButton("NEXT UNIT","sandbox_next",100,91));
         this.sandboxPanel.addChild(this.sandboxMakeButton("SPAWN ALLY","sandbox_ally",8,122));
         this.sandboxPanel.addChild(this.sandboxMakeButton("SPAWN ENEMY","sandbox_enemy",100,122));
         this.sandboxPanel.addChild(this.sandboxMakeButton("BATCH","sandbox_batch",8,153));
         this.sandboxPanel.addChild(this.sandboxMakeButton("+ MANA","sandbox_mana",100,153));
         this.sandboxPanel.addChild(this.sandboxMakeButton("SPEED","sandbox_speed",8,184));
         this.sandboxPanel.addChild(this.sandboxMakeButton("HEAL ALLIES","sandbox_heal",100,184));
         this.sandboxPanel.addChild(this.sandboxMakeButton("WIPE ENEMY","sandbox_wipe",8,215));
         this.sandboxPanel.addChild(this.sandboxMakeButton("WIN BATTLE","sandbox_win",100,215));
         this.sandboxPanel.addChild(this.sandboxMakeButton("FREE SPELLS","sandbox_free",8,246));
         this.sandboxPanel.addChild(this.sandboxMakeButton("NO BUILD CAP","sandbox_build",100,246));
         this.sandboxPanel.addChild(this.sandboxMakeButton("FAST SPAWN","sandbox_fast",8,277));
         this.sandboxPanel.addChild(this.sandboxMakeButton("POP BOOST","sandbox_pop",100,277));
         this.sandboxPanel.addChild(this.sandboxMakeButton("DISABLE SANDBOX","sandbox_disable",8,312,178));
         this.mGF.stageRoot.addChild(this.sandboxPanel);
         this.sandboxPanel.visible = false;
         this.sandboxRefresh("Ready");
      }

      private function sandboxOnOff(V:Boolean) : String
      {
         return V ? "ON" : "off";
      }

      private function sandboxSpeedText() : String
      {
         return this.sandboxSpeedIndex == 0 ? "1x" : (this.sandboxSpeedIndex == 1 ? "2x" : "4x");
      }

      private function sandboxResetToggles() : void
      {
         sandboxFreeSpells = false;
         sandboxUnlimitedBuildings = false;
         sandboxFastUnits = false;
         sandboxPopBoost = false;
         this.sandboxSpeedIndex = 0;
         this.mGF.stageRoot.stage.frameRate = 24;
      }

      private function sandboxRefresh(MSG:String = "") : void
      {
         if(this.sandboxPanel == null || this.sandboxToggleButton == null)
         {
            return;
         }
         this.sandboxPanel.visible = sandboxMaster && this.sandboxHudVisible;
         TextField(this.sandboxToggleButton.getChildAt(0)).text = sandboxMaster ? (this.sandboxHudVisible ? "SANDBOX ON ▲" : "SANDBOX ON ▼") : "SANDBOX";
         if(this.sandboxStatus == null)
         {
            return;
         }
         var name:String = String(this.sandboxNames[this.sandboxIndex]);
         this.sandboxStatus.text = name.toUpperCase() + "  •  batch " + this.sandboxCount + "  •  mana +" + this.sandboxManaAmount + "\nSpeed " + this.sandboxSpeedText() + "  •  free " + this.sandboxOnOff(sandboxFreeSpells) + "  •  build∞ " + this.sandboxOnOff(sandboxUnlimitedBuildings) + "\nFast " + this.sandboxOnOff(sandboxFastUnits) + "  •  population " + this.sandboxOnOff(sandboxPopBoost) + (MSG == "" ? "" : "\n" + MSG);
      }

      private function sandboxCycle(DELTA:int) : void
      {
         this.sandboxIndex += DELTA;
         if(this.sandboxIndex < 0)
         {
            this.sandboxIndex = this.sandboxNames.length - 1;
         }
         if(this.sandboxIndex >= this.sandboxNames.length)
         {
            this.sandboxIndex = 0;
         }
         this.sandboxRefresh("Unit selected");
      }

      private function sandboxCycleBatch() : void
      {
         if(this.sandboxCount == 1) this.sandboxCount = 5;
         else if(this.sandboxCount == 5) this.sandboxCount = 10;
         else if(this.sandboxCount == 10) this.sandboxCount = 20;
         else this.sandboxCount = 1;
         this.sandboxRefresh("Batch size changed");
      }

      private function sandboxCycleSpeed() : void
      {
         this.sandboxSpeedIndex = (this.sandboxSpeedIndex + 1) % 3;
         this.mGF.stageRoot.stage.frameRate = this.sandboxSpeedIndex == 0 ? 24 : (this.sandboxSpeedIndex == 1 ? 48 : 96);
         this.sandboxRefresh("Battle speed " + this.sandboxSpeedText());
      }

      private function sandboxSpawn(ALLY:Boolean) : void
      {
         var i:int = 0;
         var spawned:* = null;
         var name:String = String(this.sandboxNames[this.sandboxIndex]);
         var group:int = 0;
         var target:int = ALLY ? this.bgMgr.getRightBorder() - 120 : this.bgMgr.getLeftBorder() + 120;
         while(i < this.sandboxCount)
         {
            group = (ALLY ? 90 : 190) + i;
            if(ALLY)
            {
               spawned = this.charMgr.createPlayerUnit("unit",name,target,group);
            }
            else
            {
               spawned = this.charMgr.createEnemyUnit("unit",name,this.bgMgr.getRightBorder() - 120 + Math.random() * 70,0,group,0,0,"",1);
               if(spawned != null)
               {
                  spawned.commandMove("enemy",group,target);
               }
            }
            i++;
         }
         this.sandboxRefresh((ALLY ? "Allies advancing ×" : "Enemies advancing ×") + this.sandboxCount);
      }

      private function sandboxWipeEnemies() : void
      {
         var c:* = null;
         var i:int = this.mGF.contUNIT.numChildren - 1;
         while(i >= 0)
         {
            c = this.mGF.contUNIT.getChildAt(i);
            if(c != null && c.isAlignmentAs("enemy")) c.setDamage(99999999);
            i--;
         }
         this.sandboxRefresh("Enemies cleared");
      }

      private function sandboxHealAllies() : void
      {
         var c:* = null;
         var i:int = 0;
         while(i < this.mGF.contUNIT.numChildren)
         {
            c = this.mGF.contUNIT.getChildAt(i);
            if(c != null && c.isAlignmentAs("ally")) c.setDamageHeal(99999999);
            i++;
         }
         this.sandboxRefresh("Allies healed");
      }

      private function sandboxEnable() : void
      {
         sandboxMaster = true;
         this.sandboxHudVisible = true;
         this.sandboxRefresh("Sandbox enabled — normal saves are unchanged");
      }

      private function sandboxDisable() : void
      {
         sandboxMaster = false;
         this.sandboxHudVisible = false;
         this.sandboxResetToggles();
         this.sandboxRefresh("Sandbox disabled");
      }

      private function sandboxInstantWin() : void
      {
         this.battle_result = "win";
         this.battle_boss_kill = Math.max(this.battle_boss_kill,1);
         this.sandboxRefresh("Battle marked won");
      }

      private function sandboxClick(e:MouseEvent) : void
      {
         var action:String = String(e.currentTarget.name);
         if(action == "sandbox_toggle")
         {
            if(!sandboxMaster) this.sandboxEnable();
            else
            {
               this.sandboxHudVisible = !this.sandboxHudVisible;
               this.sandboxRefresh();
            }
            return;
         }
         if(action == "sandbox_disable") { this.sandboxDisable(); return; }
         if(!sandboxMaster) return;
         if(action == "sandbox_prev") this.sandboxCycle(-1);
         else if(action == "sandbox_next") this.sandboxCycle(1);
         else if(action == "sandbox_ally") this.sandboxSpawn(true);
         else if(action == "sandbox_enemy") this.sandboxSpawn(false);
         else if(action == "sandbox_batch") this.sandboxCycleBatch();
         else if(action == "sandbox_mana") { this.playerMgr.sandboxAddMana(this.sandboxManaAmount); this.sandboxRefresh("Mana added"); }
         else if(action == "sandbox_speed") this.sandboxCycleSpeed();
         else if(action == "sandbox_heal") this.sandboxHealAllies();
         else if(action == "sandbox_wipe") this.sandboxWipeEnemies();
         else if(action == "sandbox_win") this.sandboxInstantWin();
         else if(action == "sandbox_free") { sandboxFreeSpells = !sandboxFreeSpells; this.sandboxRefresh("Free spells " + this.sandboxOnOff(sandboxFreeSpells)); }
         else if(action == "sandbox_build") { sandboxUnlimitedBuildings = !sandboxUnlimitedBuildings; this.sandboxRefresh("No build cap " + this.sandboxOnOff(sandboxUnlimitedBuildings)); }
         else if(action == "sandbox_fast") { sandboxFastUnits = !sandboxFastUnits; this.sandboxRefresh("Fast spawn " + this.sandboxOnOff(sandboxFastUnits)); }
         else if(action == "sandbox_pop") { sandboxPopBoost = !sandboxPopBoost; this.sandboxRefresh("Population boost " + this.sandboxOnOff(sandboxPopBoost)); }
      }

      private function sandboxKey(e:KeyboardEvent) : void
      {
         if(e.keyCode == 192)
         {
            if(sandboxMaster) this.sandboxDisable(); else this.sandboxEnable();
            return;
         }
         if(!sandboxMaster) return;
         if(e.keyCode == 112) { this.playerMgr.sandboxAddMana(this.sandboxManaAmount); this.sandboxRefresh("Mana added"); }
         else if(e.keyCode == 113) this.sandboxCycle(-1);
         else if(e.keyCode == 114) this.sandboxCycle(1);
         else if(e.keyCode == 115) this.sandboxSpawn(true);
         else if(e.keyCode == 116) this.sandboxSpawn(false);
         else if(e.keyCode == 117) this.sandboxCycleBatch();
         else if(e.keyCode == 118) this.sandboxCycleSpeed();
         else if(e.keyCode == 119) this.sandboxWipeEnemies();
         else if(e.keyCode == 120) this.sandboxInstantWin();
         else if(e.keyCode == 121) this.sandboxHealAllies();
         else if(e.keyCode == 122) { sandboxFreeSpells = !sandboxFreeSpells; this.sandboxRefresh(); }
         else if(e.keyCode == 123) { sandboxFastUnits = !sandboxFastUnits; this.sandboxRefresh(); }
         else if(e.keyCode == 85) { sandboxUnlimitedBuildings = !sandboxUnlimitedBuildings; this.sandboxRefresh(); }
         else if(e.keyCode == 79) { sandboxPopBoost = !sandboxPopBoost; this.sandboxRefresh(); }
         else if(e.keyCode == 219) { this.sandboxManaAmount = Math.max(10,int(this.sandboxManaAmount / 2)); this.sandboxRefresh(); }
         else if(e.keyCode == 221) { this.sandboxManaAmount = Math.min(5000,this.sandboxManaAmount * 2); this.sandboxRefresh(); }
         else if(e.keyCode == 72) { this.sandboxHudVisible = !this.sandboxHudVisible; this.sandboxRefresh(); }
      }

'''
battle = battle[:start] + sandbox_methods + battle[end:]
write("System/Battle/BattleSystem.as", battle)


checks = {
    "System/Battle/BattleControlPlayer.as": [
        "REF.localToGlobal(new Point(0,0))",
        "clip.expansionSlot = INDEX",
        "this.bSys.ui.addChild(clip)",
    ],
    "System/Battle/PlayerUnit.as": [
        'this.icoClip.unitName.text = this.name_id.toUpperCase()',
        'this.icoClip.expansionUnlocked ? "EMPTY" : "LOCKED"',
    ],
    "System/GameObject/CharacterMgr.as": ["return clip;"],
    "Manager/SoundManager.as": ["public function playBgmBattle1()", "return this.playBgmBattle();"],
    "Manager/HostManager.as": ['lastIndexOf("127.0.0.1") > -1'],
    "System/Battle/BattleSystem.as": [
        'this.sandboxMakeButton("SPAWN ALLY"',
        'this.sandboxMakeButton("SPAWN ENEMY"',
        'spawned.commandMove("enemy",group,target)',
        "Allies advancing",
        "Enemies advancing",
    ],
}
for rel, needles in checks.items():
    text = read(rel)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"validation failed: {needle!r} missing from {rel}")

print("Epic War 5 Expansion V3.8 HUD + clickable sandbox polish applied")
