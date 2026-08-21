#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: build_source_mod.py <exported-scripts-root>')

root = Path(sys.argv[1])
base = root / 'scripts' / 'Game'

def read(rel):
    p = base / rel
    if not p.exists(): raise SystemExit(f'missing {p}')
    return p.read_text(encoding='utf-8-sig')

def write(rel, text):
    p = base / rel
    p.write_text(text, encoding='utf-8', newline='\n')

def once(text, old, new, label):
    n=text.count(old)
    if n != 1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old,new,1)

# ------------------------------------------------------------------
# DataManager: persistent sandbox progression applied to new AND old saves.
# ------------------------------------------------------------------
d = read('Manager/DataManager.as')
d = once(d,
'''   import flash.net.SharedObject;
''',
'''   import flash.net.SharedObject;
   import Game.System.StatDef.CharTotalStat;
''','DataManager import')

helper = r'''      public function sandboxMaxAll() : *
      {
         var ids:Array = [1,2,3,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,50,51,52,53,54,55,56,57,58,59,60];
         var id:int = 0;
         var s:CharTotalStat = null;
         for each(id in ids)
         {
            this.unitSetValue(id,"stat",1);
            this.unitSetValue(id,"exp",999999);
            s = new CharTotalStat(id);
            s.unlockAbility();
            this.unitSetValue(id,"ability1",s.unit_ability1_id);
            this.unitSetValue(id,"ability2",s.unit_ability2_id);
            this.unitSetValue(id,"ability3",s.unit_ability3_id);
            this.unitSetValue(id,"ability4",s.unit_ability4_id);
            this.unitSetValue(id,"ability5",s.unit_ability5_id);
            this.unitSetValue(id,"ability6",s.unit_ability6_id);
            this.unitSetValue(id,"ability7",s.unit_ability7_id);
            this.unitSetValue(id,"ability8",s.unit_ability8_id);
            this.unitSetValue(id,"ability9",s.unit_ability9_id);
         }
         for(id = 1; id <= 30; id++)
         {
            this.itemSetValue(id,99);
         }
         for(id = 1; id <= 12; id++) this.stageSetValue("normal",id,1);
         for(id = 1; id <= 8; id++) this.stageSetValue("extra",id,1);
         for(id = 1; id <= 5; id++) this.stageSetValue("trial",id,1);
         for(id = 1; id <= 10; id++) this.achievSetValue(id,2);
         this.stat_money = 99999999;
         this.mission_stage = 12;
         this.game_completed = 1;
         this.heroknight_competed = 1;
         this.heroqueen_competed = 1;
         this.herodemon_competed = 1;
         if(this.hero_select_id < 1 || this.hero_select_id > 3) this.hero_select_id = 1;
         if(this.unit_equip1_id == 0) this.unit_equip1_id = 10;
         if(this.unit_equip2_id == 0) this.unit_equip2_id = 13;
         if(this.unit_equip3_id == 0) this.unit_equip3_id = 18;
         if(this.unit_equip4_id == 0) this.unit_equip4_id = 24;
         if(this.unit_equip5_id == 0) this.unit_equip5_id = 54;
         if(this.unit_equip6_id == 0) this.unit_equip6_id = 55;
      }
      
'''
d = once(d,'      public function cheatMode() : *\n',helper+'      public function cheatMode() : *\n','sandbox helper insert')
d = once(d,
'''         this.loadArrayStringData();
         trace(" reset data ... ");
''',
'''         this.loadArrayStringData();
         this.sandboxMaxAll();
         trace(" reset data ... sandbox maxed ");
''','new save sandbox')
d = once(d,
'''         this.loadArrayStringData();
         trace("load data ..... ok");
         return true;
''',
'''         this.loadArrayStringData();
         this.sandboxMaxAll();
         this.saveData();
         trace("load data ..... ok / sandbox maxed");
         return true;
''','existing save sandbox')
d = once(d,
'''      public function cheatMode() : *
      {
         this.stat_money = 900000;
      }
''',
'''      public function cheatMode() : *
      {
         this.sandboxMaxAll();
         this.saveData();
      }
''','cheatMode expansion')
write('Manager/DataManager.as',d)

# ------------------------------------------------------------------
# BattleControlPlayer: huge mana pool and fast regeneration.
# ------------------------------------------------------------------
p = read('System/Battle/BattleControlPlayer.as')
p = once(p,'      private var manaMax:int = 100;','      private var manaMax:int = 9999;','mana max')
p = once(p,'      private var manaRegen:int = 1;','      private var manaRegen:int = 250;','mana regen')
p = once(p,
'''         this.bSys.ui.mana.val.htmlText = String(0);
         this.bSys.ui.mana.bar.scaleX = 0;
         this.stateControl = "init";
         this.mana = 0;
''',
'''         this.bSys.ui.mana.val.htmlText = String(this.manaMax);
         this.bSys.ui.mana.bar.scaleX = 1;
         this.stateControl = "init";
         this.mana = this.manaMax;
''','starting mana')
write('System/Battle/BattleControlPlayer.as',p)

# ------------------------------------------------------------------
# PlayerSpell: zero cost and essentially unlimited buildings.
# ------------------------------------------------------------------
s = read('System/Battle/PlayerSpell.as')
s = once(s,
'''            this.mana_cost = stat.spell_manacost;
            this.icoClip.mana.htmlText = String(this.mana_cost);
''',
'''            this.mana_cost = 0;
            this.icoClip.mana.htmlText = String("FREE");
''','free spell cost')
s = once(s,'               if(this.getTotalPlayerBuilding() < 4)','               if(this.getTotalPlayerBuilding() < 999)','building cap')
write('System/Battle/PlayerSpell.as',s)

# ------------------------------------------------------------------
# PlayerUnit: high population cap and rapid auto-production.
# ------------------------------------------------------------------
u = read('System/Battle/PlayerUnit.as')
u = once(u,
'''         this.pop_max = stat.pop;
         this.spawn_delay = stat.wait_spawn * 24;
''',
'''         this.pop_max = Math.max(stat.pop,12);
         this.spawn_delay = 6;
''','rapid units')
write('System/Battle/PlayerUnit.as',u)

# ------------------------------------------------------------------
# BattleSystem: keyboard-driven sandbox panel and arbitrary ally/enemy spawns.
# ------------------------------------------------------------------
b = read('System/Battle/BattleSystem.as')
b = once(b,
'''   import Game.System.GameObject.*;
''',
'''   import Game.System.GameObject.*;
   import flash.events.KeyboardEvent;
   import flash.text.TextField;
   import flash.text.TextFormat;
''','BattleSystem imports')

vars = r'''      private var sandboxNames:Array = ["hobbit","dwarf","elf","wizard","valkyrie","cavalry","centaurion","witch","vampire","anubis","goblin","succubus","troll","gorila","beastrider","dwarfenginer","bomber","taurus","tank","lamia","golem","lich","tiger","phoenix","angel","gaia","diablos","dragon","devil","baal","heroknight","heroqueen","herodemon"];
      
      private var sandboxIndex:int = 0;
      
      private var sandboxCount:int = 1;
      
      private var sandboxSpeedIndex:int = 0;
      
      private var sandboxHud:TextField = null;
      
'''
b = once(b,'      private var _frame_number_generate:int = 0;\n','      private var _frame_number_generate:int = 0;\n      \n'+vars,'sandbox vars')

helpers = r'''      private function sandboxInstall() : void
      {
         this.mGF.stageRoot.stage.addEventListener(KeyboardEvent.KEY_DOWN,this.sandboxKey,false,0,true);
         this.sandboxHud = new TextField();
         this.sandboxHud.defaultTextFormat = new TextFormat("_sans",12,16777215,true);
         this.sandboxHud.width = 700;
         this.sandboxHud.height = 64;
         this.sandboxHud.x = 8;
         this.sandboxHud.y = 4;
         this.sandboxHud.background = true;
         this.sandboxHud.backgroundColor = 0;
         this.sandboxHud.alpha = 0.82;
         this.sandboxHud.mouseEnabled = false;
         this.sandboxHud.selectable = false;
         this.ui.addChild(this.sandboxHud);
         this.sandboxRefresh();
      }
      
      private function sandboxRefresh(MSG:String = "") : void
      {
         if(this.sandboxHud == null) return;
         var name:String = String(this.sandboxNames[this.sandboxIndex]);
         this.sandboxHud.text = "EPIC WAR 5 SANDBOX  |  unit: " + name + "  |  batch: " + this.sandboxCount + "\nF1 mana  F2/F3 unit  F4 ally  F5 enemy  F6 batch  F7 speed  F8 wipe enemies  F9 win  F10 heal allies" + (MSG == "" ? "" : "  |  " + MSG);
      }
      
      private function sandboxCycle(DELTA:int) : void
      {
         this.sandboxIndex += DELTA;
         if(this.sandboxIndex < 0) this.sandboxIndex = this.sandboxNames.length - 1;
         if(this.sandboxIndex >= this.sandboxNames.length) this.sandboxIndex = 0;
         this.sandboxRefresh();
      }
      
      private function sandboxSpawn(ALLY:Boolean) : void
      {
         var i:int = 0;
         var name:String = String(this.sandboxNames[this.sandboxIndex]);
         for(i = 0; i < this.sandboxCount; i++)
         {
            if(ALLY)
            {
               this.charMgr.createPlayerUnit("unit",name,600 + Math.random() * 150,90 + i);
            }
            else
            {
               this.charMgr.createEnemyUnit("unit",name,this.x_area_width - 250 + Math.random() * 120,0,80 + i,0,0,"",1);
            }
         }
         this.sandboxRefresh((ALLY ? "ally x" : "enemy x") + this.sandboxCount);
      }
      
      private function sandboxWipeEnemies() : void
      {
         var child:* = null;
         var i:int = 0;
         for(i = this.mGF.contUNIT.numChildren - 1; i >= 0; i--)
         {
            child = this.mGF.contUNIT.getChildAt(i);
            if(child != null && child.isAlignmentAs("enemy")) child.setDamage(99999999);
         }
         this.sandboxRefresh("enemy wipe");
      }
      
      private function sandboxHealAllies() : void
      {
         var child:* = null;
         var i:int = 0;
         for(i = 0; i < this.mGF.contUNIT.numChildren; i++)
         {
            child = this.mGF.contUNIT.getChildAt(i);
            if(child != null && child.isAlignmentAs("ally")) child.setDamageHeal(99999999);
         }
         this.sandboxRefresh("allies healed");
      }
      
      private function sandboxKey(e:KeyboardEvent) : void
      {
         if(e.keyCode == 112)
         {
            this.playerMgr.setMana(9999);
            this.sandboxRefresh("mana filled");
         }
         else if(e.keyCode == 113) this.sandboxCycle(-1);
         else if(e.keyCode == 114) this.sandboxCycle(1);
         else if(e.keyCode == 115) this.sandboxSpawn(true);
         else if(e.keyCode == 116) this.sandboxSpawn(false);
         else if(e.keyCode == 117)
         {
            if(this.sandboxCount == 1) this.sandboxCount = 5;
            else if(this.sandboxCount == 5) this.sandboxCount = 20;
            else if(this.sandboxCount == 20) this.sandboxCount = 50;
            else this.sandboxCount = 1;
            this.sandboxRefresh();
         }
         else if(e.keyCode == 118)
         {
            this.sandboxSpeedIndex = (this.sandboxSpeedIndex + 1) % 3;
            if(this.sandboxSpeedIndex == 0) this.mGF.stageRoot.stage.frameRate = 24;
            else if(this.sandboxSpeedIndex == 1) this.mGF.stageRoot.stage.frameRate = 96;
            else this.mGF.stageRoot.stage.frameRate = 192;
            this.sandboxRefresh("speed " + (this.sandboxSpeedIndex == 0 ? "1x" : this.sandboxSpeedIndex == 1 ? "4x" : "8x"));
         }
         else if(e.keyCode == 119) this.sandboxWipeEnemies();
         else if(e.keyCode == 120)
         {
            this.battle_result = "win";
            this.battle_boss_kill = Math.max(this.battle_boss_kill,1);
            this.sandboxRefresh("instant win");
         }
         else if(e.keyCode == 121) this.sandboxHealAllies();
      }
      
'''
b = once(b,'      public function showBattleMenu() : *\n',helpers+'      public function showBattleMenu() : *\n','sandbox helpers')
b = once(b,
'''         this.enemyMgr = new BattleControlEnemy(this.mGF,this);
         this.enemyMgr.init();
         this.mGF.isPaused = false;
''',
'''         this.enemyMgr = new BattleControlEnemy(this.mGF,this);
         this.enemyMgr.init();
         this.mGF.isPaused = false;
         this.sandboxInstall();
''','sandbox install')
b = once(b,
'''      public function destroy() : *
      {
         this.mGF.stageRoot.stage.frameRate = 24;
''',
'''      public function destroy() : *
      {
         try { this.mGF.stageRoot.stage.removeEventListener(KeyboardEvent.KEY_DOWN,this.sandboxKey); } catch(e:Error) {}
         if(this.sandboxHud != null && this.sandboxHud.parent != null) this.sandboxHud.parent.removeChild(this.sandboxHud);
         this.sandboxHud = null;
         this.mGF.stageRoot.stage.frameRate = 24;
''','sandbox destroy')
write('System/Battle/BattleSystem.as',b)

# Validation
checks = {
 'Manager/DataManager.as':['sandboxMaxAll','99999999','new CharTotalStat(id)','stageSetValue("trial"'],
 'System/Battle/BattleControlPlayer.as':['manaMax:int = 9999','manaRegen:int = 250'],
 'System/Battle/PlayerSpell.as':['String("FREE")','< 999'],
 'System/Battle/PlayerUnit.as':['Math.max(stat.pop,12)','spawn_delay = 6'],
 'System/Battle/BattleSystem.as':['EPIC WAR 5 SANDBOX','sandboxSpawn','KeyboardEvent.KEY_DOWN','F10 heal allies']
}
for rel, needles in checks.items():
    text=read(rel)
    for needle in needles:
        if needle not in text: raise SystemExit(f'validation failed: {needle} missing in {rel}')
print('Epic War 5 extensive sandbox source patches applied')
