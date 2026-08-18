#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: build-v5.py <exported-scripts-dir>")

scripts = Path(sys.argv[1])


def read(name: str) -> str:
    p = scripts / name
    if not p.exists():
        raise SystemExit(f"missing exported script: {p}")
    return p.read_text(encoding="utf-8-sig")


def write(name: str, text: str) -> None:
    (scripts / name).write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected 1 exact match, found {count}")
    return text.replace(old, new, 1)


# ---------------------------------------------------------------------------
# Level.as: complete safe enemy selector, lower cosmetic cost under swarm load,
# preserve per-wave hooks during Send All, and trigger native boss entrances.
# ---------------------------------------------------------------------------
level = read("Level.as")

enemies = [
    "EnemyDesertRaider", "EnemyDesertArcher", "EnemyDesertWolf", "EnemyDesertWolfSmall",
    "EnemyImmortal", "EnemyFallen", "EnemyScorpion", "EnemyWasp", "EnemyWaspQueen",
    "EnemyExecutioner", "EnemyTremor", "EnemyBouncer",
    "EnemyCanibal", "EnemyCanibalHunter", "EnemyCanibalHunterUnderwater",
    "EnemyCanibalShamanMagic", "EnemyCanibalShamanPriest", "EnemyCanibalShamanShield",
    "EnemyCanibalNecromancer", "EnemyCanibalBeast", "EnemyCanibalUnderwater",
    "EnemyCanibalWingRider", "EnemySavageBird", "EnemyJungleSpiderSmall", "EnemyJungleSpiderBig",
    "EnemyGorilla", "EnemyMunra", "EnemyAlienBreeder", "EnemyAlienReaper",
    "EnemySaurianBroodguard", "EnemySaurianMyrmidon", "EnemySaurianDarter",
    "EnemySaurianNightscale", "EnemySaurianBlazefang", "EnemySaurianRazorwing",
    "EnemySaurianQuetzal", "EnemySaurianSavant", "EnemySaurianBrute",
]
enemy_literal = "private var qolEnemies:Array = [" + ",".join(f'\"{x}\"' for x in enemies) + "];"
level, n = re.subn(r"private var qolEnemies:Array\s*=\s*\[[^;]*\];", enemy_literal, level, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f"enemy catalog: expected 1 match, found {n}")

level = replace_once(
    level,
    "var heavy:Boolean = this.entities.numChildren > 280 || this.bullets.numChildren > 320;",
    "var heavy:Boolean = this.entities.numChildren > 180 || this.bullets.numChildren > 220;\n         var extreme:Boolean = this.entities.numChildren > 300 || this.bullets.numChildren > 380;",
    "performance thresholds",
)
level = replace_once(
    level,
    "if(!heavy || (this.qolPerfFrame & 1) == 0)",
    "if(!heavy || !extreme && (this.qolPerfFrame & 1) == 0 || extreme && this.qolPerfFrame % 4 == 0)",
    "cosmetic throttling",
)

boss_helper = '''      private function qolForceBossIfNeeded() : void
      {
         if(this.mode != §_-Mm§.MODE_CAMPAIGN)
         {
            return;
         }
         if(this is Level6)
         {
            Level6(this).qolForceBossFromSendAll();
         }
         else if(this is Level11)
         {
            Level11(this).qolForceBossFromSendAll();
         }
         else if(this is Level15)
         {
            Level15(this).qolForceBossFromSendAll();
         }
      }
      
'''
level = replace_once(
    level,
    "      private function qolSendAllWaves() : void\n",
    boss_helper + "      private function qolSendAllWaves() : void\n",
    "boss helper insertion",
)

m = re.search(r"      private function qolSendQueuedWave\(\) : void\n      \{.*?\n      \}", level, re.S)
if not m:
    raise SystemExit("send-all queue function not found")
block = m.group(0)
if block.count("this.qolSendAllPending = false;") != 2:
    raise SystemExit("send-all queue completion anchors changed")
block = block.replace(
    "this.qolSendAllPending = false;\n            this.menu.§return var§();",
    "this.qolSendAllPending = false;\n            this.qolForceBossIfNeeded();\n            this.menu.§return var§();",
)
block = replace_once(
    block,
    "this.§_-rd§.updateWaves(this.§_-g3§,this.maxWaves);",
    "this.§_-rd§.updateWaves(this.§_-g3§,this.maxWaves);\n         this.§else use§();",
    "send-all per-wave hook",
)
level = level[:m.start()] + block + level[m.end():]
write("Level.as", level)


# ---------------------------------------------------------------------------
# Boss stages: expose guarded wrappers around the stages' own entrance logic.
# This keeps each boss' animation/controller path intact instead of constructing
# boss objects through the generic enemy-wave factory.
# ---------------------------------------------------------------------------
level6 = read("Level6.as")
level6_helper = '''      public function qolForceBossFromSendAll() : void
      {
         if(this.mode == §_-Mm§.MODE_CAMPAIGN && !this.§catch const default§)
         {
            this.efreetiDoor.spawnBoss();
            this.game.gameSounds.playBossEfreetiSummon();
            this.§catch const default§ = true;
         }
      }
      
'''
level6 = replace_once(level6, "      override protected function hasEnemies() : Boolean\n", level6_helper + "      override protected function hasEnemies() : Boolean\n", "Level6 boss helper")
write("Level6.as", level6)

level11 = read("Level11.as")
level11_helper = '''      public function qolForceBossFromSendAll() : void
      {
         if(this.mode == §_-Mm§.MODE_CAMPAIGN && !this.gorillaIsOut && !this.§_-Vl§.isGoingUp)
         {
            this.§_-Vl§.goUp();
         }
      }
      
'''
level11 = replace_once(level11, "      override protected function hasEnemies() : Boolean\n", level11_helper + "      override protected function hasEnemies() : Boolean\n", "Level11 boss helper")
write("Level11.as", level11)

level15 = read("Level15.as")
level15_helper = '''      public function qolForceBossFromSendAll() : void
      {
         if(this.mode == §_-Mm§.MODE_CAMPAIGN && !this.§_-So§ && !this.§try set§.§_-yJ§)
         {
            this.§try set§.§_-ET§();
         }
      }
      
'''
level15 = replace_once(level15, "      override protected function hasEnemies() : Boolean\n", level15_helper + "      override protected function hasEnemies() : Boolean\n", "Level15 boss helper")
write("Level15.as", level15)


# ---------------------------------------------------------------------------
# TowerHolder.as: expose the one additional SPECIAL_* tower implementation in
# this SWF (Pirate Camp) on the third sandbox special-building page.
# ---------------------------------------------------------------------------
holder = read("TowerHolder.as")
old_page3 = '''            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"DWAARP",
               "text":"Build the DWAARP specialization directly."
            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Battle-Mecha T200",
               "text":"Build the Battle-Mecha specialization directly."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← Special towers",
               "text":"Return to the first special-tower page."
            })));'''
new_page3 = '''            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"DWAARP",
               "text":"Build the DWAARP specialization directly."
            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Battle-Mecha T200",
               "text":"Build the Battle-Mecha specialization directly."
            }),new Array("qol_piratecamp","tw_archer",0,false,0,0,0,3,"TooltipBasic",{
               "title":"Pirate Camp",
               "text":"Place the map-special Pirate Camp. Its own upgrades keep their normal costs."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← Special towers",
               "text":"Return to the first special-tower page."
            })));'''
holder = replace_once(holder, old_page3, new_page3, "special page 3")

pirate_action = '''         if(param1 == "qol_piratecamp")
         {
            this.qolPlaceSpecial(new §_-MR§(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
'''
holder = replace_once(holder, '         if(param1 == "qol_crossbow")\n', pirate_action + '         if(param1 == "qol_crossbow")\n', "Pirate Camp action")
write("TowerHolder.as", holder)


# Strong local validation before FFDec recompiles anything.
checks = {
    "Level.as": ["EnemyAlienBreeder", "EnemyWaspQueen", "qolForceBossIfNeeded", "numChildren > 180", "this.§else use§();"],
    "Level6.as": ["qolForceBossFromSendAll", "efreetiDoor.spawnBoss()"],
    "Level11.as": ["qolForceBossFromSendAll", "this.§_-Vl§.goUp()"],
    "Level15.as": ["qolForceBossFromSendAll", "this.§try set§.§_-ET§()"],
    "TowerHolder.as": ["qol_piratecamp", "new §_-MR§"],
}
for name, needles in checks.items():
    text = read(name)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"validation failed: {needle!r} missing from {name}")

print(f"V5 patches applied successfully. Enemy selector entries: {len(enemies)}")
