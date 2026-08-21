#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: build_source_mod_v2.py <exported-scripts-root>')
root=Path(sys.argv[1]); base=root/'scripts'/'Game'

def read(rel):
    p=base/rel
    if not p.exists(): raise SystemExit(f'missing {p}')
    return p.read_text(encoding='utf-8-sig')
def write(rel,text): (base/rel).write_text(text,encoding='utf-8',newline='\n')
def once(text,old,new,label):
    n=text.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old,new,1)

# DataManager: keep vanilla progression by default. Preserve optional max-all helper only.
d=read('Manager/DataManager.as')
d=once(d,'   import flash.net.SharedObject;\n','   import flash.net.SharedObject;\n   import Game.System.StatDef.CharTotalStat;\n','DataManager import')
helper=r'''      public function sandboxMaxAll() : *
      {
         var ids:Array = [1,2,3,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,50,51,52,53,54,55,56,57,58,59,60];
         var id:int = 0;
         var s:CharTotalStat = null;
         for each(id in ids)
         {
            this.unitSetValue(id,"stat",1);
            this.unitSetValue(id,"exp",999999);
            s = new CharTotalStat(id); s.unlockAbility();
            this.unitSetValue(id,"ability1",s.unit_ability1_id); this.unitSetValue(id,"ability2",s.unit_ability2_id);
            this.unitSetValue(id,"ability3",s.unit_ability3_id); this.unitSetValue(id,"ability4",s.unit_ability4_id);
            this.unitSetValue(id,"ability5",s.unit_ability5_id); this.unitSetValue(id,"ability6",s.unit_ability6_id);
            this.unitSetValue(id,"ability7",s.unit_ability7_id); this.unitSetValue(id,"ability8",s.unit_ability8_id);
            this.unitSetValue(id,"ability9",s.unit_ability9_id);
         }
         for(id=1;id<=30;id++) this.itemSetValue(id,99);
         for(id=1;id<=12;id++) this.stageSetValue("normal",id,1);
         for(id=1;id<=8;id++) this.stageSetValue("extra",id,1);
         for(id=1;id<=5;id++) this.stageSetValue("trial",id,1);
         this.stat_money = 99999999; this.mission_stage=12; this.game_completed=1;
         this.heroknight_competed=1; this.heroqueen_competed=1; this.herodemon_competed=1;
         this.saveData();
      }
      
'''
d=once(d,'      public function cheatMode() : *\n',helper+'      public function cheatMode() : *\n','sandbox helper')
# Native cheatMode remains an explicit max-all action, but nothing calls it automatically.
d=once(d,'      public function cheatMode() : *\n      {\n         this.stat_money = 900000;\n      }\n','      public function cheatMode() : *\n      {\n         this.sandboxMaxAll();\n      }\n','cheatMode')
write('Manager/DataManager.as',d)

# BattleControlPlayer: keep vanilla max/regen/start and add an adjustable mana helper.
p=read('System/Battle/BattleControlPlayer.as')
insert=r'''      public function sandboxAddMana(AMOUNT:int) : void
      {
         if(AMOUNT < 0) AMOUNT = 0;
         this.mana += AMOUNT;
         if(this.mana > 9999) this.mana = 9999;
         this.bSys.ui.mana.val.htmlText = String(this.mana);
         this.bSys.ui.mana.bar.scaleX = Math.min(1,this.mana / this.manaMax);
      }
      
'''
p=once(p,'      public function setMana(VAL:int) : *\n',insert+'      public function setMana(VAL:int) : *\n','mana helper')
write('System/Battle/BattleControlPlayer.as',p)

# PlayerSpell: free spells/build cap are runtime toggles, default OFF.
s=read('System/Battle/PlayerSpell.as')
s=once(s,'            this.mana_cost = stat.spell_manacost;\n            this.icoClip.mana.htmlText = String(this.mana_cost);\n','            this.mana_cost = BattleSystem.sandboxFreeSpells ? 0 : stat.spell_manacost;\n            this.icoClip.mana.htmlText = this.mana_cost == 0 ? String("FREE") : String(this.mana_cost);\n','free spell toggle')
s=once(s,'               if(this.getTotalPlayerBuilding() < 4)','               if(this.getTotalPlayerBuilding() < (BattleSystem.sandboxUnlimitedBuildings ? 999 : 4))','building toggle')
write('System/Battle/PlayerSpell.as',s)

# PlayerUnit: fast production and population boost are runtime toggles, default OFF.
u=read('System/Battle/PlayerUnit.as')
u=once(u,'         this.pop_max = stat.pop;\n         this.spawn_delay = stat.wait_spawn * 24;\n','         this.pop_max = BattleSystem.sandboxPopBoost ? Math.max(stat.pop,BattleSystem.sandboxPopAmount) : stat.pop;\n         this.spawn_delay = BattleSystem.sandboxFastUnits ? BattleSystem.sandboxSpawnDelay : stat.wait_spawn * 24;\n','unit toggles')
write('System/Battle/PlayerUnit.as',u)

# BattleSystem: opt-in sandbox controls; all gameplay-affecting toggles start OFF.
b=read('System/Battle/BattleSystem.as')
b=once(b,'   import Game.System.GameObject.*;\n','   import Game.System.GameObject.*;\n   import flash.events.KeyboardEvent;\n   import flash.text.TextField;\n   import flash.text.TextFormat;\n','Battle imports')
vars=r'''      public static var sandboxFreeSpells:Boolean = false;
      public static var sandboxUnlimitedBuildings:Boolean = false;
      public static var sandboxFastUnits:Boolean = false;
      public static var sandboxPopBoost:Boolean = false;
      public static var sandboxPopAmount:int = 12;
      public static var sandboxSpawnDelay:int = 6;
      private var sandboxNames:Array = ["hobbit","dwarf","elf","wizard","valkyrie","cavalry","centaurion","witch","vampire","anubis","goblin","succubus","troll","gorila","beastrider","dwarfenginer","bomber","taurus","tank","lamia","golem","lich","tiger","phoenix","angel","gaia","diablos","dragon","devil","baal","heroknight","heroqueen","herodemon"];
      private var sandboxIndex:int = 0;
      private var sandboxCount:int = 1;
      private var sandboxManaAmount:int = 100;
      private var sandboxSpeedIndex:int = 0;
      private var sandboxHud:TextField = null;
      private var sandboxHudVisible:Boolean = true;
      
'''
b=once(b,'      private var _frame_number_generate:int = 0;\n','      private var _frame_number_generate:int = 0;\n      \n'+vars,'sandbox vars')
helpers=r'''      private function sandboxInstall() : void
      {
         this.mGF.stageRoot.stage.addEventListener(KeyboardEvent.KEY_DOWN,this.sandboxKey,false,0,true);
         this.sandboxHud = new TextField(); this.sandboxHud.defaultTextFormat = new TextFormat("_sans",11,16777215,true);
         this.sandboxHud.width=760; this.sandboxHud.height=84; this.sandboxHud.x=8; this.sandboxHud.y=4;
         this.sandboxHud.background=true; this.sandboxHud.backgroundColor=0; this.sandboxHud.alpha=0.82;
         this.sandboxHud.mouseEnabled=false; this.sandboxHud.selectable=false; this.ui.addChild(this.sandboxHud); this.sandboxRefresh();
      }
      private function sandboxOnOff(V:Boolean) : String { return V ? "ON" : "off"; }
      private function sandboxRefresh(MSG:String="") : void
      {
         if(this.sandboxHud==null) return;
         var name:String=String(this.sandboxNames[this.sandboxIndex]);
         this.sandboxHud.visible=this.sandboxHudVisible;
         this.sandboxHud.text="SANDBOX (vanilla defaults) | unit:"+name+" batch:"+this.sandboxCount+" mana+:"+this.sandboxManaAmount+"\nFREE:"+sandboxOnOff(sandboxFreeSpells)+" BUILD∞:"+sandboxOnOff(sandboxUnlimitedBuildings)+" FAST:"+sandboxOnOff(sandboxFastUnits)+" POP:"+sandboxOnOff(sandboxPopBoost)+"("+sandboxPopAmount+")\nF1 add mana | F2/F3 unit | F4 ally | F5 enemy | F6 batch | F7 speed | F8 wipe | F9 win | F10 heal | F11 free spells | F12 fast units | B buildings | P population | [ ] mana amount | ` HUD"+(MSG==""?"":" | "+MSG);
      }
      private function sandboxCycle(DELTA:int) : void { this.sandboxIndex+=DELTA; if(this.sandboxIndex<0)this.sandboxIndex=this.sandboxNames.length-1; if(this.sandboxIndex>=this.sandboxNames.length)this.sandboxIndex=0; this.sandboxRefresh(); }
      private function sandboxSpawn(ALLY:Boolean) : void
      {
         var i:int=0; var name:String=String(this.sandboxNames[this.sandboxIndex]);
         for(i=0;i<this.sandboxCount;i++) { if(ALLY) this.charMgr.createPlayerUnit("unit",name,600+Math.random()*150,90+i); else this.charMgr.createEnemyUnit("unit",name,this.x_area_width-250+Math.random()*120,0,80+i,0,0,"",1); }
         this.sandboxRefresh((ALLY?"ally x":"enemy x")+this.sandboxCount);
      }
      private function sandboxWipeEnemies() : void { var c:*; var i:int; for(i=this.mGF.contUNIT.numChildren-1;i>=0;i--){c=this.mGF.contUNIT.getChildAt(i); if(c!=null&&c.isAlignmentAs("enemy"))c.setDamage(99999999);} this.sandboxRefresh("enemy wipe"); }
      private function sandboxHealAllies() : void { var c:*; var i:int; for(i=0;i<this.mGF.contUNIT.numChildren;i++){c=this.mGF.contUNIT.getChildAt(i); if(c!=null&&c.isAlignmentAs("ally"))c.setDamageHeal(99999999);} this.sandboxRefresh("allies healed"); }
      private function sandboxKey(e:KeyboardEvent) : void
      {
         if(e.keyCode==112) { this.playerMgr.sandboxAddMana(this.sandboxManaAmount); this.sandboxRefresh("+"+this.sandboxManaAmount+" mana"); }
         else if(e.keyCode==113) this.sandboxCycle(-1);
         else if(e.keyCode==114) this.sandboxCycle(1);
         else if(e.keyCode==115) this.sandboxSpawn(true);
         else if(e.keyCode==116) this.sandboxSpawn(false);
         else if(e.keyCode==117) { if(this.sandboxCount==1)this.sandboxCount=5; else if(this.sandboxCount==5)this.sandboxCount=20; else if(this.sandboxCount==20)this.sandboxCount=50; else this.sandboxCount=1; this.sandboxRefresh(); }
         else if(e.keyCode==118) { this.sandboxSpeedIndex=(this.sandboxSpeedIndex+1)%3; this.mGF.stageRoot.stage.frameRate=this.sandboxSpeedIndex==0?24:(this.sandboxSpeedIndex==1?96:192); this.sandboxRefresh("speed "+(this.sandboxSpeedIndex==0?"1x":(this.sandboxSpeedIndex==1?"4x":"8x"))); }
         else if(e.keyCode==119) this.sandboxWipeEnemies();
         else if(e.keyCode==120) { this.battle_result="win"; this.battle_boss_kill=Math.max(this.battle_boss_kill,1); this.sandboxRefresh("instant win"); }
         else if(e.keyCode==121) this.sandboxHealAllies();
         else if(e.keyCode==122) { sandboxFreeSpells=!sandboxFreeSpells; this.sandboxRefresh("free spells "+sandboxOnOff(sandboxFreeSpells)); }
         else if(e.keyCode==123) { sandboxFastUnits=!sandboxFastUnits; this.sandboxRefresh("fast units "+sandboxOnOff(sandboxFastUnits)+" (new spawners)"); }
         else if(e.keyCode==66) { sandboxUnlimitedBuildings=!sandboxUnlimitedBuildings; this.sandboxRefresh("unlimited buildings "+sandboxOnOff(sandboxUnlimitedBuildings)); }
         else if(e.keyCode==80) { sandboxPopBoost=!sandboxPopBoost; this.sandboxRefresh("population boost "+sandboxOnOff(sandboxPopBoost)+" (new spawners)"); }
         else if(e.keyCode==219) { this.sandboxManaAmount=Math.max(10,int(this.sandboxManaAmount/2)); this.sandboxRefresh(); }
         else if(e.keyCode==221) { this.sandboxManaAmount=Math.min(5000,this.sandboxManaAmount*2); this.sandboxRefresh(); }
         else if(e.keyCode==192) { this.sandboxHudVisible=!this.sandboxHudVisible; this.sandboxRefresh(); }
      }
      
'''
b=once(b,'      public function showBattleMenu() : *\n',helpers+'      public function showBattleMenu() : *\n','sandbox helpers')
b=once(b,'         this.enemyMgr = new BattleControlEnemy(this.mGF,this);\n         this.enemyMgr.init();\n         this.mGF.isPaused = false;\n','         this.enemyMgr = new BattleControlEnemy(this.mGF,this);\n         this.enemyMgr.init();\n         this.mGF.isPaused = false;\n         this.sandboxInstall();\n','sandbox install')
b=once(b,'      public function destroy() : *\n      {\n         this.mGF.stageRoot.stage.frameRate = 24;\n','      public function destroy() : *\n      {\n         try { this.mGF.stageRoot.stage.removeEventListener(KeyboardEvent.KEY_DOWN,this.sandboxKey); } catch(e:Error) {}\n         if(this.sandboxHud!=null&&this.sandboxHud.parent!=null)this.sandboxHud.parent.removeChild(this.sandboxHud); this.sandboxHud=null;\n         this.mGF.stageRoot.stage.frameRate = 24;\n','sandbox destroy')
write('System/Battle/BattleSystem.as',b)

checks={
'Manager/DataManager.as':['sandboxMaxAll','this.sandboxMaxAll();'],
'System/Battle/BattleControlPlayer.as':['sandboxAddMana'],
'System/Battle/PlayerSpell.as':['sandboxFreeSpells','sandboxUnlimitedBuildings'],
'System/Battle/PlayerUnit.as':['sandboxPopBoost','sandboxFastUnits'],
'System/Battle/BattleSystem.as':['vanilla defaults','sandboxManaAmount','sandboxFreeSpells:Boolean = false','sandboxFastUnits:Boolean = false']}
for rel,needles in checks.items():
    t=read(rel)
    for n in needles:
        if n not in t: raise SystemExit(f'validation failed: {n} missing in {rel}')
print('Epic War 5 vanilla-by-default sandbox V2 patches applied')
