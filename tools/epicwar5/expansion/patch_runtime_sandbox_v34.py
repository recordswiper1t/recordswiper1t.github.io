#!/usr/bin/env python3
"""Epic War 5 Expansion V3.4 runtime + optional sandbox patch.

Baseline: exact released Expansion V3.3.1. This patch deliberately does not
rebuild the expansion from older layers. It fixes the custom world-map battle
transition to follow the original game's deferred ENTER_FRAME lifecycle and
adds a battle-only sandbox that is OFF by default.
"""
from pathlib import Path
import re, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_runtime_sandbox_v34.py <ffdec-export-root>')

root = Path(sys.argv[1]) / 'scripts' / 'Game'

def read(rel):
    p = root / rel
    if not p.is_file():
        raise SystemExit(f'missing {p}')
    return p.read_text(encoding='utf-8-sig')

def write(rel, text):
    (root / rel).write_text(text, encoding='utf-8', newline='\n')

def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)

def sub_once(text, pattern, repl, label, flags=0):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 regex match, got {n}')
    return out

# ---------------------------------------------------------------------------
# 1. WorldMap: defer custom Expansion battle construction to ENTER_FRAME.
# The stock WorldMapArea classes only start a battle from frameHandle after a
# click/confirmation. V3.3.1 created battle_mc and destroyed WorldMap directly
# inside MouseEvent.CLICK, creating a display-list transition reentrancy hazard.
# ---------------------------------------------------------------------------
w = read('Interface/WorldMap.as')
w = once(
    w,
    '      private var expansionStageButtons:Array = [];\n',
    '      private var expansionStageButtons:Array = [];\n      \n      private var expansionPendingStage:int = 0;\n',
    'WorldMap pending-stage field'
)
w = once(
    w,
'''      private function frameHandle(event:Event) : void
      {
         var clip:* = undefined;
         if(this.confirmQuit.isOk())
''',
'''      private function frameHandle(event:Event) : void
      {
         var clip:* = undefined;
         if(this.expansionPendingStage > 0)
         {
            clip = new battle_mc();
            clip.init(this.mGF,this.expansionPendingStage);
            this.expansionPendingStage = 0;
            this.destroy();
            return;
         }
         if(this.confirmQuit.isOk())
''',
    'WorldMap deferred transition'
)
w = sub_once(
    w,
    r'''      private function expansionStageClick\(event:MouseEvent\) : void\n      \{.*?\n      \}\n      \n      private function expansionCloseClick''',
'''      private function expansionStageClick(event:MouseEvent) : void
      {
         var b:* = event.currentTarget;
         var id:int = int(String(b.name).replace("expansionStage_",""));
         if(id < 1 || id > 25)
         {
            return;
         }
         if(id > 1 && this.mGF.datMgr.stageGetValue("expansion",id - 1) < 1)
         {
            return;
         }
         this.expansionPendingStage = 100 + id;
         this.expansionDestroyPanel();
      }
      
      private function expansionCloseClick''',
    'WorldMap expansionStageClick',
    re.S
)
write('Interface/WorldMap.as', w)

# ---------------------------------------------------------------------------
# 2. BattleControlPlayer: additive mana helper. No progression/save mutation.
# ---------------------------------------------------------------------------
bp = read('System/Battle/BattleControlPlayer.as')
if 'public function sandboxAddMana' not in bp:
    insert = '''      public function sandboxAddMana(AMOUNT:int) : void
      {
         if(AMOUNT < 0)
         {
            AMOUNT = 0;
         }
         this.mana += AMOUNT;
         if(this.mana > 9999)
         {
            this.mana = 9999;
         }
         this.bSys.ui.mana.val.htmlText = String(this.mana);
         this.bSys.ui.mana.bar.scaleX = Math.min(1,this.mana / this.manaMax);
      }
      
'''
    m = re.search(r'(?m)^      public function setMana\([^\n]+\) : \*$', bp)
    if not m:
        raise SystemExit('BattleControlPlayer: setMana signature not found')
    bp = bp[:m.start()] + insert + bp[m.start():]
write('System/Battle/BattleControlPlayer.as', bp)

# ---------------------------------------------------------------------------
# 3. Runtime feature gates. Every gameplay-changing switch requires the master
# sandbox flag AND its individual toggle; the master starts false at SWF load.
# ---------------------------------------------------------------------------
ps = read('System/Battle/PlayerSpell.as')
ps = sub_once(
    ps,
    r'this\.mana_cost\s*=\s*stat\.spell_manacost;',
    'this.mana_cost = BattleSystem.sandboxMaster && BattleSystem.sandboxFreeSpells ? 0 : stat.spell_manacost;',
    'PlayerSpell mana cost'
)
ps = sub_once(
    ps,
    r'this\.getTotalPlayerBuilding\(\)\s*<\s*4',
    'this.getTotalPlayerBuilding() < (BattleSystem.sandboxMaster && BattleSystem.sandboxUnlimitedBuildings ? 999 : 4)',
    'PlayerSpell building cap'
)
write('System/Battle/PlayerSpell.as', ps)

pu = read('System/Battle/PlayerUnit.as')
pu = sub_once(
    pu,
    r'this\.pop_max\s*=\s*stat\.pop;',
    'this.pop_max = BattleSystem.sandboxMaster && BattleSystem.sandboxPopBoost ? Math.max(stat.pop,BattleSystem.sandboxPopAmount) : stat.pop;',
    'PlayerUnit population'
)
pu = sub_once(
    pu,
    r'this\.spawn_delay\s*=\s*stat\.wait_spawn\s*\*\s*24;',
    'this.spawn_delay = BattleSystem.sandboxMaster && BattleSystem.sandboxFastUnits ? BattleSystem.sandboxSpawnDelay : stat.wait_spawn * 24;',
    'PlayerUnit spawn delay'
)
write('System/Battle/PlayerUnit.as', pu)

# ---------------------------------------------------------------------------
# 4. BattleSystem: opt-in keyboard sandbox.
# ` toggles the sandbox master. Nothing else responds while master is OFF.
# B/P are intentionally NOT stolen from EW5's native battle controls; U/O are
# used for buildings/population instead.
# ---------------------------------------------------------------------------
bs = read('System/Battle/BattleSystem.as')
bs = once(
    bs,
    '   import Game.System.GameObject.*;\n',
    '   import Game.System.GameObject.*;\n   import flash.events.KeyboardEvent;\n   import flash.text.TextField;\n   import flash.text.TextFormat;\n',
    'BattleSystem imports'
)
vars_block = '''      public static var sandboxMaster:Boolean = false;
      public static var sandboxFreeSpells:Boolean = false;
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
bs = once(
    bs,
    '      private var _adaptive_quality_low:Boolean = false;\n',
    '      private var _adaptive_quality_low:Boolean = false;\n      \n' + vars_block,
    'BattleSystem sandbox vars'
)
helpers = r'''      private function sandboxInstall() : void
      {
         this.mGF.stageRoot.stage.addEventListener(KeyboardEvent.KEY_DOWN,this.sandboxKey,false,0,true);
         this.sandboxHud = new TextField();
         this.sandboxHud.defaultTextFormat = new TextFormat("_sans",11,16777215,true);
         this.sandboxHud.width = 760;
         this.sandboxHud.height = 84;
         this.sandboxHud.x = 8;
         this.sandboxHud.y = 4;
         this.sandboxHud.background = true;
         this.sandboxHud.backgroundColor = 0;
         this.sandboxHud.alpha = 0.82;
         this.sandboxHud.mouseEnabled = false;
         this.sandboxHud.selectable = false;
         this.ui.addChild(this.sandboxHud);
         this.sandboxHud.visible = sandboxMaster;
         if(sandboxMaster)
         {
            this.sandboxRefresh("sandbox active");
         }
      }
      
      private function sandboxOnOff(V:Boolean) : String
      {
         return V ? "ON" : "off";
      }
      
      private function sandboxResetToggles() : void
      {
         sandboxFreeSpells = false;
         sandboxUnlimitedBuildings = false;
         sandboxFastUnits = false;
         sandboxPopBoost = false;
         this.sandboxSpeedIndex = 0;
         this.mGF.stageRoot.stage.frameRate = 24;
      }
      
      private function sandboxRefresh(MSG:String = "") : void
      {
         if(this.sandboxHud == null)
         {
            return;
         }
         this.sandboxHud.visible = sandboxMaster && this.sandboxHudVisible;
         if(!sandboxMaster)
         {
            return;
         }
         var name:String = String(this.sandboxNames[this.sandboxIndex]);
         this.sandboxHud.text = "EXPANSION SANDBOX | unit:" + name + " batch:" + this.sandboxCount + " mana+:" + this.sandboxManaAmount + "\nFREE:" + sandboxOnOff(sandboxFreeSpells) + " BUILD∞:" + sandboxOnOff(sandboxUnlimitedBuildings) + " FAST:" + sandboxOnOff(sandboxFastUnits) + " POP:" + sandboxOnOff(sandboxPopBoost) + "(" + sandboxPopAmount + ")\n` disable | F1 mana | F2/F3 unit | F4 ally | F5 enemy | F6 batch | F7 speed | F8 wipe | F9 win | F10 heal | F11 free | F12 fast | U buildings | O population | [ ] mana | H HUD" + (MSG == "" ? "" : " | " + MSG);
      }
      
      private function sandboxCycle(DELTA:int) : void
      {
         this.sandboxIndex += DELTA;
         if(this.sandboxIndex < 0)
         {
            this.sandboxIndex = this.sandboxNames.length - 1;
         }
         if(this.sandboxIndex >= this.sandboxNames.length)
         {
            this.sandboxIndex = 0;
         }
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
         var c:* = null;
         var i:int = 0;
         for(i = this.mGF.contUNIT.numChildren - 1; i >= 0; i--)
         {
            c = this.mGF.contUNIT.getChildAt(i);
            if(c != null && c.isAlignmentAs("enemy"))
            {
               c.setDamage(99999999);
            }
         }
         this.sandboxRefresh("enemy wipe");
      }
      
      private function sandboxHealAllies() : void
      {
         var c:* = null;
         var i:int = 0;
         for(i = 0; i < this.mGF.contUNIT.numChildren; i++)
         {
            c = this.mGF.contUNIT.getChildAt(i);
            if(c != null && c.isAlignmentAs("ally"))
            {
               c.setDamageHeal(99999999);
            }
         }
         this.sandboxRefresh("allies healed");
      }
      
      private function sandboxKey(e:KeyboardEvent) : void
      {
         if(e.keyCode == 192)
         {
            sandboxMaster = !sandboxMaster;
            if(!sandboxMaster)
            {
               this.sandboxResetToggles();
               if(this.sandboxHud != null)
               {
                  this.sandboxHud.visible = false;
               }
               return;
            }
            this.sandboxHudVisible = true;
            this.sandboxRefresh("sandbox enabled");
            return;
         }
         if(!sandboxMaster)
         {
            return;
         }
         if(e.keyCode == 112)
         {
            this.playerMgr.sandboxAddMana(this.sandboxManaAmount);
            this.sandboxRefresh("+" + this.sandboxManaAmount + " mana");
         }
         else if(e.keyCode == 113)
         {
            this.sandboxCycle(-1);
         }
         else if(e.keyCode == 114)
         {
            this.sandboxCycle(1);
         }
         else if(e.keyCode == 115)
         {
            this.sandboxSpawn(true);
         }
         else if(e.keyCode == 116)
         {
            this.sandboxSpawn(false);
         }
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
            this.mGF.stageRoot.stage.frameRate = this.sandboxSpeedIndex == 0 ? 24 : (this.sandboxSpeedIndex == 1 ? 96 : 192);
            this.sandboxRefresh("speed " + (this.sandboxSpeedIndex == 0 ? "1x" : (this.sandboxSpeedIndex == 1 ? "4x" : "8x")));
         }
         else if(e.keyCode == 119)
         {
            this.sandboxWipeEnemies();
         }
         else if(e.keyCode == 120)
         {
            this.battle_result = "win";
            this.battle_boss_kill = Math.max(this.battle_boss_kill,1);
            this.sandboxRefresh("instant win");
         }
         else if(e.keyCode == 121)
         {
            this.sandboxHealAllies();
         }
         else if(e.keyCode == 122)
         {
            sandboxFreeSpells = !sandboxFreeSpells;
            this.sandboxRefresh("free spells " + sandboxOnOff(sandboxFreeSpells));
         }
         else if(e.keyCode == 123)
         {
            sandboxFastUnits = !sandboxFastUnits;
            this.sandboxRefresh("fast units " + sandboxOnOff(sandboxFastUnits) + " (next battle/spawner)");
         }
         else if(e.keyCode == 85)
         {
            sandboxUnlimitedBuildings = !sandboxUnlimitedBuildings;
            this.sandboxRefresh("unlimited buildings " + sandboxOnOff(sandboxUnlimitedBuildings));
         }
         else if(e.keyCode == 79)
         {
            sandboxPopBoost = !sandboxPopBoost;
            this.sandboxRefresh("population boost " + sandboxOnOff(sandboxPopBoost) + " (next battle/spawner)");
         }
         else if(e.keyCode == 219)
         {
            this.sandboxManaAmount = Math.max(10,int(this.sandboxManaAmount / 2));
            this.sandboxRefresh();
         }
         else if(e.keyCode == 221)
         {
            this.sandboxManaAmount = Math.min(5000,this.sandboxManaAmount * 2);
            this.sandboxRefresh();
         }
         else if(e.keyCode == 72)
         {
            this.sandboxHudVisible = !this.sandboxHudVisible;
            this.sandboxRefresh();
         }
      }
      
'''
bs = once(
    bs,
    '      public function showBattleMenu() : *\n',
    helpers + '      public function showBattleMenu() : *\n',
    'BattleSystem sandbox helpers'
)
bs = once(
    bs,
    '         this.enemyMgr = new BattleControlEnemy(this.mGF,this);\n         this.enemyMgr.init();\n         this.mGF.isPaused = false;\n',
    '         this.enemyMgr = new BattleControlEnemy(this.mGF,this);\n         this.enemyMgr.init();\n         this.mGF.isPaused = false;\n         this.sandboxInstall();\n',
    'BattleSystem sandbox install'
)
bs = once(
    bs,
    '      public function destroy() : *\n      {\n         this.mGF.stageRoot.stage.frameRate = 24;\n',
    '      public function destroy() : *\n      {\n         try { this.mGF.stageRoot.stage.removeEventListener(KeyboardEvent.KEY_DOWN,this.sandboxKey); } catch(e:Error) {}\n         if(this.sandboxHud != null && this.sandboxHud.parent != null)\n         {\n            this.sandboxHud.parent.removeChild(this.sandboxHud);\n         }\n         this.sandboxHud = null;\n         this.mGF.stageRoot.stage.frameRate = 24;\n',
    'BattleSystem sandbox destroy'
)
write('System/Battle/BattleSystem.as', bs)

# Verification of patch application before FFDec import.
checks = {
    'Interface/WorldMap.as': [
        'expansionPendingStage:int = 0',
        'this.expansionPendingStage = 100 + id;',
        'if(this.expansionPendingStage > 0)',
    ],
    'System/Battle/BattleSystem.as': [
        'sandboxMaster:Boolean = false',
        'if(!sandboxMaster)',
        'EXPANSION SANDBOX',
        'this.sandboxInstall();',
    ],
    'System/Battle/BattleControlPlayer.as': ['sandboxAddMana'],
    'System/Battle/PlayerSpell.as': ['sandboxMaster && BattleSystem.sandboxFreeSpells', 'sandboxUnlimitedBuildings'],
    'System/Battle/PlayerUnit.as': ['sandboxMaster && BattleSystem.sandboxPopBoost', 'sandboxMaster && BattleSystem.sandboxFastUnits'],
}
for rel, needles in checks.items():
    t = read(rel)
    for needle in needles:
        if needle not in t:
            raise SystemExit(f'validation failed: {needle!r} missing from {rel}')

print('Epic War 5 Expansion V3.4 deferred-transition + optional-sandbox patch applied')
