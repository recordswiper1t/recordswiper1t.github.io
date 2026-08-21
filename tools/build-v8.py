#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: build-v8.py <exported-v7-scripts-dir>")

scripts = Path(sys.argv[1])
level_path = scripts / "Level.as"
if not level_path.exists():
    raise SystemExit(f"missing exported V7 Level.as: {level_path}")

level = level_path.read_text(encoding="utf-8-sig")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 exact match, found {count}")
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# V8 performance: V7's time-attack completion test walked every enemy both on
# every frame and again on every kill. With all waves active that can become a
# large O(k*n) tax during mass deaths. Kills now only mark completion dirty;
# the expensive scan is amortized to 15 Hz. Timer text is updated at 10 Hz.
# ---------------------------------------------------------------------------
level = replace_once(
    level,
    "      private var qolBestTimeLoaded:Boolean = false;",
    "      private var qolBestTimeLoaded:Boolean = false;\n      \n      private var qolTimeAttackDirty:Boolean = false;",
    "time attack dirty state",
)

old_killed = '''      public function qolTimeAttackEnemyKilled() : void
      {
         if(this.qolTimerRunning && this.qolTimeAttackDone())
         {
            this.qolFinishTimeAttack();
         }
      }
'''
new_killed = '''      public function qolTimeAttackEnemyKilled() : void
      {
         if(this.qolTimerRunning)
         {
            this.qolTimeAttackDirty = true;
         }
      }
'''
level = replace_once(level, old_killed, new_killed, "amortized kill completion")

old_tick = '''      private function qolTimeAttackTick() : void
      {
         if(Level.qolTimeAttackEnabled && !this.qolTimeAttackLaunched && this.indexWaves == 0 && this.waves != null && this.waves.length > 0)
         {
            this.qolStartTimeAttack();
         }
         if(this.qolTimerRunning)
         {
            if(this.qolTimeAttackDone())
            {
               this.qolFinishTimeAttack();
            }
            else
            {
               this.qolUpdateTimerHud();
            }
         }
      }
'''
new_tick = '''      private function qolTimeAttackTick() : void
      {
         if(Level.qolTimeAttackEnabled && !this.qolTimeAttackLaunched && this.indexWaves == 0 && this.waves != null && this.waves.length > 0)
         {
            this.qolStartTimeAttack();
         }
         if(this.qolTimerRunning)
         {
            if((this.qolTimeAttackDirty && this.qolPerfFrame % 4 == 0) || this.qolPerfFrame % 12 == 0)
            {
               this.qolTimeAttackDirty = false;
               if(this.qolTimeAttackDone())
               {
                  this.qolFinishTimeAttack();
                  return;
               }
            }
            if(this.qolPerfFrame % 6 == 0)
            {
               this.qolUpdateTimerHud();
            }
         }
      }
'''
level = replace_once(level, old_tick, new_tick, "timer scan and HUD throttling")

# V6 already reduced non-gameplay/cosmetic updates under heavy swarms. Add an
# ultra tier so extreme Time Attack boards spend even less time on cosmetics.
level = replace_once(
    level,
    "var extreme:Boolean = this.entities.numChildren > 260 || this.bullets.numChildren > 330;",
    "var extreme:Boolean = this.entities.numChildren > 260 || this.bullets.numChildren > 330;\n         var ultra:Boolean = this.entities.numChildren > 520 || this.bullets.numChildren > 680;",
    "ultra swarm threshold",
)
level = replace_once(
    level,
    "if(!heavy || !extreme && (this.qolPerfFrame & 1) == 0 || extreme && this.qolPerfFrame % 6 == 0)",
    "if(!heavy || !extreme && (this.qolPerfFrame & 1) == 0 || extreme && !ultra && this.qolPerfFrame % 6 == 0 || ultra && this.qolPerfFrame % 12 == 0)",
    "ultra cosmetic cadence",
)

# ---------------------------------------------------------------------------
# Ctrl+C / Ctrl+V tower clipboard.
# Copy uses the tower currently selected in the game's radial menu. Paste uses
# the currently selected empty TowerHolder. It copies the tower family/branch
# (including the six normal tier-4 branches) and charges the same direct build
# cost used by the existing V6/V7 sandbox catalog. Ability ranks are deliberately
# not cloned because those are private per-subclass state and blindly copying
# them would create invalid soldier/projectile references.
# ---------------------------------------------------------------------------
level = replace_once(
    level,
    "      private var qolTimeAttackDirty:Boolean = false;",
    "      private var qolTimeAttackDirty:Boolean = false;\n      \n      private var qolTowerClipboardAction:String = \"\";",
    "tower clipboard state",
)

clipboard_helpers = r'''      private function qolTowerActionFor(param1:Object) : String
      {
         if(param1 == null)
         {
            return "";
         }
         var name:String = getQualifiedClassName(param1);
         switch(name)
         {
            case "TowerMage":
               return "mage";
            case "§_-v9§":
               return "archer";
            case "TowerEngineer":
               return "engineer";
            case "§_-oH§":
               return "soldier";
            case "TowerArcherCrossbow":
               return "qol_crossbow";
            case "TowerArcherTotem":
               return "qol_totem";
            case "TowerMageArchmage":
               return "qol_archmage";
            case "TowerMageNecromancer":
               return "qol_necromancer";
            case "TowerEngineerDwaarp":
               return "qol_dwaarp";
            case "TowerEngineerMech":
               return "qol_mech";
            case "TowerSoldierAssassin":
               return "qol_assassin";
            case "TowerSoldierTemplar":
               return "qol_templar";
         }
         return "";
      }
      
      private function qolTowerClipboardCost(param1:String) : int
      {
         switch(param1)
         {
            case "archer":
               return this.gameSettings.archers.level1.cost;
            case "soldier":
               return this.gameSettings.§_-jG§.level1.cost;
            case "mage":
               return this.gameSettings.mages.level1.cost;
            case "engineer":
               return this.gameSettings.engineers.level1.cost;
            case "qol_crossbow":
               return this.gameSettings.archers.crossbow.cost;
            case "qol_totem":
               return this.gameSettings.archers.totem.cost;
            case "qol_archmage":
               return this.gameSettings.mages.archmage.cost;
            case "qol_necromancer":
               return this.gameSettings.mages.necromancer.cost;
            case "qol_dwaarp":
               return this.gameSettings.engineers.dwaarp.cost;
            case "qol_mech":
               return this.gameSettings.engineers.mech.cost;
            case "qol_assassin":
               return this.gameSettings.§_-jG§.assassin.cost;
            case "qol_templar":
               return this.gameSettings.§_-jG§.templar.cost;
         }
         return 2147483647;
      }
      
      private function qolTowerClipboardKey(param1:KeyboardEvent) : void
      {
         if(!param1.ctrlKey || this.quickMenu == null)
         {
            return;
         }
         var selected:Object = this.quickMenu.cTower;
         if(param1.keyCode == 67)
         {
            var action:String = this.qolTowerActionFor(selected);
            if(action != "")
            {
               this.qolTowerClipboardAction = action;
               param1.preventDefault();
            }
            return;
         }
         if(param1.keyCode == 86 && this.qolTowerClipboardAction != "" && selected is TowerHolder)
         {
            var cost:int = this.qolTowerClipboardCost(this.qolTowerClipboardAction);
            if(this.cash >= cost)
            {
               TowerHolder(selected).upgradeTower(this.qolTowerClipboardAction);
               param1.preventDefault();
            }
         }
      }
      
'''
level = replace_once(
    level,
    "      private function qolInstallTimerHud() : void\n",
    clipboard_helpers + "      private function qolInstallTimerHud() : void\n",
    "tower clipboard helpers",
)

# Install one keyboard listener alongside the existing HUD initialization. The
# weak listener is removed automatically with the Level instance.
level = replace_once(
    level,
    "         this.addChild(this.qolTimerLabel);\n         this.qolLoadBestTime();",
    "         this.addChild(this.qolTimerLabel);\n         if(this.stage != null)\n         {\n            this.stage.addEventListener(KeyboardEvent.KEY_DOWN,this.qolTowerClipboardKey,false,0,true);\n         }\n         this.qolLoadBestTime();",
    "tower clipboard keyboard listener",
)

checks = [
    "qolTimeAttackDirty",
    "this.qolPerfFrame % 12 == 0",
    "var ultra:Boolean",
    "ultra && this.qolPerfFrame % 12 == 0",
    "qolTowerClipboardKey",
    'case "TowerArcherCrossbow"',
    'return "qol_dwaarp";',
    "this.cash >= cost",
    "TowerHolder(selected).upgradeTower(this.qolTowerClipboardAction);",
]
for needle in checks:
    if needle not in level:
        raise SystemExit(f"validation failed: {needle!r} missing from Level.as")

level_path.write_text(level, encoding="utf-8", newline="\n")
print("V8 performance + tower clipboard patches applied successfully")
