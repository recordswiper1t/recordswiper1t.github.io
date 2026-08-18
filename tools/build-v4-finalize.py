#!/usr/bin/env python3
from pathlib import Path
import sys


def die(msg):
    raise SystemExit(msg)


def readp(p):
    if not p.exists(): die(f"missing {p}")
    return p.read_text(encoding="utf-8")


def once(t,a,b,label):
    n=t.count(a)
    if n!=1: die(f"{label}: expected 1 anchor, got {n}")
    return t.replace(a,b,1)


def func(t,sig,repl):
    a=t.find(sig)
    if a<0: die(f"missing function {sig}")
    b=t.find('{',a); depth=0; end=None
    for i in range(b,len(t)):
        if t[i]=='{': depth+=1
        elif t[i]=='}':
            depth-=1
            if depth==0: end=i+1; break
    if end is None: die(f"unterminated {sig}")
    return t[:a]+repl.rstrip()+t[end:]


def source(src,imp,name):
    p=imp/'scripts'/name
    return readp(p if p.exists() else src/name)


def save(imp,name,t):
    p=imp/'scripts'/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(t,encoding='utf-8')


def patch_hero(t):
    return func(t,'public function qolSetSkillsMaxed(param1:Boolean) : void',r'''public function qolSetSkillsMaxed(param1:Boolean) : void
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


def patch_game(t):
    t=once(t,'         this.qolSetTreesMaxed(true);\n',r'''         if(this.qolGetProgressMode() == "custom")
         {
            this.qolTreesMaxed = false;
            this.stars = this.qolRemainingUpgradeStars();
         }
         else
         {
            this.qolSetTreesMaxed(true);
         }
''','persistent custom load')
    marker='      public function qolSetTreesMaxed(param1:Boolean) : void\n'
    helper=r'''      public function qolGetProgressMode() : String
      {
         var so:SharedObject = null;
         if(this.§_-yX§) return "max";
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
         catch(err:Error) {}
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
            catch(err:Error) {}
         }
         this.gameUpgrades.§case super§();
         this.gameHeroData.§case super§();
      }
      
'''
    t=once(t,marker,helper+marker,'progress helpers')
    return func(t,'public function qolSetTreesMaxed(param1:Boolean) : void',r'''public function qolSetTreesMaxed(param1:Boolean) : void
      {
         this.qolTreesMaxed = param1;
         this.gameUpgrades.qolSetMaxed(param1);
         this.gameHeroData.qolSetSkillsMaxed(param1);
         this.starsWon = 65;
         this.stars = param1 ? 0 : this.qolRemainingUpgradeStars();
         this.qolSaveProgressMode(param1 ? "max" : "custom");
      }''')


def patch_level(t):
    t=once(t,'      private var qolSendAllCooldown:int = 0;\n','      private var qolSendAllCooldown:int = 0;\n      \n      private var qolPerfFrame:int = 0;\n      \n      private var qolEntityScratch:Array = [];\n      \n      private var qolEnemyDecalScratch:Array = [];\n      \n      private var qolBulletScratch:Array = [];\n','perf fields')
    t=once(t,'            Level.qolHeroEnabled[heroName] = false;\n','            Level.qolHeroEnabled[heroName] = true;\n','heroes default on')
    t=t.replace('         Level.qolHeroEnabled[this.game.gameHeroData.selectedHero.name] = true;\n','',1)
    t=t.replace('this.game.qolTreesMaxed ? "Trees: MAXED (reset)" : "Trees: RESET (max)"','this.game.qolTreesMaxed ? "RESET FOR CUSTOM" : "MAX ALL"',1)
    t=t.replace('This Flash build contains 9 regular hero implementations.','All 9 start ON. Tap any hero to toggle it for this level.',1)
    helper=r'''      private function qolUpdateContainer(param1:DisplayObjectContainer, param2:Array) : void
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
    t=once(t,'      public function updateEntities() : void\n',helper+'      public function updateEntities() : void\n','perf helper')
    t=func(t,'public function updateEntities() : void',r'''public function updateEntities() : void
      {
         this.qolUpdateContainer(this.entities,this.qolEntityScratch);
      }''')
    t=func(t,'public function updateEnemyDecals() : void',r'''public function updateEnemyDecals() : void
      {
         this.qolUpdateContainer(this.enemyDecals,this.qolEnemyDecalScratch);
      }''')
    t=func(t,'public function updateBullets() : void',r'''public function updateBullets() : void
      {
         this.qolUpdateContainer(this.bullets,this.qolBulletScratch);
      }''')
    return func(t,'private function qolGameTick() : void',r'''private function qolGameTick() : void
      {
         this.qolPerfFrame++;
         if(this.§_-BF§ == LEVEL_NORMAL) this.§_-HR§();
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


def patch_tower(t):
    # Reorganize the already-working V4 catalog to include the missing Dwarf Hall.
    old1='''new Array("qol_crossbow","tw_archer",this.cRoot.gameSettings.archers.crossbow.cost,false,0,0,0,3,"TooltipBasic",{\n               "title":"Crossbow Fort",\n               "text":"Build the Crossbow specialization directly."\n            }),new Array("qol_totem","tw_archer",this.cRoot.gameSettings.archers.totem.cost,false,0,0,0,4,"TooltipBasic",{\n               "title":"Tribal Axethrowers",\n               "text":"Build the Totem specialization directly."\n            }),new Array("qol_specials2"'''
    new1='''new Array("qol_hall","tw_soldier",225,false,0,0,0,3,"TooltipBasic",{\n               "title":"Dwarf Hall — 225",\n               "text":"Place the map-special Dwarf Hall barracks."\n            }),new Array("qol_specials2"'''
    t=once(t,old1,new1,'Dwarf Hall page')
    old2='''new Array("qol_archmage","tw_mage",this.cRoot.gameSettings.mages.archmage.cost,false,0,0,0,1,"TooltipBasic",{\n               "title":"Archmage",\n               "text":"Build the Archmage specialization directly."\n            }),new Array("qol_necro","tw_mage",this.cRoot.gameSettings.mages.necromancer.cost,false,0,0,0,2,"TooltipBasic",{\n               "title":"Necromancer",\n               "text":"Build the Necromancer specialization directly."\n            }),new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,3,"TooltipBasic",{\n               "title":"DWAARP",\n               "text":"Build the DWAARP specialization directly."\n            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,4,"TooltipBasic",{\n               "title":"Battle-Mecha T200",\n               "text":"Build the Battle-Mecha specialization directly."\n            }),new Array("qol_specials"'''
    new2='''new Array("qol_crossbow","tw_archer",this.cRoot.gameSettings.archers.crossbow.cost,false,0,0,0,1,"TooltipBasic",{\n               "title":"Crossbow Fort",\n               "text":"Build the Crossbow specialization directly."\n            }),new Array("qol_totem","tw_archer",this.cRoot.gameSettings.archers.totem.cost,false,0,0,0,2,"TooltipBasic",{\n               "title":"Tribal Axethrowers",\n               "text":"Build the Totem specialization directly."\n            }),new Array("qol_archmage","tw_mage",this.cRoot.gameSettings.mages.archmage.cost,false,0,0,0,3,"TooltipBasic",{\n               "title":"Archmage",\n               "text":"Build the Archmage specialization directly."\n            }),new Array("qol_necro","tw_mage",this.cRoot.gameSettings.mages.necromancer.cost,false,0,0,0,4,"TooltipBasic",{\n               "title":"Necromancer",\n               "text":"Build the Necromancer specialization directly."\n            }),new Array("qol_specials3"'''
    t=once(t,old2,new2,'catalog page 2')
    anchor='''         if(param1 == "qol_dwarf")\n'''
    page3=r'''         if(param1 == "qol_specials3")
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
    t=once(t,anchor,page3+anchor,'catalog page 3')
    hall=r'''         if(param1 == "qol_hall")
         {
            if(this.cRoot.cash < 225) return;
            this.cRoot.updateCash(-225);
            this.qolPlaceSpecial(new §_-Zs§(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
'''
    t=once(t,'         if(param1 == "qol_pirates")\n',hall+'         if(param1 == "qol_pirates")\n','Dwarf Hall action')
    return t


def patch_menu(t):
    t=once(t,'if(param1 == "qol_specials" || param1 == "qol_specials2")','if(param1 == "qol_specials" || param1 == "qol_specials2" || param1 == "qol_specials3")','page3 nav')
    marker='         this.cTower.upgradeTower(param1);\n'
    special=r'''         if(param1.indexOf("qol_") == 0)
         {
            this.cTower.upgradeTower(param1);
            this.hide();
            return;
         }
'''
    return once(t,marker,special+marker,'safe special action')


def patch(src,imp):
    items=[('§_-2i§.as',patch_hero),('§_-BQ§.as',patch_game),('Level.as',patch_level),('TowerHolder.as',patch_tower),('§_-LZ§.as',patch_menu)]
    for n,f in items: save(imp,n,f(source(src,imp,n)))
    for n in ['§true break§.as','TowerDwarfRiflemen.as','TowerSoldierPirates.as','§_-Zs§.as']:
        t=source(src,imp,n).replace('MouseEvent.CLICK,this.clickEvent','MouseEvent.MOUSE_DOWN,this.clickEvent')
        save(imp,n,t)
    print('final V4 patch applied')


def verify(root):
    checks={
      'Level.as':['Level.qolHeroEnabled[heroName] = true','RESET FOR CUSTOM','qolUpdateContainer','var heavy:Boolean'],
      '§_-2i§.as':['h.level = 10','h.xp = this.master_xp[this.master_xp.length - 1]'],
      '§_-BQ§.as':['qolProgressMode','qolSaveProgressMode'],
      'TowerHolder.as':['Dwarf Hall — 225','qol_specials3'],
      '§_-LZ§.as':['qol_specials3','param1.indexOf("qol_") == 0'],
      '§true break§.as':['MouseEvent.MOUSE_DOWN,this.clickEvent'],
      'TowerDwarfRiflemen.as':['MouseEvent.MOUSE_DOWN,this.clickEvent'],
      'TowerSoldierPirates.as':['MouseEvent.MOUSE_DOWN,this.clickEvent'],
      '§_-Zs§.as':['MouseEvent.MOUSE_DOWN,this.clickEvent']}
    for n,needles in checks.items():
        t=readp(root/n)
        for x in needles:
            if x not in t: die(f'verify {n} missing {x}')
    print('final V4 verification markers present')


def main():
    if len(sys.argv)<3: die('usage: patch src import | verify root')
    if sys.argv[1]=='patch': patch(Path(sys.argv[2]),Path(sys.argv[3]))
    elif sys.argv[1]=='verify': verify(Path(sys.argv[2]))
    else: die('bad mode')

if __name__=='__main__': main()
