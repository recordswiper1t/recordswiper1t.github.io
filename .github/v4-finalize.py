#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

SRC = Path(sys.argv[1])
IMP = Path(sys.argv[2])


def die(msg):
    raise SystemExit(msg)


def get(name):
    p = IMP / 'scripts' / name
    if p.exists():
        return p.read_text(encoding='utf-8')
    p = SRC / name
    if not p.exists():
        die(f'missing source: {name}')
    return p.read_text(encoding='utf-8')


def save(name, text):
    p = IMP / 'scripts' / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        die(f'{label}: expected one anchor, found {count}')
    return text.replace(old, new, 1)


def replace_function(text, signature, replacement):
    start = text.find(signature)
    if start < 0:
        die(f'function not found: {signature}')
    brace = text.find('{', start)
    depth = 0
    end = None
    for i in range(brace, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        die(f'unterminated function: {signature}')
    return text[:start] + replacement.rstrip() + text[end:]


# Hero levels + skills: maxed by default, reset leaves level 10 with spendable skill pool.
t = get('§_-2i§.as')
t = replace_function(t, 'public function qolSetSkillsMaxed(param1:Boolean) : void', r'''public function qolSetSkillsMaxed(param1:Boolean) : void
      {
         var heroes:Array = [this.heroAlric,this.heroMirage,this.heroCronan,this.heroCaptain,this.heroNivus,this.heroDierdre,this.heroGrawl,this.heroShatra,this.heroAshbite];
         var h:Object = null;
         var skill:Object = null;
         for each(h in heroes)
         {
            h.level = 10;
            if(this.master_xp != null && this.master_xp.length > 0)
            {
               h.xp = this.master_xp[this.master_xp.length - 1];
            }
            for each(skill in h.skillArray)
            {
               skill.level = param1 ? 3 : 0;
            }
         }
         this.updateSkillPoints();
      }''')
save('§_-2i§.as', t)

# Progression: max mode by default; custom reset persists and preserves later manual choices.
t = get('§_-BQ§.as')
t = once(t, '         this.qolSetTreesMaxed(true);\n', r'''         if(this.qolGetProgressMode() == "custom")
         {
            this.qolTreesMaxed = false;
            this.stars = this.qolRemainingUpgradeStars();
         }
         else
         {
            this.qolSetTreesMaxed(true);
         }
''', 'progress constructor')
marker = '      public function qolSetTreesMaxed(param1:Boolean) : void\n'
helper = r'''      public function qolGetProgressMode() : String
      {
         var so:SharedObject = null;
         if(this.§_-yX§)
         {
            return "max";
         }
         try
         {
            so = SharedObject.getLocal(this.§use const get§);
            if(so.data.qolProgressMode == "custom")
            {
               so.close();
               return "custom";
            }
            so.close();
         }
         catch(err:Error)
         {
         }
         return "max";
      }
      
      private function qolSaveProgressMode(param1:String) : void
      {
         var so:SharedObject = null;
         if(!this.§_-yX§)
         {
            try
            {
               so = SharedObject.getLocal(this.§use const get§);
               so.data.qolProgressMode = param1;
               so.data.starsWon = this.starsWon;
               so.data.stars = this.stars;
               so.flush();
               so.close();
            }
            catch(err:Error)
            {
            }
         }
         this.gameUpgrades.§case super§();
         this.gameHeroData.§case super§();
      }
      
'''
t = once(t, marker, helper + marker, 'progress persistence')
t = replace_function(t, 'public function qolSetTreesMaxed(param1:Boolean) : void', r'''public function qolSetTreesMaxed(param1:Boolean) : void
      {
         this.qolTreesMaxed = param1;
         this.gameUpgrades.qolSetMaxed(param1);
         this.gameHeroData.qolSetSkillsMaxed(param1);
         this.starsWon = 65;
         this.stars = param1 ? 0 : this.qolRemainingUpgradeStars();
         this.qolSaveProgressMode(param1 ? "max" : "custom");
      }''')
save('§_-BQ§.as', t)

# Level: all heroes enabled by default, clearer controls, and lower allocation/cosmetic load under swarms.
t = get('Level.as')
t = once(t, '      private var qolSendAllCooldown:int = 0;\n', '      private var qolSendAllCooldown:int = 0;\n      \n      private var qolPerfFrame:int = 0;\n      \n      private var qolEntityScratch:Array = [];\n      \n      private var qolEnemyDecalScratch:Array = [];\n      \n      private var qolBulletScratch:Array = [];\n', 'performance fields')
t = once(t, '            Level.qolHeroEnabled[heroName] = false;\n', '            Level.qolHeroEnabled[heroName] = true;\n', 'hero defaults')
t = t.replace('         Level.qolHeroEnabled[this.game.gameHeroData.selectedHero.name] = true;\n', '', 1)
t = t.replace('this.game.qolTreesMaxed ? "Trees: MAXED (reset)" : "Trees: RESET (max)"', 'this.game.qolTreesMaxed ? "RESET FOR CUSTOM" : "MAX ALL"', 1)
t = t.replace('This Flash build contains 9 regular hero implementations.', 'All 9 start ON. Tap any hero to toggle it for this level.', 1)
snapshot = r'''      private function qolUpdateContainer(param1:DisplayObjectContainer, param2:Array) : void
      {
         var i:int = 0;
         var item:DisplayObject = null;
         param2.length = 0;
         while(i < param1.numChildren)
         {
            param2.push(param1.getChildAt(i));
            i++;
         }
         i = 0;
         while(i < param2.length)
         {
            item = param2[i] as DisplayObject;
            if(item != null && item.parent == param1)
            {
               MovieClip(item).onFrameUpdate();
               ++this.§override get§;
            }
            i++;
         }
      }
      
'''
t = once(t, '      public function updateEntities() : void\n', snapshot + '      public function updateEntities() : void\n', 'snapshot helper')
t = replace_function(t, 'public function updateEntities() : void', r'''public function updateEntities() : void
      {
         this.qolUpdateContainer(this.entities,this.qolEntityScratch);
      }''')
t = replace_function(t, 'public function updateEnemyDecals() : void', r'''public function updateEnemyDecals() : void
      {
         this.qolUpdateContainer(this.enemyDecals,this.qolEnemyDecalScratch);
      }''')
t = replace_function(t, 'public function updateBullets() : void', r'''public function updateBullets() : void
      {
         this.qolUpdateContainer(this.bullets,this.qolBulletScratch);
      }''')
t = replace_function(t, 'private function qolGameTick() : void', r'''private function qolGameTick() : void
      {
         this.qolPerfFrame++;
         if(this.§_-BF§ == LEVEL_NORMAL)
         {
            this.§_-HR§();
         }
         if(this.§_-BF§ == LEVEL_NORMAL || this.§_-BF§ == LEVEL_PRE_WIN)
         {
            var heavy:Boolean = this.entities.numChildren > 280 || this.bullets.numChildren > 320;
            this.updateEntities();
            this.updateBullets();
            if(!heavy || (this.qolPerfFrame & 1) == 0)
            {
               this.updateEnemyDecals();
               this.updateBulletsDecals();
               this.updateDecals();
               this.updateBackground();
            }
            this.§_-ai§();
            this.menu.updateMenu();
            this.§include return§.update();
            this.updatePointers();
         }
      }''')
save('Level.as', t)

# Special tower catalog: preserve the existing eight and add the missing true map-special Dwarf Hall.
t = get('TowerHolder.as')
old1 = '''new Array("qol_crossbow","tw_archer",this.cRoot.gameSettings.archers.crossbow.cost,false,0,0,0,3,"TooltipBasic",{\n               "title":"Crossbow Fort",\n               "text":"Build the Crossbow specialization directly."\n            }),new Array("qol_totem","tw_archer",this.cRoot.gameSettings.archers.totem.cost,false,0,0,0,4,"TooltipBasic",{\n               "title":"Tribal Axethrowers",\n               "text":"Build the Totem specialization directly."\n            }),new Array("qol_specials2"'''
new1 = '''new Array("qol_hall","tw_soldier",225,false,0,0,0,3,"TooltipBasic",{\n               "title":"Dwarf Hall — 225",\n               "text":"Place the map-special Dwarf Hall barracks."\n            }),new Array("qol_specials2"'''
t = once(t, old1, new1, 'Dwarf Hall menu')
old2 = '''new Array("qol_archmage","tw_mage",this.cRoot.gameSettings.mages.archmage.cost,false,0,0,0,1,"TooltipBasic",{\n               "title":"Archmage",\n               "text":"Build the Archmage specialization directly."\n            }),new Array("qol_necro","tw_mage",this.cRoot.gameSettings.mages.necromancer.cost,false,0,0,0,2,"TooltipBasic",{\n               "title":"Necromancer",\n               "text":"Build the Necromancer specialization directly."\n            }),new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,3,"TooltipBasic",{\n               "title":"DWAARP",\n               "text":"Build the DWAARP specialization directly."\n            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,4,"TooltipBasic",{\n               "title":"Battle-Mecha T200",\n               "text":"Build the Battle-Mecha specialization directly."\n            }),new Array("qol_specials"'''
new2 = '''new Array("qol_crossbow","tw_archer",this.cRoot.gameSettings.archers.crossbow.cost,false,0,0,0,1,"TooltipBasic",{\n               "title":"Crossbow Fort",\n               "text":"Build the Crossbow specialization directly."\n            }),new Array("qol_totem","tw_archer",this.cRoot.gameSettings.archers.totem.cost,false,0,0,0,2,"TooltipBasic",{\n               "title":"Tribal Axethrowers",\n               "text":"Build the Totem specialization directly."\n            }),new Array("qol_archmage","tw_mage",this.cRoot.gameSettings.mages.archmage.cost,false,0,0,0,3,"TooltipBasic",{\n               "title":"Archmage",\n               "text":"Build the Archmage specialization directly."\n            }),new Array("qol_necro","tw_mage",this.cRoot.gameSettings.mages.necromancer.cost,false,0,0,0,4,"TooltipBasic",{\n               "title":"Necromancer",\n               "text":"Build the Necromancer specialization directly."\n            }),new Array("qol_specials3"'''
t = once(t, old2, new2, 'special page 2')
page3 = r'''         if(param1 == "qol_specials3")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"DWAARP","text":"Build the DWAARP specialization directly."
            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Battle-Mecha T200","text":"Build the Battle-Mecha specialization directly."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← Special towers","text":"Return to the first special-tower page."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
'''
t = once(t, '         if(param1 == "qol_dwarf")\n', page3 + '         if(param1 == "qol_dwarf")\n', 'special page 3')
hall = r'''         if(param1 == "qol_hall")
         {
            if(this.cRoot.cash < 225)
            {
               return;
            }
            this.cRoot.updateCash(-225);
            this.qolPlaceSpecial(new §_-Zs§(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
'''
t = once(t, '         if(param1 == "qol_pirates")\n', hall + '         if(param1 == "qol_pirates")\n', 'Dwarf Hall action')
save('TowerHolder.as', t)

# Quick menu recognizes page 3 and exits safely after V4 tower replacement actions.
t = get('§_-LZ§.as')
t = once(t, 'if(param1 == "qol_specials" || param1 == "qol_specials2")', 'if(param1 == "qol_specials" || param1 == "qol_specials2" || param1 == "qol_specials3")', 'special page navigation')
marker = '         this.cTower.upgradeTower(param1);\n'
safe = r'''         if(param1.indexOf("qol_") == 0)
         {
            this.cTower.upgradeTower(param1);
            this.hide();
            return;
         }
'''
t = once(t, marker, safe + marker, 'safe special action')
save('§_-LZ§.as', t)

# Touch reliability for the radial item and all true map-special towers.
for name in ['§true break§.as', 'TowerDwarfRiflemen.as', 'TowerSoldierPirates.as', '§_-Zs§.as']:
    t = get(name).replace('MouseEvent.CLICK,this.clickEvent', 'MouseEvent.MOUSE_DOWN,this.clickEvent')
    save(name, t)

assets = SRC.parent / '_assets'
if assets.exists():
    shutil.copytree(assets, IMP.parent / '_assets', dirs_exist_ok=True)
print('V4 final patch staged')
