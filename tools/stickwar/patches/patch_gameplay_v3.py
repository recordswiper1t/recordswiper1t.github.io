#!/usr/bin/env python3
"""Finish Super Stick War's advertised mission families and campaign map.

Applied on top of the released V2 export.  The patch intentionally uses the
existing Stick War units, walls, AI and win/loss pipeline so objectives remain
compatible with campaign saves and the normal result screen.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


OBJECTIVE_FUNCTION = r'''      private function objectiveForTitle(title:String) : String
      {
         var escort:Array = ["Ambush at Dusk","The Healers' Road","Black River","Whiteout"];
         var siege:Array = ["Castle Approach","Siege of Westwind","Juggerknight Gate","Twin Fortresses","Iron Camp"];
         var assassinate:Array = ["Silent Knives","Broken Phalanx"];
         var interrupt:Array = ["Bone Oracle","Ritual Ground"];
         var defend:Array = ["Bombers in the Dark","New Empire"];
         if(escort.indexOf(title) >= 0) return "escort";
         if(siege.indexOf(title) >= 0) return "siege";
         if(assassinate.indexOf(title) >= 0) return "assassinate";
         if(interrupt.indexOf(title) >= 0) return "interrupt";
         if(defend.indexOf(title) >= 0) return "defend";
         if(title.indexOf("Benchmark") >= 0 || title == "Hundred Unit War") return "benchmark";
         if(title.indexOf("Crucible") >= 0 || title.indexOf("Gauntlet") >= 0 || title.indexOf("Stand") >= 0 || title.indexOf("Trial") >= 0 || title.indexOf("Rampage") >= 0) return "possession";
         if(title == "Miner's Fortune") return "economy";
         if(title.indexOf("Giant") >= 0 || title.indexOf("King") >= 0 || title.indexOf("Matriarch") >= 0 || title.indexOf("Prime") >= 0 || title.indexOf("Medusa") >= 0 || title == "Last Conquest" || title == "Second Crown") return "boss";
         if(title == "No Man's Land" || title.indexOf("Night") >= 0 || title == "Skyfall" || title == "Hollow Legion" || title == "War Mammoths" || title == "Rifle Line") return "survive";
         return "destroy";
      }
'''


def patch_gameplay(path: Path) -> None:
    text = read(path)
    if "SUPER STICK WAR GAMEPLAY V3" in text:
        return
    text = once(
        text,
        "   import flash.net.SharedObject;\n",
        "   import flash.net.SharedObject;\n   import flash.text.TextField;\n   import flash.text.TextFormat;\n",
        "text imports",
    )
    text = once(
        text,
        "      private var _superTimeRecorded:Boolean;\n",
        """      private var _superTimeRecorded:Boolean;

      // SUPER STICK WAR GAMEPLAY V3
      private var _superObjectiveTarget:Unit;

      private var _superEscort:Unit;

      private var _superSiegeWalls:Array;

      private var _superObjectiveLimit:int;

      private var _superObjectiveResolved:Boolean;

      private var _superObjectiveHud:TextField;
""",
        "objective fields",
    )
    start = text.index("      private function objectiveForTitle(title:String) : String")
    end = text.index("      private function bossTypeForTitle", start)
    text = text[:start] + OBJECTIVE_FUNCTION + "      \n" + text[end:]

    text = once(
        text,
        """         this._superTimeAttack = false;
         this._superTimeRecorded = false;
         if(this._superObjective == "boss")
""",
        """         this._superTimeAttack = false;
         this._superTimeRecorded = false;
         this._superObjectiveTarget = null;
         this._superEscort = null;
         this._superSiegeWalls = [];
         this._superObjectiveLimit = 0;
         this._superObjectiveResolved = false;
         this.installObjectiveHud();
         if(this._superObjective == "boss")
""",
        "objective initialization",
    )
    text = once(
        text,
        """         else if(this._superObjective == "survive")
         {
            userInterface.helpMessage.showMessage("SURVIVE — hold until the timer expires");
         }
         else if(this._superObjective == "economy")
""",
        """         else if(this._superObjective == "survive" || this._superObjective == "defend")
         {
            this._superObjectiveLimit = main.campaign.getCurrentLevel().title == "Long Night" ? 3600 : 1800;
            userInterface.helpMessage.showMessage(this._superObjective == "defend" ? "DEFEND — keep your statue standing through every assault" : "SURVIVE — hold until the timer expires");
         }
         else if(this._superObjective == "escort")
         {
            this._superObjectiveLimit = 1800;
            this._superEscort = this.spawnSuperUnit(this.team,this.team.type == Team.T_CHAOS ? Unit.U_KNIGHT : Unit.U_SPEARTON,4,1.35);
            this._superEscort.x = this._superEscort.px = this.team.homeX + this.team.direction * 520;
            this.team.attack(false);
            userInterface.helpMessage.showMessage("ESCORT — keep the marked champion alive until the route is secured");
         }
         else if(this._superObjective == "assassinate")
         {
            this._superObjectiveTarget = this.spawnSuperUnit(this.team.enemyTeam,this.bossTypeForTitle(main.campaign.getCurrentLevel().title),5,1.6);
            this.team.enemyTeam.statue.maxHealth = 100000000;
            this.team.enemyTeam.statue.health = 100000000;
            userInterface.helpMessage.showMessage("ASSASSINATE — eliminate the enemy commander; the statue is only a decoy");
         }
         else if(this._superObjective == "interrupt")
         {
            this._superObjectiveLimit = 1500;
            this._superObjectiveTarget = this.spawnSuperUnit(this.team.enemyTeam,Unit.U_SKELATOR,5.5,1.4);
            this.team.enemyTeam.statue.maxHealth = 100000000;
            this.team.enemyTeam.statue.health = 100000000;
            userInterface.helpMessage.showMessage("INTERRUPT — destroy the ritual caster before the channel completes");
         }
         else if(this._superObjective == "siege")
         {
            var wallIndex:int = 0;
            while(wallIndex < 3)
            {
               var siegeWall:Wall = this.team.enemyTeam.addWall(this.team.enemyTeam.homeX - 500 - wallIndex * 380);
               siegeWall.setConstructionAmount(1);
               siegeWall.maxHealth = int(siegeWall.maxHealth * (1.5 + main.campaign.currentLevel * 0.025));
               siegeWall.health = siegeWall.maxHealth;
               this._superSiegeWalls.push(siegeWall);
               wallIndex++;
            }
            this.team.enemyTeam.statue.maxHealth = 100000000;
            this.team.enemyTeam.statue.health = 100000000;
            userInterface.helpMessage.showMessage("SIEGE — breach all three fortified walls to win");
         }
         else if(this._superObjective == "economy")
""",
        "new objective setup",
    )

    helper = r'''      private function installObjectiveHud() : void
      {
         if(this._superObjectiveHud != null && this._superObjectiveHud.parent != null) this._superObjectiveHud.parent.removeChild(this._superObjectiveHud);
         this._superObjectiveHud = new TextField();
         this._superObjectiveHud.defaultTextFormat = new TextFormat("_sans",14,16774620,true);
         this._superObjectiveHud.background = true;
         this._superObjectiveHud.backgroundColor = 1118481;
         this._superObjectiveHud.border = true;
         this._superObjectiveHud.borderColor = 13870409;
         this._superObjectiveHud.x = 210;
         this._superObjectiveHud.y = 8;
         this._superObjectiveHud.width = 430;
         this._superObjectiveHud.height = 26;
         this._superObjectiveHud.selectable = false;
         this._superObjectiveHud.mouseEnabled = false;
         addChild(this._superObjectiveHud);
         this.updateObjectiveHud();
      }

      private function objectiveSecondsLeft() : int
      {
         return Math.max(0,Math.ceil((this._superObjectiveLimit - (game.frame - this._superObjectiveStart)) / 30));
      }

      private function updateObjectiveHud() : void
      {
         if(this._superObjectiveHud == null) return;
         var label:String = this._superObjective.toUpperCase();
         if(this._superObjective == "survive" || this._superObjective == "defend" || this._superObjective == "escort" || this._superObjective == "interrupt") label += "  •  " + this.objectiveSecondsLeft() + "s";
         if(this._superObjective == "economy") label += "  •  " + this.team.gold + " / " + this._superEconomyTarget + " gold";
         if(this._superObjective == "siege") label += "  •  " + this.livingSiegeWalls() + " walls remaining";
         if(this._superObjective == "assassinate") label += "  •  commander " + (this._superObjectiveTarget != null && this._superObjectiveTarget.isAlive() ? "alive" : "defeated");
         this._superObjectiveHud.text = "  OBJECTIVE: " + label;
      }

      private function livingSiegeWalls() : int
      {
         var wall:Wall = null;
         var alive:int = 0;
         for each(wall in this._superSiegeWalls) if(wall != null && wall.isAlive()) alive++;
         return alive;
      }

      private function objectiveWin() : void
      {
         if(this._superObjectiveResolved) return;
         this._superObjectiveResolved = true;
         this.team.enemyTeam.statue.health = Math.min(this.team.enemyTeam.statue.health,1);
         this.team.enemyTeam.statue.damage(0,100000000,null);
      }

      private function objectiveLose() : void
      {
         if(this._superObjectiveResolved) return;
         this._superObjectiveResolved = true;
         this.team.statue.damage(0,100000000,null);
      }

'''
    text = once(text, "      private function livingEnemyCombat() : int\n", helper + "      private function livingEnemyCombat() : int\n", "objective helpers")

    update_start = text.index("      private function updateSuperObjective() : void")
    update_end = text.index("      private function applyBattleLabPreset", update_start)
    new_update = r'''      private function updateSuperObjective() : void
      {
         var w:int = 0;
         var elapsed:int = game.frame - this._superObjectiveStart;
         if((game.frame & 15) == 0) this.updateObjectiveHud();
         if(this._superTimeAttack && elapsed > 30 && this.livingEnemyCombat() == 0)
         {
            this.recordTimeAttack();
            this.objectiveWin();
            this._superTimeAttack = false;
         }
         if(this._superObjective == "boss" && !this._superBossResolved && (this._superBoss == null || !this._superBoss.isAlive()))
         {
            this._superBossResolved = true;
            this.objectiveWin();
         }
         else if(this._superObjective == "survive" || this._superObjective == "defend")
         {
            if(elapsed >= this._superObjectiveLimit) this.objectiveWin();
            else if(game.frame >= this._superNextWave)
            {
               this._superNextWave += this._superObjective == "defend" ? 240 : 300;
               w = 0;
               while(w < 4 + int(elapsed / 600))
               {
                  var waveUnit:Unit = this.spawnSuperUnit(this.team.enemyTeam,this.team.enemyTeam.type == Team.T_CHAOS ? (w % 3 == 0 ? Unit.U_BOMBER : (w % 2 == 0 ? Unit.U_CAT : Unit.U_DEAD)) : (w % 2 == 0 ? Unit.U_SWORDWRATH : Unit.U_ARCHER));
                  waveUnit.y = waveUnit.py = game.map.height * (w % 2 == 0 ? 0.32 : 0.68);
                  w++;
               }
               this.team.enemyTeam.attack(false);
            }
         }
         else if(this._superObjective == "escort")
         {
            if(this._superEscort == null || !this._superEscort.isAlive()) this.objectiveLose();
            else if(elapsed >= this._superObjectiveLimit) this.objectiveWin();
            else if(game.frame >= this._superNextWave)
            {
               this._superNextWave += 270;
               w = 0;
               while(w < 3 + int(elapsed / 750))
               {
                  var ambusher:Unit = this.spawnSuperUnit(this.team.enemyTeam,w % 2 == 0 ? this.team.enemyTeam.getMinerType() : this.bossTypeForTitle("Silent Knives"));
                  ambusher.y = ambusher.py = game.map.height * (w % 2 == 0 ? 0.28 : 0.72);
                  w++;
               }
               this.team.enemyTeam.attack(false);
            }
         }
         else if(this._superObjective == "assassinate")
         {
            if(this._superObjectiveTarget == null || !this._superObjectiveTarget.isAlive()) this.objectiveWin();
         }
         else if(this._superObjective == "interrupt")
         {
            if(this._superObjectiveTarget == null || !this._superObjectiveTarget.isAlive()) this.objectiveWin();
            else if(elapsed >= this._superObjectiveLimit) this.objectiveLose();
            else if(game.frame >= this._superNextWave)
            {
               this._superNextWave += 300;
               this.spawnSuperUnit(this.team.enemyTeam,Unit.U_DEAD);
               this.spawnSuperUnit(this.team.enemyTeam,Unit.U_SKELATOR);
               this.team.enemyTeam.attack(false);
            }
         }
         else if(this._superObjective == "siege")
         {
            if(this.livingSiegeWalls() == 0) this.objectiveWin();
         }
         else if(this._superObjective == "economy" && this.team.gold >= this._superEconomyTarget) this.objectiveWin();
         else if(this._superObjective == "possession" && elapsed > 180 && !userInterface.possessMode && elapsed % 300 == 0) userInterface.helpMessage.showMessage("Press F on one selected unit for direct control");
         else if(this._superObjective == "benchmark" && elapsed > 2700) this.objectiveWin();
      }

'''
    text = text[:update_start] + new_update + text[update_end:]

    text = once(
        text,
        """      override public function leave() : void
      {
         this.cleanUp();
      }
""",
        """      override public function leave() : void
      {
         if(this._superObjectiveHud != null && this._superObjectiveHud.parent != null) this._superObjectiveHud.parent.removeChild(this._superObjectiveHud);
         this._superObjectiveHud = null;
         this.cleanUp();
      }
""",
        "objective HUD cleanup",
    )
    write(path, text)


def patch_campaign_map(path: Path) -> None:
    text = read(path)
    if "SUPER CAMPAIGN ATLAS V3" in text:
        return
    text = once(text, "   import flash.display.MovieClip;\n", "   import flash.display.*;\n   import flash.text.*;\n", "map display imports")
    text = once(
        text,
        "      private var keyboard:KeyboardState;\n",
        """      private var keyboard:KeyboardState;

      // SUPER CAMPAIGN ATLAS V3
      private var superAtlas:Sprite;

      private var superChapterPage:int = 0;
""",
        "atlas fields",
    )
    text = once(
        text,
        """         this.mc.title.mouseEnabled = false;
         if(this.main.campaign.currentLevel == 0)
""",
        """         this.mc.title.mouseEnabled = false;
         this.superChapterPage = this.superChapterForStage(this.main.campaign.currentLevel);
         this.renderSuperAtlas();
         if(this.main.campaign.currentLevel == 0)
""",
        "atlas install",
    )
    helpers = r'''      private function atlasText(label:String,xPos:Number,yPos:Number,width:Number,height:Number,size:int = 12,color:uint = 16777215) : TextField
      {
         var field:TextField = new TextField();
         field.defaultTextFormat = new TextFormat("_sans",size,color,true);
         field.text = label;
         field.x = xPos;
         field.y = yPos;
         field.width = width;
         field.height = height;
         field.selectable = false;
         field.mouseEnabled = false;
         return field;
      }

      private function atlasButton(label:String,action:String,xPos:Number,yPos:Number,width:Number) : Sprite
      {
         var button:Sprite = new Sprite();
         button.name = action;
         button.x = xPos;
         button.y = yPos;
         button.graphics.lineStyle(2,13870409,1);
         button.graphics.beginFill(1183245,0.97);
         button.graphics.drawRoundRect(0,0,width,34,8,8);
         button.graphics.endFill();
         button.addChild(this.atlasText(label,8,7,width - 16,20,11,16774620));
         button.buttonMode = true;
         button.mouseChildren = false;
         return button;
      }

      private function superChapterForStage(stage:int) : int
      {
         var limits:Array = [12,18,26,36,45,55,65];
         var i:int = 0;
         while(i < limits.length - 1 && stage >= int(limits[i])) i++;
         return i;
      }

      private function renderSuperAtlas() : void
      {
         if(this.superAtlas != null && this.superAtlas.parent != null) this.superAtlas.parent.removeChild(this.superAtlas);
         var starts:Array = [0,12,18,26,36,45,55];
         var ends:Array = [12,18,26,36,45,55,65];
         var names:Array = ["THE CONQUEST","THE REBELLION","RISE OF CHAOS","AFTERMATH","NORTHERN INAMORTA","ENDGAME","WAR GAMES"];
         this.superChapterPage = Math.max(0,Math.min(6,this.superChapterPage));
         var panel:Sprite = new Sprite();
         panel.x = 438;
         panel.y = 42;
         panel.graphics.lineStyle(3,13870409,1);
         panel.graphics.beginFill(460551,0.94);
         panel.graphics.drawRoundRect(0,0,392,238,14,14);
         panel.graphics.endFill();
         panel.addChild(this.atlasText("CAMPAIGN ATLAS  •  " + (this.superChapterPage + 1) + "/7",16,12,360,25,17,16774620));
         panel.addChild(this.atlasText(String(names[this.superChapterPage]),16,40,360,22,13,16777215));
         var first:int = int(starts[this.superChapterPage]);
         var last:int = int(ends[this.superChapterPage]);
         var i:int = first;
         while(i < last)
         {
            var local:int = i - first;
            var node:Sprite = new Sprite();
            node.x = 18 + local % 5 * 71;
            node.y = 74 + int(local / 5) * 54;
            var state:int = i < this.main.campaign.currentLevel ? 2 : (i == this.main.campaign.currentLevel ? 1 : 0);
            node.graphics.lineStyle(2,state == 1 ? 16763904 : 13870409,1);
            node.graphics.beginFill(state == 2 ? 2647080 : (state == 1 ? 8018944 : 1052688),1);
            node.graphics.drawCircle(22,18,18);
            node.graphics.endFill();
            node.addChild(this.atlasText(String(i + 1),8,8,28,22,11,state == 0 ? 8421504 : 16777215));
            if(state == 1) { node.name = "atlas_play"; node.buttonMode = true; node.mouseChildren = false; }
            panel.addChild(node);
            i++;
         }
         panel.addChild(this.atlasButton("◀ CHAPTER","atlas_prev",16,194,112));
         panel.addChild(this.atlasButton("PLAY CURRENT","atlas_play",140,194,112));
         panel.addChild(this.atlasButton("CHAPTER ▶","atlas_next",264,194,112));
         this.superAtlas = panel;
         addChild(panel);
      }

'''
    text = once(text, "      private function strategyGuideClick(e:Event) : void\n", helpers + "      private function strategyGuideClick(e:Event) : void\n", "atlas helpers")
    text = once(
        text,
        """      private function click(evt:MouseEvent) : void
      {
         if(evt.target == this.mc.map.playbuttonflag && (this.main.campaign.currentLevel >= 13 || this.mc.currentFrameLabel == "level" + (this.main.campaign.currentLevel + 1)))
""",
        """      private function click(evt:MouseEvent) : void
      {
         var action:String = evt.target is DisplayObject ? DisplayObject(evt.target).name : "";
         if(action == "atlas_prev") { this.superChapterPage = (this.superChapterPage + 6) % 7; this.renderSuperAtlas(); return; }
         if(action == "atlas_next") { this.superChapterPage = (this.superChapterPage + 1) % 7; this.renderSuperAtlas(); return; }
         if(action == "atlas_play") { this.clickPlay(null); return; }
         if(evt.target == this.mc.map.playbuttonflag && (this.main.campaign.currentLevel >= 13 || this.mc.currentFrameLabel == "level" + (this.main.campaign.currentLevel + 1)))
""",
        "atlas clicks",
    )
    text = once(
        text,
        """         removeEventListener(MouseEvent.CLICK,this.click);
         this.mc.bottomPanel.campaignButtons.autoSaveEnabled.removeEventListener(MouseEvent.CLICK,this.disableSave);
""",
        """         removeEventListener(MouseEvent.CLICK,this.click);
         if(this.superAtlas != null && this.superAtlas.parent != null) this.superAtlas.parent.removeChild(this.superAtlas);
         this.superAtlas = null;
         this.mc.bottomPanel.campaignButtons.autoSaveEnabled.removeEventListener(MouseEvent.CLICK,this.disableSave);
""",
        "atlas cleanup",
    )
    write(path, text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scripts", type=Path)
    args = parser.parse_args()
    campaign = args.scripts / "com" / "brockw" / "stickwar" / "campaign"
    gameplay = campaign / "CampaignGameScreen.as"
    campaign_map = campaign / "CampaignScreen.as"
    patch_gameplay(gameplay)
    patch_campaign_map(campaign_map)
    checks = {
        gameplay: ["SUPER STICK WAR GAMEPLAY V3", 'return "escort"', 'return "siege"', 'return "assassinate"', 'return "interrupt"', 'return "defend"', "installObjectiveHud", "objectiveLose"],
        campaign_map: ["SUPER CAMPAIGN ATLAS V3", "CAMPAIGN ATLAS", "atlas_play", "superChapterForStage"],
    }
    for path, needles in checks.items():
        data = read(path)
        for needle in needles:
            if needle not in data:
                raise SystemExit(f"validation failed: {needle!r} missing from {path}")
    print("Super Stick War gameplay V3 objectives and seven-chapter campaign atlas applied")


if __name__ == "__main__":
    main()
