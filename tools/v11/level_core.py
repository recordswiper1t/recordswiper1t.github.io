#!/usr/bin/env python3
from pathlib import Path
import sys
if len(sys.argv)!=2: raise SystemExit("usage: patch.py <scripts-dir>")
scripts=Path(sys.argv[1])
def read(name): return (scripts/name).read_text(encoding="utf-8-sig")
def write(name,text): (scripts/name).write_text(text,encoding="utf-8",newline="\n")
def replace_once(text,old,new,label):
 n=text.count(old)
 if n!=1: raise SystemExit(f"{label}: expected 1 match, found {n}")
 return text.replace(old,new,1)
def insert_before(text,needle,block,label):
 n=text.count(needle)
 if n!=1: raise SystemExit(f"{label}: expected 1 anchor, found {n}")
 return text.replace(needle,block+needle,1)

level=read('Level.as')
level=replace_once(level,'      private var qolTowerClipboardAction:String = "";','''      private var qolTowerClipboardAction:String = "";
      
      private var qolTowerClipboard:Object = null;
      
      private var qolTowerPaste:Object = null;
      
      private var qolDiagLabel:TextField = null;
      
      private var qolDiagEnabled:Boolean = false;
      
      private var qolDiagLastMs:int = 0;
      
      private var qolDiagFrames:int = 0;
      
      private var qolDiagFps:Number = 0;
      
      private var qolHeavyEntities:int = 160;
      
      private var qolHeavyBullets:int = 200;
      
      private var qolExtremeEntities:int = 260;
      
      private var qolExtremeBullets:int = 330;
      
      private var qolUltraEntities:int = 520;
      
      private var qolUltraBullets:int = 680;''','V11 state')
level=level.replace('return "qol_necromancer";','return "qol_necro";')
level=replace_once(level,'''            case "TowerSoldierTemplar":
               return "qol_templar";
            default:
               return "";''','''            case "TowerSoldierTemplar":
               return "qol_templar";
            case "TowerDwarfRiflemen":
               return "qol_dwarf";
            case "TowerSoldierPirates":
               return "qol_pirates";
            case "§_-Zs§":
               return "qol_hall";
            case "§_-MR§":
               return "qol_piratecamp";
            case "§_-Xb§":
               return "qol_legion_archer";
            case "§return const if§":
               return "qol_mercenary";
            case "§override import§":
               return "qol_amazona";
            default:
               return "";''','map special clipboard mapping')
clipboard_helpers=r'''      private function qolTowerBlueprintFor(param1:Object) : Object
      {
         if(param1 == null) return null;
         var root:String = this.qolTowerActionFor(param1);
         if(root == "") return null;
         var actions:Array = [];
         var name:String = getQualifiedClassName(param1);
         var current:String = "";
         if("currentLevel" in param1) current = String(param1["currentLevel"]);
         if(name == "TowerMage" || name == "§_-v9§" || name == "TowerEngineer" || name == "§_-oH§")
         {
            if(current == "level_2") actions.push("level_2");
            else if(current == "level_3") actions.push("level_2","level_3");
         }
         else if("qolBlueprintActions" in param1) actions = param1["qolBlueprintActions"]();
         var invested:int = 0;
         if("§_-6f§" in param1) invested = Math.max(0,int(param1["§_-6f§"]));
         return {"root":root,"className":name,"actions":actions,"cost":invested};
      }
      
      private function qolFindTowerNear(param1:Number, param2:Number, param3:String) : §_-5u§
      {
         var tower:§_-5u§ = null;
         var best:§_-5u§ = null;
         var bestD:Number = 1000000;
         var dx:Number = 0;
         var dy:Number = 0;
         var d:Number = 0;
         for each(tower in this.towers)
         {
            if(tower == null) continue;
            if(param3 != "" && getQualifiedClassName(tower) != param3) continue;
            dx = tower.x - param1; dy = tower.y - param2; d = dx * dx + dy * dy;
            if(d < bestD) { bestD = d; best = tower; }
         }
         return bestD <= 3600 ? best : null;
      }
      
      private function qolProcessTowerPaste() : void
      {
         if(this.qolTowerPaste == null) return;
         this.qolTowerPaste.frames = int(this.qolTowerPaste.frames) + 1;
         var tower:§_-5u§ = this.qolFindTowerNear(Number(this.qolTowerPaste.x),Number(this.qolTowerPaste.y),String(this.qolTowerPaste.className));
         if(tower == null)
         {
            if(int(this.qolTowerPaste.frames) > 120) this.qolTowerPaste = null;
            return;
         }
         var actions:Array = this.qolTowerPaste.actions as Array;
         if(actions != null && actions.length > 0)
         {
            var before:int = this.cash;
            tower.upgradeTower(String(actions.shift()));
            this.qolTowerPaste.charged = int(this.qolTowerPaste.charged) + before - this.cash;
            return;
         }
         var remaining:int = int(this.qolTowerPaste.cost) - int(this.qolTowerPaste.charged);
         if(remaining != 0) this.updateCash(-remaining);
         this.qolTowerPaste = null;
      }
      
      private function qolTowerClipboardKey(param1:KeyboardEvent) : void
      {
         if(!param1.ctrlKey || this.quickMenu == null) return;
         var selected:Object = this.quickMenu.cTower;
         if(param1.keyCode == 67)
         {
            var blueprint:Object = this.qolTowerBlueprintFor(selected);
            if(blueprint != null)
            {
               this.qolTowerClipboard = blueprint;
               this.qolTowerClipboardAction = String(blueprint.root);
               param1.preventDefault();
            }
            return;
         }
         if(param1.keyCode == 86 && this.qolTowerClipboard != null && selected is TowerHolder)
         {
            var cost:int = int(this.qolTowerClipboard.cost);
            if(this.cash >= cost)
            {
               this.qolTowerPaste = {"x":selected.x,"y":selected.y,"className":String(this.qolTowerClipboard.className),"actions":(this.qolTowerClipboard.actions as Array).concat(),"cost":cost,"charged":0,"frames":0};
               var cashBeforeBuild:int = this.cash;
               TowerHolder(selected).upgradeTower(String(this.qolTowerClipboard.root));
               this.qolTowerPaste.charged = cashBeforeBuild - this.cash;
               param1.preventDefault();
            }
         }
      }
      
'''
start=level.find('      private function qolTowerClipboardCost(param1:String) : int\n')
end=level.find('      private function qolInstallTimerHud() : void\n',start)
if start<0 or end<0: raise SystemExit('clipboard block anchors missing')
level=level[:start]+clipboard_helpers+level[end:]
level=replace_once(level,'''         if(this.stage != null)
         {
            this.stage.addEventListener(KeyboardEvent.KEY_DOWN,this.qolTowerClipboardKey,false,0,true);
         }
         this.qolLoadBestTime();''','''         if(this.stage != null)
         {
            this.stage.addEventListener(KeyboardEvent.KEY_DOWN,this.qolTowerClipboardKey,false,0,true);
         }
         this.qolDiagLabel = new TextField();
         this.qolDiagLabel.defaultTextFormat = new TextFormat("_sans",12,16777215,true);
         this.qolDiagLabel.width = 300;
         this.qolDiagLabel.height = 22;
         this.qolDiagLabel.x = 8;
         this.qolDiagLabel.y = 8;
         this.qolDiagLabel.selectable = false;
         this.qolDiagLabel.mouseEnabled = false;
         this.qolDiagLabel.visible = false;
         this.§else const native§.addChild(this.qolDiagLabel);
         this.qolDiagLastMs = getTimer();
         this.qolLoadBestTime();''','diagnostic HUD install')
helpers=r'''      private function qolStatusText() : String
      {
         return "PAUSED | " + (Level.qolSpeed == 3 ? "3x" : "1x") + " | TA " + (Level.qolTimeAttackEnabled ? "ON" : "off") + " | recycle " + (Level.qolRecycleEnemies ? "ON" : "off") + " | unlimited " + (this.qolUnlimitedMode ? "ON" : "off");
      }
      
      private function qolDiagnosticsFrame() : void
      {
         this.qolDiagFrames++;
         var now:int = getTimer();
         var elapsed:int = now - this.qolDiagLastMs;
         if(elapsed >= 500)
         {
            this.qolDiagFps = this.qolDiagFrames * 1000 / elapsed;
            this.qolDiagFrames = 0;
            this.qolDiagLastMs = now;
            if(this.qolDiagLabel != null) this.qolDiagLabel.text = "FPS " + this.qolDiagFps.toFixed(1) + " | entities " + this.entities.numChildren + " | bullets " + this.bullets.numChildren + " | towers " + this.qolTowerCount();
         }
         if(this.qolDiagLabel != null) this.qolDiagLabel.visible = this.qolDiagEnabled;
      }
      
      private function qolTowerCount() : int
      {
         var n:int = 0;
         var tower:§_-5u§ = null;
         for each(tower in this.towers) n++;
         return n;
      }
      
      private function qolIsMapSpecial(param1:Object) : Boolean
      {
         var name:String = getQualifiedClassName(param1);
         return name == "TowerDwarfRiflemen" || name == "TowerSoldierPirates" || name == "§_-Zs§" || name == "§_-MR§" || name == "§_-Xb§" || name == "§return const if§" || name == "§override import§";
      }
      
      private function qolClearAllEnemies() : void
      {
         var victims:Array = [];
         var enemy:Enemy = null;
         for each(enemy in this.enemies) if(enemy != null) victims.push(enemy);
         for each(enemy in victims) { enemy.isActive = false; enemy.destroyThis(); }
      }
      
      private function qolSellAllMapSpecials() : void
      {
         var victims:Array = [];
         var tower:§_-5u§ = null;
         for each(tower in this.towers) if(tower != null && this.qolIsMapSpecial(tower)) victims.push(tower);
         for each(tower in victims) tower.upgradeTower("sell");
      }
      
      private function qolApplyPreset(param1:String) : void
      {
         if(param1 == "normal")
         {
            Level.qolSpeed = 1; Level.qolTimeAttackEnabled = false; Level.qolRecycleEnemies = false; this.qolUnlimitedMode = false; this.qolDiagEnabled = false;
            this.qolHeavyEntities = 160; this.qolHeavyBullets = 200; this.qolExtremeEntities = 260; this.qolExtremeBullets = 330; this.qolUltraEntities = 520; this.qolUltraBullets = 680;
         }
         else if(param1 == "chaos")
         {
            Level.qolSpeed = 3; this.qolUnlimitedMode = true; this.qolDiagEnabled = true;
            this.qolHeavyEntities = 130; this.qolHeavyBullets = 165; this.qolExtremeEntities = 220; this.qolExtremeBullets = 280; this.qolUltraEntities = 420; this.qolUltraBullets = 540;
         }
         else if(param1 == "benchmark")
         {
            Level.qolSpeed = 3; this.qolUnlimitedMode = true; this.qolDiagEnabled = true; Level.qolTimeAttackEnabled = false;
            this.qolHeavyEntities = 160; this.qolHeavyBullets = 200; this.qolExtremeEntities = 260; this.qolExtremeBullets = 330; this.qolUltraEntities = 520; this.qolUltraBullets = 680;
         }
         else if(param1 == "timeattack")
         {
            Level.qolSpeed = 1; Level.qolRecycleEnemies = true; Level.qolTimeAttackEnabled = true; this.qolTimeAttackPending = this.indexWaves == 0 && !this.qolTimeAttackLaunched; this.qolDiagEnabled = true;
         }
         this.isReadyToWin = false; this.readyToWinTimeCounter = 0;
      }
      
'''
level=insert_before(level,'      private function qolRenderSettings() : void\n',helpers,'V11 helpers')
write('Level.as',level)
print('V11 level core patches applied')
