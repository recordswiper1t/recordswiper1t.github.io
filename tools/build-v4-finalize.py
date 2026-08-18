#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys


def die(msg):
    raise SystemExit(msg)


def read_file(path):
    if not path.exists():
        die(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def write_import(import_root, name, text):
    p = import_root / "scripts" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def get_text(source_root, import_root, name):
    patched = import_root / "scripts" / name
    if patched.exists():
        return read_file(patched)
    return read_file(source_root / name)


def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        die(f"{label}: expected one anchor, found {n}")
    return text.replace(old, new, 1)


def replace_function(text, signature, replacement):
    start = text.find(signature)
    if start < 0:
        die(f"function not found: {signature}")
    brace = text.find("{", start)
    if brace < 0:
        die(f"opening brace missing: {signature}")
    depth = 0
    end = None
    for i in range(brace, len(text)):
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        die(f"closing brace missing: {signature}")
    return text[:start] + replacement.rstrip() + text[end:]


def patch_hero_data(text):
    replacement = r'''public function qolSetSkillsMaxed(param1:Boolean) : void
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
      }'''
    return replace_function(text, "public function qolSetSkillsMaxed(param1:Boolean) : void", replacement)


def patch_game(text):
    text = once(
        text,
        "         this.qolSetTreesMaxed(true);\n",
        r'''         if(this.qolGetProgressMode() == "custom")
         {
            this.qolTreesMaxed = false;
            this.stars = this.qolRemainingUpgradeStars();
         }
         else
         {
            this.qolSetTreesMaxed(true);
         }
''',
        "persistent custom-mode constructor",
    )
    helper = r'''      public function qolGetProgressMode() : String
      {
         var so:SharedObject = null;
         var mode:String = "max";
         if(this.§_-yX§)
         {
            return mode;
         }
         try
         {
            so = SharedObject.getLocal(this.§use const get§);
            if(so.data.qolProgressMode == "custom")
            {
               mode = "custom";
            }
            so.close();
         }
         catch(err:Error)
         {
         }
         return mode;
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
    marker = "      public function qolSetTreesMaxed(param1:Boolean) : void\n"
    text = once(text, marker, helper + marker, "progress persistence helpers")
    replacement = r'''public function qolSetTreesMaxed(param1:Boolean) : void
      {
         this.qolTreesMaxed = param1;
         this.gameUpgrades.qolSetMaxed(param1);
         this.gameHeroData.qolSetSkillsMaxed(param1);
         this.starsWon = 65;
         this.stars = param1 ? 0 : this.qolRemainingUpgradeStars();
         this.qolSaveProgressMode(param1 ? "max" : "custom");
      }'''
    return replace_function(text, "public function qolSetTreesMaxed(param1:Boolean) : void", replacement)


def patch_level(text):
    text = once(
        text,
        "      private var qolSendAllCooldown:int = 0;\n",
        "      private var qolSendAllCooldown:int = 0;\n      \n      private var qolPerfFrame:int = 0;\n      \n      private var qolEntityScratch:Array = [];\n      \n      private var qolEnemyDecalScratch:Array = [];\n      \n      private var qolBulletScratch:Array = [];\n",
        "performance scratch fields",
    )
    text = once(
        text,
        "            Level.qolHeroEnabled[heroName] = false;\n",
        "            Level.qolHeroEnabled[heroName] = true;\n",
        "all heroes enabled by default",
    )
    old_selected = "         Level.qolHeroEnabled[this.game.gameHeroData.selectedHero.name] = true;\n"
    if old_selected in text:
        text = text.replace(old_selected, "", 1)
    text = text.replace(
        'this.game.qolTreesMaxed ? "Trees: MAXED (reset)" : "Trees: RESET (max)"',
        'this.game.qolTreesMaxed ? "RESET FOR CUSTOM" : "MAX ALL"',
        1,
    )
    text = text.replace(
        'this.qolSettings.addChild(this.qolLabel("This Flash build contains 9 regular hero implementations.",28,326,14));',
        'this.qolSettings.addChild(this.qolLabel("All 9 start ON. Tap any hero to toggle that hero for this level.",28,326,14));',
        1,
    )

    helper = r'''      private function qolUpdateContainer(param1:DisplayObjectContainer, param2:Array) : void
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
    marker = "      public function updateEntities() : void\n"
    text = once(text, marker, helper + marker, "snapshot update helper")
    text = replace_function(
        text,
        "public function updateEntities() : void",
        r'''public function updateEntities() : void
      {
         this.qolUpdateContainer(this.entities,this.qolEntityScratch);
      }''',
    )
    text = replace_function(
        text,
        "public function updateEnemyDecals() : void",
        r'''public function updateEnemyDecals() : void
      {
         this.qolUpdateContainer(this.enemyDecals,this.qolEnemyDecalScratch);
      }''',
    )
    text = replace_function(
        text,
        "public function updateBullets() : void",
        r'''public function updateBullets() : void
      {
         this.qolUpdateContainer(this.bullets,this.qolBulletScratch);
      }''',
    )
    text = replace_function(
        text,
        "private function qolGameTick() : void",
        r'''private function qolGameTick() : void
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
      }''',
    )
    return text


TOWER_BRANCH = r'''         if(param1 == "qol_specials")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwarf","tw_archer",250,false,0,0,0,1,"TooltipBasic",{
               "title":"Dwarf Bastion — 250",
               "text":"Place the map-special Dwarf Riflemen tower."
            }),new Array("qol_hall","tw_soldier",225,false,0,0,0,2,"TooltipBasic",{
               "title":"Dwarf Hall — 225",
               "text":"Place the map-special Dwarf Hall barracks."
            }),new Array("qol_pirates","tw_soldier",200,false,0,0,0,3,"TooltipBasic",{
               "title":"Pirate Barracks — 200",
               "text":"Place the map-special Pirate Barracks."
            }),new Array("qol_repair_jungle","tw_clean",this.cRoot.gameSettings.§_-wX§.towerHolderLocked.repairCost,false,0,0,0,4,"TooltipBasic",{
               "title":"Jungle repair site",
               "text":"Restore a normal build spot for the game’s native jungle repair cost."
            }),new Array("qol_specials2","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"More towers →",
               "text":"Open the direct-build specialization page."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
         if(param1 == "qol_specials2")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_crossbow","tw_archer",this.cRoot.gameSettings.archers.crossbow.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"Crossbow Fort",
               "text":"Build the Crossbow specialization directly at its native specialization cost."
            }),new Array("qol_totem","tw_archer",this.cRoot.gameSettings.archers.totem.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Tribal Axethrowers",
               "text":"Build the Totem specialization directly at its native specialization cost."
            }),new Array("qol_archmage","tw_mage",this.cRoot.gameSettings.mages.archmage.cost,false,0,0,0,3,"TooltipBasic",{
               "title":"Archmage",
               "text":"Build the Archmage specialization directly."
            }),new Array("qol_necro","tw_mage",this.cRoot.gameSettings.mages.necromancer.cost,false,0,0,0,4,"TooltipBasic",{
               "title":"Necromancer",
               "text":"Build the Necromancer specialization directly."
            }),new Array("qol_specials3","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"More towers →",
               "text":"Open the final special-tower page."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
         if(param1 == "qol_specials3")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"DWAARP",
               "text":"Build the DWAARP specialization directly."
            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Battle-Mecha T200",
               "text":"Build the Battle-Mecha specialization directly."
            }),new Array("qol_repair_underground","tw_clean",this.cRoot.gameSettings.§_-wX§.towerHolderLocked.repairCostUnderground,false,0,0,0,3,"TooltipBasic",{
               "title":"Underground repair site",
               "text":"Restore a normal build spot for the game’s native underground repair cost."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← First special page",
               "text":"Return to the map-special tower page."
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
         if(param1 == "qol_dwarf")
         {
            if(this.cRoot.cash < 250) return;
            this.cRoot.updateCash(-250);
            this.qolPlaceSpecial(new TowerDwarfRiflemen(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
         if(param1 == "qol_hall")
         {
            if(this.cRoot.cash < 225) return;
            this.cRoot.updateCash(-225);
            this.qolPlaceSpecial(new §_-Zs§(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
         if(param1 == "qol_pirates")
         {
            if(this.cRoot.cash < 200) return;
            this.cRoot.updateCash(-200);
            this.qolPlaceSpecial(new TowerSoldierPirates(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
         if(param1 == "qol_repair_jungle")
         {
            var repairJungle:int = this.cRoot.gameSettings.§_-wX§.towerHolderLocked.repairCost;
            if(this.cRoot.cash < repairJungle) return;
            this.cRoot.updateCash(-repairJungle);
            this.cRoot.entities.addChild(new TowerHolder(this.x,this.y + this.yAdjust,this.§_-EV§,this.canBuildBarracks));
            this.destroyThis();
            return;
         }
         if(param1 == "qol_repair_underground")
         {
            var repairUnderground:int = this.cRoot.gameSettings.§_-wX§.towerHolderLocked.repairCostUnderground;
            if(this.cRoot.cash < repairUnderground) return;
            this.cRoot.updateCash(-repairUnderground);
            this.cRoot.entities.addChild(new TowerHolder(this.x,this.y + this.yAdjust,this.§_-EV§,this.canBuildBarracks));
            this.destroyThis();
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
    start = text.find('         if(param1 == "qol_specials")\n')
    if start < 0:
        die("special branch start missing")
    end = text.find('         if(param1 == "qol_back")\n', start)
    if end < 0:
        die("special branch end missing")
    return text[:start] + TOWER_BRANCH + "         " + text[end:]


def patch_quick_menu(text):
    old = 'if(param1 == "qol_specials" || param1 == "qol_specials2")'
    new = 'if(param1 == "qol_specials" || param1 == "qol_specials2" || param1 == "qol_specials3")'
    text = once(text, old, new, "special page navigation")
    marker = '         this.cTower.upgradeTower(param1);\n'
    special = r'''         if(param1.indexOf("qol_") == 0)
         {
            this.cTower.upgradeTower(param1);
            this.hide();
            return;
         }
'''
    return once(text, marker, special + marker, "safe special placement action")


def patch_taps(source_root, import_root):
    for name in ["§true break§.as","TowerDwarfRiflemen.as","TowerSoldierPirates.as","§_-Zs§.as"]:
        text = get_text(source_root, import_root, name)
        text = text.replace("MouseEvent.CLICK,this.clickEvent", "MouseEvent.MOUSE_DOWN,this.clickEvent")
        write_import(import_root, name, text)


def patch(source_root, import_root):
    for name, fn in [
        ("§_-2i§.as", patch_hero_data),
        ("§_-BQ§.as", patch_game),
        ("Level.as", patch_level),
        ("TowerHolder.as", patch_tower_holder),
        ("§_-LZ§.as", patch_quick_menu),
    ]:
        write_import(import_root, name, fn(get_text(source_root, import_root, name)))
    patch_taps(source_root, import_root)
    print("V4 finalize patches applied")


def verify(root):
    checks = {
        "Level.as": [
            "Level.qolHeroEnabled[heroName] = true",
            "RESET FOR CUSTOM",
            "qolEntityScratch",
            "qolUpdateContainer",
            "var heavy:Boolean",
        ],
        "§_-2i§.as": ["h.level = 10", "h.xp = this.master_xp[this.master_xp.length - 1]"],
        "§_-BQ§.as": ["qolProgressMode", 'this.qolSaveProgressMode(param1 ? "max" : "custom")'],
        "TowerHolder.as": ["Dwarf Hall — 225", "qol_repair_jungle", "qol_specials3", "repairCostUnderground"],
        "§_-LZ§.as": ["qol_specials3", 'param1.indexOf("qol_") == 0'],
        "§true break§.as": ["MouseEvent.MOUSE_DOWN,this.clickEvent"],
        "TowerDwarfRiflemen.as": ["MouseEvent.MOUSE_DOWN,this.clickEvent"],
        "TowerSoldierPirates.as": ["MouseEvent.MOUSE_DOWN,this.clickEvent"],
        "§_-Zs§.as": ["MouseEvent.MOUSE_DOWN,this.clickEvent"],
    }
    for name, needles in checks.items():
        text = read_file(root / name)
        for needle in needles:
            if needle not in text:
                die(f"verify failed: {name} missing {needle!r}")
    print("V4 finalize verification markers present")


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in {"patch", "verify"}:
        die("usage: build-v4-finalize.py patch <source-root> <import-root> | verify <verify-root>")
    if sys.argv[1] == "patch":
        if len(sys.argv) != 4:
            die("patch requires source and import roots")
        patch(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        verify(Path(sys.argv[2]))


if __name__ == "__main__":
    main()
