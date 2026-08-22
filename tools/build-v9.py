#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: build-v9.py <exported-v8-scripts-dir>')
scripts = Path(sys.argv[1])

def read(name):
    return (scripts / name).read_text(encoding='utf-8-sig')

def write(name, text):
    (scripts / name).write_text(text, encoding='utf-8', newline='\n')

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    return text.replace(old, new, 1)

level = read('Level.as')
level = replace_once(level, '      private var qolEnemyIndex:int = 0;', '      private var qolEnemyIndex:int = 0;\n      \n      private var qolEnemyPage:int = 0;', 'enemy page state')
level = replace_once(level, '      private var qolTowerClipboardAction:String = "";', '      private var qolTowerClipboardAction:String = "";\n      \n      private var qolSettingsOwnsPause:Boolean = false;\n      \n      private var qolTimeAttackPending:Boolean = false;\n      \n      private var qolSendAllAfterMenu:Boolean = false;', 'menu deferred state')
level = replace_once(level, '         this.qolTimerLabel.x = 562;\n         this.qolTimerLabel.y = 540;', '         this.qolTimerLabel.x = 317;\n         this.qolTimerLabel.y = 8;', 'timer position')
level = replace_once(level, '         this.addChild(this.qolTimerLabel);', '         this.§else const native§.addChild(this.qolTimerLabel);', 'timer overlay layer')
old = '''      private function qolShowSettings() : void
      {
         if(this.qolSettings == null)
         {
            this.qolSettings = new Sprite();
            this.qolSettings.x = 110;
            this.qolSettings.y = 70;
         }
         if(this.qolSettings.parent == null)
         {
            this.§else const native§.addChild(this.qolSettings);
         }
         this.qolRenderSettings();
      }
      
      private function qolHideSettings() : void
      {
         if(this.qolSettings != null && this.qolSettings.parent != null)
         {
            this.qolSettings.parent.removeChild(this.qolSettings);
         }
      }
'''
new = '''      private function qolShowSettings() : void
      {
         if(!this.onPause())
         {
            this.qolSettingsOwnsPause = true;
            this.pause(false,false);
         }
         if(this.qolSettings == null)
         {
            this.qolSettings = new Sprite();
            this.qolSettings.x = 110;
            this.qolSettings.y = 70;
         }
         if(this.qolSettings.parent == null)
         {
            this.§else const native§.addChild(this.qolSettings);
         }
         this.qolRenderSettings();
      }
      
      private function qolHideSettings() : void
      {
         if(this.qolSettings != null && this.qolSettings.parent != null)
         {
            this.qolSettings.parent.removeChild(this.qolSettings);
         }
         if(this.qolSettingsOwnsPause && this.onPause())
         {
            this.qolSettingsOwnsPause = false;
            this.pause(false,false);
         }
         if(this.qolTimeAttackPending)
         {
            this.qolTimeAttackPending = false;
            if(Level.qolTimeAttackEnabled && this.indexWaves == 0 && !this.qolTimeAttackLaunched)
            {
               this.qolStartTimeAttack();
               return;
            }
         }
         if(this.qolSendAllAfterMenu)
         {
            this.qolSendAllAfterMenu = false;
            this.qolSendAllWaves();
         }
      }
'''
level = replace_once(level, old, new, 'pause/defer menu lifecycle')
old_enemy = '''         else if(this.qolSettingsPage == 1)
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
'''
new_enemy = '''         else if(this.qolSettingsPage == 1)
         {
            var enemyPages:int = Math.ceil(this.qolEnemies.length / 8);
            this.qolEnemyPage = Math.max(0,Math.min(enemyPages - 1,this.qolEnemyPage));
            this.qolSettings.addChild(this.qolLabel("CUSTOM ENEMIES — PAGE " + (this.qolEnemyPage + 1) + "/" + enemyPages,28,20,22));
            var firstEnemy:int = this.qolEnemyPage * 8;
            var slot:int = 0;
            while(slot < 8 && firstEnemy + slot < this.qolEnemies.length)
            {
               var enemyIndex:int = firstEnemy + slot;
               var shortName:String = String(this.qolEnemies[enemyIndex]).replace("Enemy","");
               var selectedPrefix:String = enemyIndex == this.qolEnemyIndex ? "▶ " : "";
               var bx:Number = slot % 2 == 0 ? 28 : 302;
               var by:Number = 62 + int(slot / 2) * 46;
               this.qolSettings.addChild(this.qolButton(selectedPrefix + shortName,bx,by,250,"enemy_pick_" + enemyIndex));
               slot++;
            }
            this.qolSettings.addChild(this.qolButton("← Enemy page",28,252,150,"enemy_page_prev"));
            this.qolSettings.addChild(this.qolButton("Enemy page →",402,252,150,"enemy_page_next"));
            this.qolSettings.addChild(this.qolLabel("Count: " + this.qolEnemyCount,28,314,16));
            this.qolSettings.addChild(this.qolButton("-5",160,302,70,"count_minus"));
            this.qolSettings.addChild(this.qolButton("+5",240,302,70,"count_plus"));
            this.qolSettings.addChild(this.qolLabel("Path: " + (this.qolEnemyPath + 1),326,314,16));
            this.qolSettings.addChild(this.qolButton("Prev",402,302,70,"path_prev"));
            this.qolSettings.addChild(this.qolButton("Next",482,302,70,"path_next"));
            this.qolSettings.addChild(this.qolButton("SEND " + String(this.qolEnemies[this.qolEnemyIndex]).replace("Enemy",""),28,360,524,"send_custom"));
            this.qolSettings.addChild(this.qolButton("←  Main settings",165,420,250,"page_main"));
         }
'''
level = replace_once(level, old_enemy, new_enemy, 'enemy catalog grid')
old_hero = '''            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("ashbite","Ashbite"),28,264,250,"hero_ashbite"));
            this.qolSettings.addChild(this.qolLabel("All 9 start ON. Tap any hero to toggle it for this level.",28,326,14));
            this.qolSettings.addChild(this.qolButton("←  Main settings",165,374,250,"page_main"));'''
new_hero = '''            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("ashbite","Ashbite"),28,264,250,"hero_ashbite"));
            var allHeroesOn:Boolean = this.qolAllHeroesEnabled();
            this.qolSettings.addChild(this.qolButton(allHeroesOn ? "TURN ALL 9 HEROES OFF" : "TURN ALL 9 HEROES ON",28,316,524,"heroes_all"));
            this.qolSettings.addChild(this.qolLabel("This SWF contains 9 playable hero classes; all 9 are listed above.",28,368,14));
            this.qolSettings.addChild(this.qolButton("←  Main settings",165,408,250,"page_main"));'''
level = replace_once(level, old_hero, new_hero, 'all heroes button')
level = level.replace('Timer ON activates every authored wave immediately.', 'Timer arms here; all authored waves launch only after this menu closes.')
level = level.replace('Turn recycling on first, then enable the timer to start.', 'Configure options, then close the menu to start the timer and waves.')
anchor = '''         else if(action.indexOf("hero_") == 0)
         {
            this.qolToggleHero(action.substr(5));
         }
'''
level = replace_once(level, anchor, anchor + '''         else if(action == "heroes_all")
         {
            this.qolSetAllHeroes(!this.qolAllHeroesEnabled());
         }
''', 'heroes all action')
old_ta = '''         else if(action == "time_attack")
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
'''
new_ta = '''         else if(action == "time_attack")
         {
            Level.qolTimeAttackEnabled = !Level.qolTimeAttackEnabled;
            this.qolTimeAttackPending = Level.qolTimeAttackEnabled && this.indexWaves == 0 && !this.qolTimeAttackLaunched;
            if(!Level.qolTimeAttackEnabled)
            {
               this.qolTimeAttackPending = false;
               this.qolTimerRunning = false;
            }
            this.qolUpdateTimerHud();
         }
'''
level = replace_once(level, old_ta, new_ta, 'defer time attack')
level = replace_once(level, '            if(action == "all_waves")\n            {\n               this.qolSendAllWaves();\n            }', '            if(action == "all_waves")\n            {\n               this.qolSendAllAfterMenu = true;\n            }', 'defer send all')
old_nav = '''            else if(action == "enemy_prev")
            {
               this.qolEnemyIndex = (this.qolEnemyIndex + this.qolEnemies.length - 1) % this.qolEnemies.length;
            }
            else if(action == "enemy_next")
            {
               this.qolEnemyIndex = (this.qolEnemyIndex + 1) % this.qolEnemies.length;
            }
'''
new_nav = '''            else if(action == "enemy_page_prev")
            {
               this.qolEnemyPage = (this.qolEnemyPage + Math.ceil(this.qolEnemies.length / 8) - 1) % Math.ceil(this.qolEnemies.length / 8);
            }
            else if(action == "enemy_page_next")
            {
               this.qolEnemyPage = (this.qolEnemyPage + 1) % Math.ceil(this.qolEnemies.length / 8);
            }
            else if(action.indexOf("enemy_pick_") == 0)
            {
               this.qolEnemyIndex = int(action.substr(11));
            }
'''
level = replace_once(level, old_nav, new_nav, 'enemy page actions')
hero_anchor = '''      private function qolHeroLabel(param1:String, param2:String) : String
      {
         this.qolEnsureHeroSelection();
         return param2 + ": " + (Boolean(Level.qolHeroEnabled[param1]) ? "ON" : "off");
      }
      
'''
hero_helpers = hero_anchor + '''      private function qolAllHeroesEnabled() : Boolean
      {
         this.qolEnsureHeroSelection();
         for each(var enabled:Boolean in Level.qolHeroEnabled)
         {
            if(!enabled)
            {
               return false;
            }
         }
         return true;
      }
      
      private function qolSetAllHeroes(param1:Boolean) : void
      {
         this.qolEnsureHeroSelection();
         for(var heroName:String in Level.qolHeroEnabled)
         {
            Level.qolHeroEnabled[heroName] = param1;
         }
         this.qolApplyHeroSelection();
      }
      
'''
level = replace_once(level, hero_anchor, hero_helpers, 'hero bulk helpers')
level = replace_once(level, '         if(this.qolSendAllPending)\n         {', '         if(this.qolSendAllPending && !this.onPause())\n         {', 'pause send-all scheduler')
write('Level.as', level)

holder = read('TowerHolder.as')
old_specials = '''            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_legion_archer","tw_archer",0,false,0,0,0,1,"TooltipBasic",{
               "title":"Legion Archer",
               "text":"Place the original-stage Legion Archer special tower."
            }),new Array("qol_mercenary","tw_soldier",0,false,0,0,0,2,"TooltipBasic",{
               "title":"Mercenary Camp",
               "text":"Place the Dunes of Despair camp; recruits keep their normal hire costs."
            }),new Array("qol_amazona","tw_soldier",0,false,0,0,0,3,"TooltipBasic",{
               "title":"Spear Maiden Hut",
               "text":"Place the Crimson Valley hut; recruits keep their normal hire costs."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← Special towers",
               "text":"Return to the first special-tower page."
            })));'''
new_specials = '''            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_legion_archer","tw_archer",0,false,0,0,0,1,"TooltipBasic",{
               "title":"Legion Archer",
               "text":"Place the original-stage Legion Archer special tower."
            }),new Array("qol_mercenary","tw_soldier",0,false,0,0,0,2,"TooltipBasic",{
               "title":"Mercenary Camp",
               "text":"Place the Dunes of Despair camp; recruits keep their normal hire costs."
            }),new Array("qol_amazona","tw_soldier",0,false,0,0,0,3,"TooltipBasic",{
               "title":"Spear Maiden Hut",
               "text":"Place the Crimson Valley hut; recruits keep their normal hire costs."
            }),new Array("qol_assassin","tw_assassin",this.cRoot.gameSettings.§_-jG§.assassin.cost,false,0,0,0,4,"TooltipBasic",{
               "title":"Assassins Guild",
               "text":"Build the Assassin specialization directly."
            }),new Array("qol_templar","tw_templar",this.cRoot.gameSettings.§_-jG§.templar.cost,false,0,0,0,5,"TooltipBasic",{
               "title":"Knights Templar",
               "text":"Build the Templar specialization directly."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← Special towers",
               "text":"Return to the first special-tower page."
            })));'''
holder = replace_once(holder, old_specials, new_specials, 'assassin templar menu')
anchor = '''         if(param1 == "qol_crossbow")
         {
            this.qolPlaceSpecial(new TowerArcherCrossbow(this.x,this.y + this.yAdjust,this.§_-EV§,0,this.canBuildBarracks));
            return;
         }
'''
extra = '''         if(param1 == "qol_assassin" || param1 == "qol_templar")
         {
            var barracks:§_-oH§ = new §_-oH§(this.x,this.y + this.yAdjust,this.§_-EV§,"level_3");
            this.cRoot.entities.addChild(barracks);
            this.cRoot.towers[barracks] = barracks;
            barracks.upgradeTower(param1 == "qol_assassin" ? "level_assassin" : "level_templar");
            this.destroyThis();
            return;
         }
'''
holder = replace_once(holder, anchor, extra + anchor, 'assassin templar actions')
write('TowerHolder.as', holder)

for name, needles in {
    'Level.as':['qolSettingsOwnsPause','qolTimeAttackPending','TURN ALL 9 HEROES','enemy_pick_','this.§else const native§.addChild(this.qolTimerLabel)'],
    'TowerHolder.as':['qol_assassin','qol_templar','barracks.upgradeTower'],
}.items():
    text = read(name)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'{needle} missing in {name}')
print('V9 menu/completeness patch applied')
