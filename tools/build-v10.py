#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: build-v10.py <exported-v9-scripts-dir>')
scripts = Path(sys.argv[1])

def read(name):
    p = scripts / name
    if not p.exists():
        raise SystemExit(f'missing exported script: {p}')
    return p.read_text(encoding='utf-8-sig')

def write(name, text):
    (scripts / name).write_text(text, encoding='utf-8', newline='\n')

def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    return text.replace(old, new, 1)

# ---------------------------------------------------------------------------
# Level.as: add the real stage-exclusive Rurin hero, cleanly detach Cronan,
# and make Send All enter the same first-wave/power state as normal play.
# ---------------------------------------------------------------------------
level = read('Level.as')
level = replace_once(
    level,
    '''this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("ashbite","Ashbite"),28,264,250,"hero_ashbite"));
            var allHeroesOn:Boolean = this.qolAllHeroesEnabled();
            this.qolSettings.addChild(this.qolButton(allHeroesOn ? "TURN ALL 9 HEROES OFF" : "TURN ALL 9 HEROES ON",28,316,524,"heroes_all"));
            this.qolSettings.addChild(this.qolLabel("This SWF contains 9 playable hero classes; all 9 are listed above.",28,368,14));''',
    '''this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("ashbite","Ashbite"),28,264,250,"hero_ashbite"));
            this.qolSettings.addChild(this.qolButton(this.qolHeroLabel("rurin","Rurin Longbeard"),302,264,250,"hero_rurin"));
            var allHeroesOn:Boolean = this.qolAllHeroesEnabled();
            this.qolSettings.addChild(this.qolButton(allHeroesOn ? "TURN ALL 10 HEROES OFF" : "TURN ALL 10 HEROES ON",28,316,524,"heroes_all"));
            this.qolSettings.addChild(this.qolLabel("Includes Rurin Longbeard, the Dark Descent stage hero.",28,368,14));''',
    'Rurin hero UI',
)
level = replace_once(
    level,
    '''            case "ashbite":
               return new SoldierHeroDragon(p,p,null,p);
            default:''',
    '''            case "ashbite":
               return new SoldierHeroDragon(p,p,null,p);
            case "rurin":
               return new §switch for super§(p,p,null,p);
            default:''',
    'Rurin hero constructor',
)
old_roster = '["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite"]'
if level.count(old_roster) != 2:
    raise SystemExit(f'hero roster: expected 2 matches, found {level.count(old_roster)}')
level = level.replace(old_roster, '["alric","mirage","captain","cronan","shatra","grawl","nivus","dierdre","ashbite","rurin"]')

apply_anchor = '''      private function qolApplyHeroSelection() : void
      {
'''
detach_helper = '''      private function qolDetachHero(param1:§dynamic const class§) : void
      {
         if(param1 == null)
         {
            return;
         }
         if(param1 is SoldierHeroCronan)
         {
            SoldierHeroCronan(param1).qolCleanupCompanions();
         }
         if(param1.parent != null)
         {
            param1.parent.removeChild(param1);
         }
      }
      
''' + apply_anchor
level = replace_once(level, apply_anchor, detach_helper, 'hero detach helper')
level = replace_once(
    level,
    '''            if(oldHero != null && oldHero.parent != null)
            {
               oldHero.parent.removeChild(oldHero);
            }''',
    '''            this.qolDetachHero(oldHero);''',
    'detach extra heroes',
)
level = replace_once(
    level,
    '''         else if(this.hero != null && this.hero.parent != null)
         {
            this.hero.parent.removeChild(this.hero);
         }''',
    '''         else if(this.hero != null && this.hero.parent != null)
         {
            this.qolDetachHero(this.hero);
         }''',
    'detach primary hero',
)

send_anchor = '''      private function qolSendAllWaves() : void
      {
'''
power_helper = '''      private function qolEnsureSendAllLevelStarted() : void
      {
         if(this.indexWaves != 0)
         {
            return;
         }
         if(this.power1)
         {
            this.§finally const function§();
         }
         if(this.power2)
         {
            this.§do for import§();
         }
         if(this.power3)
         {
            this.unlockPowerPriest();
         }
         if(this.power4)
         {
            this.§do var§();
         }
         this.§_-yQ§();
         this.§dynamic include§ = false;
         if(this.§null use§ != null && this.bullets.contains(this.§null use§))
         {
            this.bullets.removeChild(this.§null use§);
         }
         this.game.gameSounds.§catch const set§();
      }
      
''' + send_anchor
level = replace_once(level, send_anchor, power_helper, 'Send All start helper')
level = replace_once(
    level,
    '''      private function qolSendAllWaves() : void
      {
         this.qolSendAllPending''',
    '''      private function qolSendAllWaves() : void
      {
         this.qolEnsureSendAllLevelStarted();
         this.qolSendAllPending''',
    'Send All power activation',
)
write('Level.as', level)

# Dark Descent normally spawns Rurin through Level14 itself. V10 manages him
# through the unified hero roster so the toggle works and there is no duplicate.
level14 = read('Level14.as')
level14 = replace_once(
    level14,
    '''      override public function §_-9B§() : void
      {
         this.entities.addChild(new §switch for super§(new Point(this.§_-R4§[1].x,this.§_-R4§[1].y),new Point(this.§_-R4§[1].x,this.§_-R4§[1].y),null,new Point(this.§_-R4§[1].x,this.§_-R4§[1].y)));
      }''',
    '''      override public function §_-9B§() : void
      {
         // Rurin is managed by the V10 hero roster to avoid duplicate stage spawns.
      }''',
    'Level14 Rurin ownership',
)
write('Level14.as', level14)

# Cronan companions used to outlive the hero because the menu only detached the
# hero display object. Explicitly destroy both companion types and break their
# back-reference before the hero is removed.
cronan = read('SoldierHeroCronan.as')
cronan_anchor = '''      override public function §_-my§() : void
      {
'''
cronan_helper = '''      public function qolCleanupCompanions() : void
      {
         var falcon:SoldierFalcon = null;
         var boar:§_-Fu§ = null;
         for each(falcon in this.falcons)
         {
            falcon.hero = null;
            falcon.§null const final§();
            falcon.destroyThis();
         }
         this.falcons = [];
         for each(boar in this.boars)
         {
            boar.hero = null;
            boar.§null const final§();
            boar.destroyThis();
         }
         this.boars = [];
      }
      
''' + cronan_anchor
cronan = replace_once(cronan, cronan_anchor, cronan_helper, 'Cronan companion cleanup')
cronan = replace_once(
    cronan,
    '''         var _loc1_:SoldierFalcon = null;
         super.§_-my§();
         this.isCastingDeepLashes = false;
         this.§_-sI§ = false;
         this.§_-jT§ = false;
         this.isCastingStampede = false;
         for each(_loc1_ in this.falcons)
         {
            _loc1_.§null const final§();
         }
         this.falcons = [];''',
    '''         super.§_-my§();
         this.isCastingDeepLashes = false;
         this.§_-sI§ = false;
         this.§_-jT§ = false;
         this.isCastingStampede = false;
         this.qolCleanupCompanions();''',
    'Cronan native cleanup reuse',
)
write('SoldierHeroCronan.as', cronan)

# ---------------------------------------------------------------------------
# Map-special selling. The QuickMenu's tower=true flag exposes the engine's
# normal sell control; each class gets a sell action that replaces it with a
# normal build holder. Paid special towers also seed their original build cost
# so preplaced and player-placed copies return a normal sell-percent refund.
# ---------------------------------------------------------------------------
for name, cost in [
    ('TowerDwarfRiflemen.as', 250),
    ('TowerSoldierPirates.as', 180),
    ('§_-Zs§.as', 225),
]:
    text = read(name)
    text = replace_once(
        text,
        '         this.cRoot = Level(this.parent.parent);',
        '         this.cRoot = Level(this.parent.parent);\n         if(this.§_-6f§ <= 0)\n         {\n            this.§_-6f§ = %d;\n         }' % cost,
        name + ' initial sell investment',
    )
    write(name, text)

def add_standard_sell(name, soldier=False):
    text = read(name)
    old_menu = 'this,false,180,'
    if old_menu not in text:
        raise SystemExit(f'{name}: sell-menu anchor missing')
    text = text.replace(old_menu, 'this,true,180,', 1)
    signature = '      override public function upgradeTower(param1:String) : void\n      {'
    pos = text.find(signature)
    if pos < 0:
        raise SystemExit(f'{name}: upgradeTower signature missing')
    switch = '         switch(param1)\n         {'
    sw = text.find(switch, pos)
    if sw < 0:
        raise SystemExit(f'{name}: upgradeTower switch missing')
    cleanup = '               this.§_-Zj§();\n' if soldier else ''
    sell = '''         switch(param1)
         {
            case "sell":
               var refund:int = this.getSellValue();
               this.cRoot.updateCash(refund);
''' + cleanup + '''               this.cRoot.entities.addChild(new TowerHolder(this.x,this.y,this.§_-EV§));
               this.cRoot.entities.addChild(new §_-6G§(new Point(this.x,this.y),refund));
               this.cRoot.§get import§();
               this.destroyThis(true);
               return;
'''
    text = text[:sw] + sell + text[sw + len(switch):]
    write(name, text)

add_standard_sell('TowerDwarfRiflemen.as', False)
add_standard_sell('TowerSoldierPirates.as', True)
add_standard_sell('§_-Zs§.as', True)
add_standard_sell('§return const if§.as', True)
add_standard_sell('§override import§.as', True)

# Pirate Camp has its own no-argument destroyThis implementation.
pirate = read('§_-MR§.as')
if 'this,false,180,' not in pirate:
    raise SystemExit('Pirate Camp sell-menu anchor missing')
pirate = pirate.replace('this,false,180,', 'this,true,180,', 1)
sig = '      override public function upgradeTower(param1:String) : void\n      {'
pos = pirate.find(sig)
switch = '         switch(param1)\n         {'
sw = pirate.find(switch, pos)
if pos < 0 or sw < 0:
    raise SystemExit('Pirate Camp upgrade switch missing')
pirate_sell = '''         switch(param1)
         {
            case "sell":
               var refund:int = this.getSellValue();
               this.cRoot.updateCash(refund);
               this.cRoot.entities.addChild(new TowerHolder(this.x,this.y,this.§_-EV§));
               this.cRoot.entities.addChild(new §_-6G§(new Point(this.x,this.y),refund));
               this.cRoot.§get import§();
               this.destroyThis();
               return;
'''
pirate = pirate[:sw] + pirate_sell + pirate[sw + len(switch):]
write('§_-MR§.as', pirate)

# Legion Archer had no radial menu at all. Give it a sell-only radial using the
# same QuickMenu tower flag and intercept the sell action before its init path.
legion = read('§_-Xb§.as')
legion = replace_once(
    legion,
    '''         this.showRange(this.§dynamic const§,this.§null for set§);
         this.cRoot.quickMenu.cTower = this;
         this.cRoot.game.gameSounds.§if for§();''',
    '''         this.showRange(this.§dynamic const§,this.§null for set§);
         MovieClip(this.cRoot).quickMenu.load(this.x,this.y - 10,this,true,180,false,new Array());
         this.cRoot.quickMenu.show(this.cRoot.§else const native§);
         this.cRoot.quickMenu.cTower = this;
         this.cRoot.game.gameSounds.§if for§();''',
    'Legion Archer sell menu',
)
legion = replace_once(
    legion,
    '''      override public function upgradeTower(param1:String) : void
      {
         this.§_-3g§(new §for for use§());''',
    '''      override public function upgradeTower(param1:String) : void
      {
         if(param1 == "sell")
         {
            var refund:int = this.getSellValue();
            this.cRoot.updateCash(refund);
            this.cRoot.entities.addChild(new TowerHolder(this.x,this.y,this.§_-EV§));
            this.cRoot.entities.addChild(new §_-6G§(new Point(this.x,this.y),refund));
            this.cRoot.§get import§();
            this.destroyThis(true);
            return;
         }
         this.§_-3g§(new §for for use§());''',
    'Legion Archer sell action',
)
write('§_-Xb§.as', legion)

checks = {
    'Level.as': ['Rurin Longbeard', 'qolDetachHero', 'qolEnsureSendAllLevelStarted', 'new §switch for super§'],
    'Level14.as': ['Rurin is managed by the V10 hero roster'],
    'SoldierHeroCronan.as': ['qolCleanupCompanions', 'boar.destroyThis()', 'falcon.destroyThis()'],
    'TowerDwarfRiflemen.as': ['case "sell"', 'this.§_-6f§ = 250'],
    'TowerSoldierPirates.as': ['case "sell"', 'this.§_-6f§ = 180'],
    '§_-Zs§.as': ['case "sell"', 'this.§_-6f§ = 225'],
    '§_-MR§.as': ['case "sell"'],
    '§_-Xb§.as': ['case "sell"'],
    '§return const if§.as': ['case "sell"'],
    '§override import§.as': ['case "sell"'],
}
for name, needles in checks.items():
    text = read(name)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f'validation failed: {needle!r} missing from {name}')

print('V10 follow-up patches applied successfully')
