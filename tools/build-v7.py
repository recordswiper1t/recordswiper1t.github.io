#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: build-v7.py <exported-scripts-dir>")

scripts = Path(sys.argv[1])


def read(name: str) -> str:
    p = scripts / name
    if not p.exists():
        raise SystemExit(f"missing exported script: {p}")
    return p.read_text(encoding="utf-8-sig")


def write(name: str, text: str) -> None:
    (scripts / name).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 exact match, found {count}")
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# Level.as: time-attack state/UI, immediate all-wave activation, wall-clock
# timer, and a per-level best time stored separately from the normal save slots.
# ---------------------------------------------------------------------------
level = read("Level.as")

level = replace_once(
    level,
    "   import flash.geom.*;\n",
    "   import flash.geom.*;\n   import flash.net.SharedObject;\n",
    "SharedObject import",
)

level = replace_once(
    level,
    "      public static var qolHeroEnabled:Object = null;",
    "      public static var qolHeroEnabled:Object = null;\n      \n      public static var qolTimeAttackEnabled:Boolean = false;\n      \n      public static var qolRecycleEnemies:Boolean = false;",
    "time-attack static settings",
)

level = replace_once(
    level,
    "      private var qolUnlimitedMode:Boolean = false;",
    "      private var qolUnlimitedMode:Boolean = false;\n      \n      private var qolTimeAttackLaunched:Boolean = false;\n      \n      private var qolTimerRunning:Boolean = false;\n      \n      private var qolTimerStartMs:int = 0;\n      \n      private var qolTimerLast:Number = -1;\n      \n      private var qolTimerLabel:TextField;\n      \n      private var qolBestTime:Number = -1;\n      \n      private var qolBestTimeLoaded:Boolean = false;",
    "time-attack level state",
)

level = replace_once(
    level,
    "         this.addChild(this.qolSpeedButton);",
    "         this.addChild(this.qolSpeedButton);\n         this.qolInstallTimerHud();",
    "timer HUD install",
)

helpers = r'''      private function qolInstallTimerHud() : void
      {
         if(this.qolTimerLabel != null)
         {
            return;
         }
         this.qolTimerLabel = new TextField();
         this.qolTimerLabel.defaultTextFormat = new TextFormat("_sans",13,16777215,true);
         this.qolTimerLabel.width = 166;
         this.qolTimerLabel.height = 42;
         this.qolTimerLabel.x = 562;
         this.qolTimerLabel.y = 540;
         this.qolTimerLabel.background = true;
         this.qolTimerLabel.backgroundColor = 1118481;
         this.qolTimerLabel.textColor = 16777215;
         this.qolTimerLabel.selectable = false;
         this.qolTimerLabel.mouseEnabled = false;
         this.addChild(this.qolTimerLabel);
         this.qolLoadBestTime();
         this.qolUpdateTimerHud();
      }
      
      private function qolTimeAttackKey() : String
      {
         return getQualifiedClassName(this) + ":" + String(this.mode);
      }
      
      private function qolLoadBestTime() : void
      {
         if(this.qolBestTimeLoaded)
         {
            return;
         }
         this.qolBestTimeLoaded = true;
         try
         {
            var save:SharedObject = SharedObject.getLocal("krf_qol_time_attack");
            var key:String = this.qolTimeAttackKey();
            if(save.data.hasOwnProperty(key))
            {
               var stored:Number = Number(save.data[key]);
               if(!isNaN(stored) && stored > 0)
               {
                  this.qolBestTime = stored;
               }
            }
         }
         catch(error:Error)
         {
         }
      }
      
      private function qolSaveBestTime() : void
      {
         try
         {
            var save:SharedObject = SharedObject.getLocal("krf_qol_time_attack");
            save.data[this.qolTimeAttackKey()] = this.qolBestTime;
            save.flush();
         }
         catch(error:Error)
         {
         }
      }
      
      private function qolTimeText(param1:Number) : String
      {
         if(param1 < 0 || isNaN(param1))
         {
            return "--";
         }
         return param1.toFixed(2) + "s";
      }
      
      private function qolBestTimeText() : String
      {
         this.qolLoadBestTime();
         return this.qolTimeText(this.qolBestTime);
      }
      
      private function qolUpdateTimerHud() : void
      {
         if(this.qolTimerLabel == null)
         {
            return;
         }
         this.qolTimerLabel.visible = Level.qolTimeAttackEnabled;
         if(!Level.qolTimeAttackEnabled)
         {
            return;
         }
         var current:Number = this.qolTimerLast;
         if(this.qolTimerRunning)
         {
            current = (getTimer() - this.qolTimerStartMs) / 1000;
         }
         var currentText:String = this.qolTimeAttackLaunched ? this.qolTimeText(current) : "ARMED";
         this.qolTimerLabel.text = "TIME  " + currentText + "\nBEST  " + this.qolBestTimeText();
      }
      
      private function qolStartTimeAttack() : void
      {
         if(this.qolTimeAttackLaunched || this.waves == null || this.waves.length == 0)
         {
            return;
         }
         this.qolTimeAttackLaunched = true;
         this.qolTimerRunning = true;
         this.qolTimerLast = -1;
         this.qolTimerStartMs = getTimer();
         if(this.indexWaves < this.waves.length)
         {
            this.qolSendAllWaves();
            while(this.qolSendAllPending)
            {
               this.qolSendQueuedWave();
            }
         }
         this.qolUpdateTimerHud();
      }
      
      private function qolFinishTimeAttack() : void
      {
         if(!this.qolTimerRunning)
         {
            return;
         }
         this.qolTimerLast = Math.max(0,(getTimer() - this.qolTimerStartMs) / 1000);
         this.qolTimerRunning = false;
         this.qolLoadBestTime();
         if(this.qolTimerLast > 0 && (this.qolBestTime < 0 || this.qolTimerLast < this.qolBestTime))
         {
            this.qolBestTime = this.qolTimerLast;
            this.qolSaveBestTime();
         }
         this.qolUpdateTimerHud();
      }
      
      public function qolTimeAttackEnemyKilled() : void
      {
         if(this.qolTimerRunning && this.indexWaves >= this.waves.length && !this.hasEnemies())
         {
            this.qolFinishTimeAttack();
         }
      }
      
      private function qolTimeAttackTick() : void
      {
         if(Level.qolTimeAttackEnabled && !this.qolTimeAttackLaunched && this.indexWaves == 0 && this.waves != null && this.waves.length > 0)
         {
            this.qolStartTimeAttack();
         }
         if(this.qolTimerRunning)
         {
            if(this.indexWaves >= this.waves.length && !this.hasEnemies())
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
level = replace_once(
    level,
    "      private function qolGameTick() : void\n",
    helpers + "      private function qolGameTick() : void\n",
    "time-attack helpers",
)

level = replace_once(
    level,
    "         ++this.qolPerfFrame;",
    "         ++this.qolPerfFrame;\n         this.qolTimeAttackTick();",
    "time-attack tick",
)

level = replace_once(
    level,
    '            this.qolSettings.addChild(this.qolLabel("Send-all pauses new waves while the board is overloaded.",28,442,14));',
    '            this.qolSettings.addChild(this.qolButton("Time attack  →",165,442,250,"page_time_attack"));',
    "time-attack settings entry",
)

level = replace_once(
    level,
    "         else\n         {\n            this.qolEnsureHeroSelection();",
    "         else if(this.qolSettingsPage == 2)\n         {\n            this.qolEnsureHeroSelection();",
    "hero page condition",
)

hero_end = '''            this.qolSettings.addChild(this.qolButton("←  Main settings",165,374,250,"page_main"));
         }
      }
      
      private function qolSettingsClick(param1:MouseEvent) : void
'''
time_page = '''            this.qolSettings.addChild(this.qolButton("←  Main settings",165,374,250,"page_main"));
         }
         else
         {
            this.qolSettings.addChild(this.qolLabel("TIME ATTACK",28,20,24));
            this.qolSettings.addChild(this.qolButton("Timer + all waves: " + (Level.qolTimeAttackEnabled ? "ON" : "OFF"),28,72,524,"time_attack"));
            this.qolSettings.addChild(this.qolButton("Recycle exits: " + (Level.qolRecycleEnemies ? "ON" : "OFF"),28,132,524,"recycle_exits"));
            this.qolSettings.addChild(this.qolLabel("Timer ON activates every authored wave immediately.",28,202,14));
            this.qolSettings.addChild(this.qolLabel("Recycle ON sends escaped enemies back to their path start with no life loss.",28,232,14));
            this.qolSettings.addChild(this.qolLabel("Best for this level: " + this.qolBestTimeText(),28,286,18));
            this.qolSettings.addChild(this.qolLabel(this.indexWaves == 0 ? "Turn recycling on first, then enable the timer to start." : "If wave 1 already started, the timer setting applies next level.",28,330,14));
            this.qolSettings.addChild(this.qolButton("←  Main settings",165,400,250,"page_main"));
         }
      }
      
      private function qolSettingsClick(param1:MouseEvent) : void
'''
level = replace_once(level, hero_end, time_page, "time-attack settings page")

level = replace_once(
    level,
    '         else if(action == "unlimited")\n',
    '''         else if(action == "page_time_attack")
         {
            this.qolSettingsPage = 3;
         }
         else if(action == "recycle_exits")
         {
            Level.qolRecycleEnemies = !Level.qolRecycleEnemies;
         }
         else if(action == "time_attack")
         {
            Level.qolTimeAttackEnabled = !Level.qolTimeAttackEnabled;
            if(!Level.qolTimeAttackEnabled)
            {
               this.qolTimerRunning = false;
               this.qolUpdateTimerHud();
            }
            else if(this.indexWaves == 0 && !this.qolTimeAttackLaunched)
            {
               this.qolHideSettings();
               this.qolStartTimeAttack();
               return;
            }
            this.qolUpdateTimerHud();
         }
         else if(action == "unlimited")
''',
    "time-attack settings actions",
)

level = replace_once(
    level,
    "            else if(!this.qolUnlimitedMode && !this.hasEnemies())\n            {",
    "            else if(!this.qolUnlimitedMode && !this.hasEnemies())\n            {\n               this.qolFinishTimeAttack();",
    "time-attack native win finish",
)

write("Level.as", level)


# ---------------------------------------------------------------------------
# Enemy.as: intercept the common path-exit branch before it removes the enemy,
# deducts lives, grants exit gold, and destroys the instance. Keeping the same
# object preserves boss state and remaining health across laps.
# ---------------------------------------------------------------------------
enemy = read("Enemy.as")
exit_anchor = '''         if(this.§package for var§ + 7 < this.§with const static§.length)
         {
            return false;
         }
         this.isActive = false;
         this.cRoot.§with for super§(this);
         this.cRoot.§function for const§(this.cost);
         this.cRoot.updateCash(this.gold);
         this.destroyThis();
         return true;
'''
exit_replacement = '''         if(this.§package for var§ + 7 < this.§with const static§.length)
         {
            return false;
         }
         if(Level.qolRecycleEnemies)
         {
            this.isActive = false;
            this.isBlocked = false;
            this.isFighting = false;
            this.isCharging = false;
            this.soldier = null;
            this.§_-1v§ = "";
            this.§package for var§ = 0;
            this.x = this.§with const static§[0].x;
            this.y = this.§with const static§[0].y;
            this.xSpeed = 0;
            this.ySpeed = 0;
            this.visible = false;
            return true;
         }
         this.isActive = false;
         this.cRoot.§with for super§(this);
         this.cRoot.§function for const§(this.cost);
         this.cRoot.updateCash(this.gold);
         this.destroyThis();
         return true;
'''
enemy = replace_once(enemy, exit_anchor, exit_replacement, "enemy exit recycling")

enemy = replace_once(
    enemy,
    "         this.isDead = true;\n         this.lifeBar.hide();",
    "         this.isDead = true;\n         if(this.cRoot != null)\n         {\n            this.cRoot.qolTimeAttackEnemyKilled();\n         }\n         this.lifeBar.hide();",
    "timer kill notification",
)
write("Enemy.as", enemy)


checks = {
    "Level.as": [
        "qolTimeAttackEnabled", "qolRecycleEnemies", "qolStartTimeAttack",
        "qolTimeAttackEnemyKilled", "SharedObject.getLocal(\"krf_qol_time_attack\")",
        "Timer + all waves:", "Recycle exits:", "qolFinishTimeAttack();",
    ],
    "Enemy.as": [
        "if(Level.qolRecycleEnemies)", "this.§package for var§ = 0;",
        "this.cRoot.qolTimeAttackEnemyKilled();",
    ],
}
for name, needles in checks.items():
    text = read(name)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"validation failed: {needle!r} missing from {name}")

print("V7 time-attack patches applied successfully")
