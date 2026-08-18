#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys


def die(msg):
    raise SystemExit(msg)


def read(root, name):
    p = root / name
    if not p.exists():
        die(f"missing exported source: {p}")
    return p.read_text(encoding="utf-8")


def write(out, name, text):
    p = out / "scripts" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        die(f"{label}: expected exactly one anchor, found {n}")
    return text.replace(old, new, 1)


def replace_between(text, start, end, replacement, label):
    a = text.find(start)
    if a < 0:
        die(f"{label}: start marker not found: {start}")
    b = text.find(end, a + len(start))
    if b < 0:
        die(f"{label}: end marker not found: {end}")
    return text[:a] + replacement.rstrip() + "\n\n      " + text[b:]


def patch_game_upgrades(text):
    marker = "      public function §_-r7§() : void\n"
    helper = r'''      public function qolSetMaxed(param1:Boolean) : void
      {
         if(!param1)
         {
            this.§_-r7§();
            return;
         }
         this.archersUpLevel = 5;
         this.archersUpSalvage = true;
         this.archersUpEagleEye = true;
         this.archersUpPiercing = true;
         this.archersUpFarShots = true;
         this.archersUpPrecision = true;
         this.barracksUpLevel = 5;
         this.barracksUpSurvival = true;
         this.barracksUpBetterArmor = true;
         this.barracksUpImprovedDeployment = true;
         this.barracksUpBarbedArmor = true;
         this.barracksUpSurvival2 = true;
         this.magesUpLevel = 5;
         this.§final const implements§ = true;
         this.§_-G0§ = true;
         this.§_-i7§ = true;
         this.§_-dC§ = true;
         this.magesUpSlowCurse = true;
         this.engineersUpLevel = 5;
         this.engineersUpConcentratedFire = true;
         this.engineersUpRangeFinder = true;
         this.engineersUpFieldLogistics = true;
         this.engineersUpIndustrialization = true;
         this.engineersUpEfficiency = true;
         this.rainUpLevel = 5;
         this.rainUpBlazingSkies = true;
         this.§_-M9§ = true;
         this.§_-YK§ = true;
         this.§continue const final§ = true;
         this.rainUpCataclysm = true;
         this.reinforcementLevel = 5;
      }
      
'''
    return once(text, marker, helper + marker, "GameUpgrades.qolSetMaxed")


def patch_hero_data(text):
    marker = "      public function §_-oq§(param1:Object) : Number\n"
    helper = r'''      public function qolSetSkillsMaxed(param1:Boolean) : void
      {
         var heroes:Array = [this.heroAlric,this.heroMirage,this.heroCronan,this.heroCaptain,this.heroNivus,this.heroDierdre,this.heroGrawl,this.heroShatra,this.heroAshbite];
         var h:Object = null;
         var skill:Object = null;
         for each(h in heroes)
         {
            for each(skill in h.skillArray)
            {
               skill.level = param1 ? 3 : 0;
            }
         }
         this.updateSkillPoints();
      }
      
'''
    return once(text, marker, helper + marker, "hero data qolSetSkillsMaxed")


def patch_game(text):
    text = once(
        text,
        "      public var stars:int = 65;\n",
        "      public var stars:int = 65;\n      \n      public var qolTreesMaxed:Boolean = true;\n",
        "game qolTreesMaxed field",
    )
    text = once(
        text,
        "         this.§_-gp§();\n         this.stars = this.qolRemainingUpgradeStars();\n",
        "         this.§_-gp§();\n         this.qolSetTreesMaxed(true);\n",
        "game default auto max",
    )
    marker = "      private function qolRemainingUpgradeStars() : int\n"
    helper = r'''      public function qolSetTreesMaxed(param1:Boolean) : void
      {
         this.qolTreesMaxed = param1;
         this.gameUpgrades.qolSetMaxed(param1);
         this.gameHeroData.qolSetSkillsMaxed(param1);
         this.stars = param1 ? 0 : this.qolRemainingUpgradeStars();
      }
      
'''
    text = once(text, marker, helper + marker, "game qolSetTreesMaxed")
    return text


LEVEL_RENDER = r'''      private function qolRenderSettings() : void
      {
         if(this.qolSettings == null)
         {
            return;
         }
         while(this.qolSettings.numChildren > 0)
         {
            this.qolSettings.removeChildAt(0);
         }
         this.qolSettings.graphics.clear();
         this.qolSettings.graphics.beginFill(1118481,0.97);
         this.qolSettings.graphics.lineStyle(2,13983051,0.8);
         this.qolSettings.graphics.drawRoundRect(0,0,580,455,18,18);
         this.qolSettings.graphics.endFill();
         if(this.qolSettingsPage == 0)
         {
            this.qolSettings.addChild(this.qolLabel("V4 LEVEL SETTINGS",28,20,24));
            this.qolSettings.addChild(this.qolButton("Speed: " + (Level.qolSpeed == 3 ? "3x" : "1x"),28,72,250,"speed"));
            this.qolSettings.addChild(this.qolButton(this.game.qolTreesMaxed ? "Trees: MAXED (reset)" : "Trees: RESET (max)",302,72,250,"trees_toggle"));
            this.qolSettings.addChild(this.qolLabel("Add gold:",28,142,18));
            this.qolGoldInput = this.qolInput("0",130,130,215);
            this.qolSettings.addChild(this.qolGoldInput);
            this.qolSettings.addChild(this.qolButton("ADD",360,130,192,"gold_add"));
            this.qolSettings.addChild(this.qolButton("Hero selection  →",28,202,250,"page_heroes"));
            this.qolSettings.addChild(this.qolButton(this.qolSendAllPending ? "Sending all waves…" : "Send all waves",302,202,250,"all_waves"));
            this.qolSettings.addChild(this.qolButton("Enemy tools  →",28,262,250,"page_enemy"));
            this.qolSettings.addChild(this.qolButton("Hide V4 tools",302,262,250,"hide"));
            this.qolSettings.addChild(this.qolLabel("Next-wave flags now appear immediately after the previous wave is sent.",28,330,14));
            this.qolSettings.addChild(this.qolLabel("Send-all is paced across frames to reduce Ruffle spikes.",28,354,14));
         }
         else if(this.qolSettingsPage == 1)
         {
            this.qolSettings.addChild(this.qolLabel("CUSTOM ENEMY ROUND",28,20,24));
            var shortName:String = String(this.qolEnemies[this.qolEnemyIndex]).replace("Enemy","");
            this.qolSettings.addChild(this.qolButton("<",28,72,58,"enemy_prev"));
            this.qolSettings.addChild(this.qolButton(shortName,98,72,384,"noop"));
            this.qolSettings.addChild(this.qolButton(">",494,72,58,"enemy_next"));
            this.qolSettings.addChild(this.qolLabel("Count: " + this.qolEnemyCount,28,142,18));
            this.qolSettings.addChild(this.qolButton("-5",220,130,78,"count_minus"));
            this.qolSettings.addChild(this.qolButton("+5",310,130,78,"count_plus"));
            this.qolSettings.addChild(this.qolLabel("Path: " + (this.qolEnemyPath + 1),28,204,18));
            this.qolSettings.addChild(this.qolButton("Prev path",220,192,110,"path_prev"));
            this.qolSettings.addChild(this.qolButton("Next path",342,192,110,"path_next"));
            this.qolSettings.addChild(this.qolButton("SEND CUSTOM ROUND",28,270,524,"send_custom"));
            this.qolSettings.addChild(this.qolButton("←  Main settings",165,350,250,"page_main"));
         }
         else
         {
            this.qolEnsureHeroSelection();
            this.qolSettings.addChild(this.qolLabel("HEROES FOR THIS GAME",28,20,24));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("alric","Alric"),28,72,250,"hero_alric"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("mirage","Mirage"),302,72,250,"hero_mirage"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("captain","Blackthorne"),28,120,250,"hero_captain"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("cronan","Cronan"),302,120,250,"hero_cronan"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("shatra","Sha'tra"),28,168,250,"hero_shatra"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("grawl","Grawl"),302,168,250,"hero_grawl"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("nivus","Nivus"),28,216,250,"hero_nivus"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("dierdre","Dierdre"),302,216,250,"hero_dierdre"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("ashbite","Ashbite"),28,264,250,"hero_ashbite"));
            this.qolSettings.addChild(this.qolLabel("This Flash build contains 9 regular hero implementations.",28,326,14));
            this.qolSettings.addChild(this.qolButton("←  Main settings",165,374,250,"page_main"));
         }
      }'''


LEVEL_CLICK = r'''      private function qolSettingsClick(param1:MouseEvent) : void
      {
         var action:String = Sprite(param1.currentTarget).name;
         if(action == "speed")
         {
            Level.qolSpeed = Level.qolSpeed == 1 ? 3 : 1;
         }
         else if(action == "gold_add")
         {
            var amount:Number = this.qolGoldInput == null ? 0 : Number(this.qolGoldInput.text);
            if(isNaN(amount) || amount < 0)
            {
               amount = 0;
            }
            this.updateCash(int(Math.min(2000000000,amount)));
         }
         else if(action == "trees_toggle")
         {
            this.game.qolSetTreesMaxed(!this.game.qolTreesMaxed);
         }
         else if(action == "page_heroes")
         {
            this.qolSettingsPage = 2;
         }
         else if(action.indexOf("hero_") == 0)
         {
            this.qolToggleHero(action.substr(5));
         }
         else if(action == "all_waves")
         {
            this.qolSendAllWaves();
         }
         else if(action == "page_enemy")
         {
            this.qolSettingsPage = 1;
         }
         else if(action == "page_main")
         {
            this.qolSettingsPage = 0;
         }
         else if(action == "enemy_prev")
         {
            this.qolEnemyIndex = (this.qolEnemyIndex + this.qolEnemies.length - 1) % this.qolEnemies.length;
         }
         else if(action == "enemy_next")
         {
            this.qolEnemyIndex = (this.qolEnemyIndex + 1) % this.qolEnemies.length;
         }
         else if(action == "count_minus")
         {
            this.qolEnemyCount = Math.max(1,this.qolEnemyCount - 5);
         }
         else if(action == "count_plus")
         {
            this.qolEnemyCount = Math.min(200,this.qolEnemyCount + 5);
         }
         else if(action == "path_prev")
         {
            this.qolEnemyPath = Math.max(0,this.qolEnemyPath - 1);
         }
         else if(action == "path_next")
         {
            this.qolEnemyPath = Math.min(Math.max(0,this.§_-V8§.length - 1),this.qolEnemyPath + 1);
         }
         else if(action == "send_custom")
         {
            this.qolSendCustomRound();
         }
         else if(action == "hide")
         {
            this.qolHideSettings();
            return;
         }
         this.qolRenderSettings();
      }'''


LEVEL_SEND_ALL = r'''      private function qolSendAllWaves() : void
      {
         this.qolSendAllPending = this.indexWaves < this.waves.length;
         this.qolSendAllCooldown = 0;
         this.qolSendQueuedWave();
      }
      
      private function qolSendQueuedWave() : void
      {
         if(!this.qolSendAllPending)
         {
            return;
         }
         if(this.indexWaves >= this.waves.length)
         {
            this.qolSendAllPending = false;
            this.menu.§return var§();
            return;
         }
         ++this.§_-g3§;
         this.activeWaves[this.waves[this.indexWaves]] = this.waves[this.indexWaves];
         this.intervalWaveCounter = 0;
         ++this.indexWaves;
         this.§_-rd§.updateWaves(this.§_-g3§,this.maxWaves);
         if(this.indexWaves >= this.waves.length)
         {
            this.qolSendAllPending = false;
            this.menu.§return var§();
         }
      }'''


LEVEL_HERO_SPAWN = r'''      private function qolSpawnExtraHeroes() : void
      {
         this.qolEnsureHeroSelection();
         var roster:Array = ["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite"];
         var primary:String = this.game.gameHeroData.selectedHero.name;
         var i:int = 0;
         for each(var heroName:String in roster)
         {
            if(heroName != primary && Boolean(Level.qolHeroEnabled[heroName]))
            {
               var h:§dynamic const class§ = this.qolMakeHero(heroName,i + 1);
               if(h != null)
               {
                  this.entities.addChild(h);
                  this.qolExtraHeroes.push(h);
                  i++;
               }
            }
         }
      }'''


LEVEL_HERO_APPLY = r'''      private function qolApplyHeroCount() : void
      {
         this.qolApplyHeroSelection();
      }
      
      private function qolEnsureHeroSelection() : void
      {
         if(Level.qolHeroEnabled != null)
         {
            return;
         }
         Level.qolHeroEnabled = {};
         var roster:Array = ["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite"];
         for each(var heroName:String in roster)
         {
            Level.qolHeroEnabled[heroName] = false;
         }
         Level.qolHeroEnabled[this.game.gameHeroData.selectedHero.name] = true;
      }
      
      private function qolHeroLabel(param1:String, param2:String) : String
      {
         this.qolEnsureHeroSelection();
         return param2 + ": " + (Boolean(Level.qolHeroEnabled[param1]) ? "ON" : "off");
      }
      
      private function qolToggleHero(param1:String) : void
      {
         this.qolEnsureHeroSelection();
         Level.qolHeroEnabled[param1] = !Boolean(Level.qolHeroEnabled[param1]);
         this.qolApplyHeroSelection();
      }
      
      private function qolApplyHeroSelection() : void
      {
         this.qolEnsureHeroSelection();
         while(this.qolExtraHeroes.length > 0)
         {
            var oldHero:§dynamic const class§ = this.qolExtraHeroes.pop();
            if(oldHero != null && oldHero.parent != null)
            {
               oldHero.parent.removeChild(oldHero);
            }
         }
         var primary:String = this.game.gameHeroData.selectedHero.name;
         if(Boolean(Level.qolHeroEnabled[primary]))
         {
            if(this.hero == null)
            {
               this.switchHeroes();
            }
            if(this.hero != null && this.hero.parent == null)
            {
               this.entities.addChild(this.hero);
            }
         }
         else if(this.hero != null && this.hero.parent != null)
         {
            this.hero.parent.removeChild(this.hero);
         }
         this.qolSpawnExtraHeroes();
      }'''


LEVEL_OD = r'''      public function §_-OD§() : void
      {
         this.qolEnsureHeroSelection();
         var primary:String = this.game.gameHeroData.selectedHero.name;
         if(Boolean(Level.qolHeroEnabled[primary]))
         {
            this.switchHeroes();
            if(this.hero != null)
            {
               this.entities.addChild(this.hero);
            }
         }
         this.§continue const function§ = true;
         this.qolSpawnExtraHeroes();
         if(this.hero != null && this.hero.parent != null)
         {
            this.§_-9B§();
         }
      }'''


def patch_level(text):
    text = once(
        text,
        "      public static var qolHeroCount:int = 1;\n",
        "      public static var qolHeroCount:int = 1;\n      \n      public static var qolHeroEnabled:Object = null;\n",
        "Level hero-selection field",
    )
    text = once(
        text,
        "      private var qolSettings:Sprite;\n",
        "      private var qolSettings:Sprite;\n      \n      private var qolGoldInput:TextField;\n      \n      private var qolSendAllPending:Boolean = false;\n      \n      private var qolSendAllCooldown:int = 0;\n",
        "Level V4 state fields",
    )
    text = replace_between(
        text,
        "      private function qolRenderSettings() : void\n",
        "      private function qolSettingsClick(param1:MouseEvent) : void\n",
        LEVEL_RENDER,
        "Level qolRenderSettings",
    )
    text = replace_between(
        text,
        "      private function qolSettingsClick(param1:MouseEvent) : void\n",
        "      private function qolSendCustomRound() : void\n",
        LEVEL_CLICK,
        "Level qolSettingsClick",
    )
    text = replace_between(
        text,
        "      private function qolSendAllWaves() : void\n",
        "      private function qolMakeHero(param1:String, param2:int) : §dynamic const class§\n",
        LEVEL_SEND_ALL,
        "Level paced send-all",
    )
    text = replace_between(
        text,
        "      private function qolSpawnExtraHeroes() : void\n",
        "      private function qolApplyHeroCount() : void\n",
        LEVEL_HERO_SPAWN,
        "Level hero spawn",
    )
    text = replace_between(
        text,
        "      private function qolApplyHeroCount() : void\n",
        "      public function eFrameEvents(param1:Event) : void\n",
        LEVEL_HERO_APPLY,
        "Level hero toggle application",
    )
    text = replace_between(
        text,
        "      public function §_-OD§() : void\n",
        "      public function switchHeroes() : void\n",
        LEVEL_OD,
        "Level initial hero selection",
    )
    text = once(
        text,
        "      private function qolLabel(param1:String, param2:Number, param3:Number, param4:int = 18) : TextField\n",
        r'''      private function qolInput(param1:String, param2:Number, param3:Number, param4:Number) : TextField
      {
         var tf:TextField = new TextField();
         tf.defaultTextFormat = new TextFormat("_sans",18,16777215,true);
         tf.type = "input";
         tf.restrict = "0-9";
         tf.maxChars = 10;
         tf.background = true;
         tf.backgroundColor = 2302755;
         tf.border = true;
         tf.borderColor = 11184810;
         tf.textColor = 16777215;
         tf.width = param4;
         tf.height = 42;
         tf.x = param2;
         tf.y = param3;
         tf.text = param1;
         return tf;
      }
      
      private function qolLabel(param1:String, param2:Number, param3:Number, param4:int = 18) : TextField
''',
        "Level gold input helper",
    )
    # For touch emulation under Ruffle, act on press rather than waiting for a full click gesture.
    text = once(
        text,
        "         b.addEventListener(MouseEvent.CLICK,this.qolSettingsClick,false,0,true);\n",
        "         b.addEventListener(MouseEvent.MOUSE_DOWN,this.qolSettingsClick,false,0,true);\n",
        "Level settings touch event",
    )
    # Show the next-wave flag immediately, rather than 50 frames into the countdown.
    text = once(
        text,
        "if(this.intervalWaveCounter == 50 && this.waves[this.indexWaves].interval != 0 || this.indexWaves == 0)",
        "if(this.intervalWaveCounter == 0 && this.waves[this.indexWaves].interval != 0 || this.indexWaves == 0)",
        "Level immediate wave flag condition",
    )
    text = once(
        text,
        "this.waves[this.indexWaves].showWaveFlag(this,this.waves[this.indexWaves].interval - 50,this.indexWaves);",
        "this.waves[this.indexWaves].showWaveFlag(this,this.waves[this.indexWaves].interval,this.indexWaves);",
        "Level immediate wave flag countdown",
    )
    # Pace send-all across frames. One wave is released every three eFrame ticks.
    eframe = "      public function eFrameEvents(param1:Event) : void\n      {\n"
    eframe_new = r'''      public function eFrameEvents(param1:Event) : void
      {
         if(this.qolSendAllPending)
         {
            if(this.qolSendAllCooldown <= 0)
            {
               this.qolSendQueuedWave();
               this.qolSendAllCooldown = 2;
            }
            else
            {
               --this.qolSendAllCooldown;
            }
         }
'''
    text = once(text, eframe, eframe_new, "Level send-all frame pacing")
    return text


TOWER_SPECIAL_BRANCH = r'''         if(param1 == "qol_specials")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwarf","tw_archer",250,false,0,0,0,1,"TooltipBasic",{
               "title":"Dwarf Riflemen — 250",
               "text":"Place the level-only Dwarf Riflemen tower."
            }),new Array("qol_pirates","tw_soldier",180,false,0,0,0,2,"TooltipBasic",{
               "title":"Pirate Barracks — 180",
               "text":"Place the level-only Pirate Barracks."
            }),new Array("qol_crossbow","tw_archer",this.cRoot.gameSettings.archers.crossbow.cost,false,0,0,0,3,"TooltipBasic",{
               "title":"Crossbow Fort",
               "text":"Build the Crossbow specialization directly."
            }),new Array("qol_totem","tw_archer",this.cRoot.gameSettings.archers.totem.cost,false,0,0,0,4,"TooltipBasic",{
               "title":"Tribal Axethrowers",
               "text":"Build the Totem specialization directly."
            }),new Array("qol_specials2","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"More special towers →",
               "text":"Open the second special-tower page."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
         if(param1 == "qol_specials2")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_archmage","tw_mage",this.cRoot.gameSettings.mages.archmage.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"Archmage",
               "text":"Build the Archmage specialization directly."
            }),new Array("qol_necro","tw_mage",this.cRoot.gameSettings.mages.necromancer.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Necromancer",
               "text":"Build the Necromancer specialization directly."
            }),new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,3,"TooltipBasic",{
               "title":"DWAARP",
               "text":"Build the DWAARP specialization directly."
            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,4,"TooltipBasic",{
               "title":"Battle-Mecha T200",
               "text":"Build the Battle-Mecha specialization directly."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← Special towers",
               "text":"Return to the first special-tower page."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
         if(param1 == "qol_dwarf")
         {
            if(this.cRoot.cash < 250)
            {
               return;
            }
            this.cRoot.updateCash(-250);
            this.qolPlaceSpecial(new TowerDwarfRiflemen(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
         if(param1 == "qol_pirates")
         {
            if(this.cRoot.cash < 180)
            {
               return;
            }
            this.cRoot.updateCash(-180);
            this.qolPlaceSpecial(new TowerSoldierPirates(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
         if(param1 == "qol_crossbow")
         {
            this.qolPlaceSpecial(new TowerArcherCrossbow(this.x,this.y + this.yAdjust,this.§_-EV§,0,this.canBuildBarracks));
            return;
         }
         if(param1 == "qol_totem")
         {
            this.qolPlaceSpecial(new TowerArcherTotem(this.x,this.y + this.yAdjust,this.§_-EV§,0,this.canBuildBarracks));
            return;
         }
         if(param1 == "qol_archmage")
         {
            this.qolPlaceSpecial(new TowerMageArchmage(this.x,this.y + this.yAdjust,this.§_-EV§,0,this.canBuildBarracks));
            return;
         }
         if(param1 == "qol_necro")
         {
            this.qolPlaceSpecial(new TowerMageNecromancer(this.x,this.y + this.yAdjust,this.§_-EV§,0,this.canBuildBarracks));
            return;
         }
         if(param1 == "qol_dwaarp")
         {
            this.qolPlaceSpecial(new TowerEngineerDwaarp(this.x,this.y + this.yAdjust,this.§_-EV§,0,this.canBuildBarracks));
            return;
         }
         if(param1 == "qol_mech")
         {
            this.qolPlaceSpecial(new TowerEngineerMech(this.x,this.y + this.yAdjust,this.§_-EV§,0,this.canBuildBarracks));
            return;
         }
'''


def patch_tower_holder(text):
    helper_marker = "      public function upgradeTower(param1:String) : void\n"
    helper = r'''      private function qolPlaceSpecial(param1:§_-5u§) : void
      {
         this.cRoot.entities.addChild(param1);
         this.cRoot.towers[param1] = param1;
         this.destroyThis();
      }
      
'''
    text = once(text, helper_marker, helper + helper_marker, "TowerHolder special placement helper")
    start = "         if(param1 == \"qol_specials\")\n         {\n"
    end = "         if(param1 == \"qol_back\")\n"
    a = text.find(start, text.find(helper_marker))
    if a < 0:
        die("TowerHolder old special branch start not found")
    b = text.find(end, a)
    if b < 0:
        die("TowerHolder old special branch end not found")
    text = text[:a] + TOWER_SPECIAL_BRANCH + "         " + text[b:]
    # The old back branch remains harmless, but it is not exposed by V4 pages.
    text = once(
        text,
        "this.removeEventListener(MouseEvent.CLICK,this.clickEvent);",
        "this.removeEventListener(MouseEvent.MOUSE_DOWN,this.clickEvent);",
        "TowerHolder listener cleanup",
    )
    return text


def patch_quick_menu(text):
    return once(
        text,
        '         if(param1 == "qol_specials")\n',
        '         if(param1 == "qol_specials" || param1 == "qol_specials2")\n',
        "quick menu special-page navigation",
    )


def patch(root, out):
    out_scripts = out / "scripts"
    if out.exists():
        shutil.rmtree(out)
    out_scripts.mkdir(parents=True)

    files = {
        "GameUpgrades.as": patch_game_upgrades(read(root, "GameUpgrades.as")),
        "§_-2i§.as": patch_hero_data(read(root, "§_-2i§.as")),
        "§_-BQ§.as": patch_game(read(root, "§_-BQ§.as")),
        "Level.as": patch_level(read(root, "Level.as")),
        "TowerHolder.as": patch_tower_holder(read(root, "TowerHolder.as")),
        "§_-LZ§.as": patch_quick_menu(read(root, "§_-LZ§.as")),
    }
    for name, text in files.items():
        write(out, name, text)
    print("patched", ", ".join(files))


def verify(root):
    checks = {
        "Level.as": [
            "qolHeroEnabled",
            "HEROES FOR THIS GAME",
            "private function qolSendQueuedWave",
            "intervalWaveCounter == 0",
            'tf.type = "input"',
            "qolSendAllCooldown = 2",
        ],
        "GameUpgrades.as": ["public function qolSetMaxed"],
        "§_-2i§.as": ["public function qolSetSkillsMaxed"],
        "§_-BQ§.as": ["public var qolTreesMaxed", "this.qolSetTreesMaxed(true)"],
        "TowerHolder.as": [
            "qol_specials2",
            "private function qolPlaceSpecial",
            "this.y + this.yAdjust",
            "Dwarf Riflemen — 250",
            "Battle-Mecha T200",
            "removeEventListener(MouseEvent.MOUSE_DOWN,this.clickEvent)",
        ],
        "§_-LZ§.as": ['param1 == "qol_specials" || param1 == "qol_specials2"'],
    }
    for name, needles in checks.items():
        text = read(root, name)
        for needle in needles:
            if needle not in text:
                die(f"verify failed: {name} missing {needle!r}")
    print("verification markers present")


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in {"patch", "verify"}:
        die("usage: build-v4.py patch <exported-scripts-root> <import-root> | verify <reexported-scripts-root>")
    if sys.argv[1] == "patch":
        if len(sys.argv) != 4:
            die("patch requires source root and import root")
        patch(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        verify(Path(sys.argv[2]))


if __name__ == "__main__":
    main()
