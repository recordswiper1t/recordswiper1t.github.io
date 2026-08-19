#!/usr/bin/env python3
from pathlib import Path
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: build-v6.py <exported-scripts-dir>")

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
# Level.as: expose every real enemy class, unlimited/instant-win controls,
# and stronger load-aware Send All pacing for memory-constrained phones.
# ---------------------------------------------------------------------------
level = read("Level.as")

enemies = [
    "EnemyDesertRaider", "EnemyDesertArcher", "EnemyDesertWolf", "EnemyDesertWolfSmall",
    "EnemyImmortal", "EnemyFallen", "EnemyScorpion", "EnemyWasp", "EnemyWaspQueen",
    "EnemyExecutioner", "EnemyTremor", "EnemyBouncer",
    "EnemyCanibal", "EnemyCanibalHunter", "EnemyCanibalHunterUnderwater",
    "EnemyCanibalShamanMagic", "EnemyCanibalShamanPriest", "EnemyCanibalShamanShield",
    "EnemyCanibalNecromancer", "EnemyCanibalBeast", "EnemyCanibalUnderwater",
    "EnemyCanibalWingRider", "EnemyCanibalZombie",
    "EnemySavageBird", "EnemyJungleSpiderSmall", "EnemyJungleSpiderBig", "EnemyJungleSpiderTiny",
    "EnemyGorilla", "EnemyGorillaBoss", "EnemyGorillaOffspring",
    "EnemyMunra", "EnemyAlienBreeder", "EnemyAlienReaper",
    "EnemyEfreeti", "EnemyEfreetiSmall",
    "EnemyFinalBoss", "EnemyFinalBossMinion", "EnemyFinalBossPiece",
    "EnemySaurianBroodguard", "EnemySaurianMyrmidon", "EnemySaurianDarter",
    "EnemySaurianNightscale", "EnemySaurianBlazefang", "EnemySaurianRazorwing",
    "EnemySaurianQuetzal", "EnemySaurianSavant", "EnemySaurianBrute",
]
if len(enemies) != 47:
    raise SystemExit(f"enemy catalog invariant failed: {len(enemies)}")
enemy_literal = "private var qolEnemies:Array = [" + ",".join(f'\"{x}\"' for x in enemies) + "];"
level, n = re.subn(r"private var qolEnemies:Array\s*=\s*\[[^;]*\];", enemy_literal, level, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f"enemy catalog: expected 1 match, found {n}")

if "private var qolUnlimitedMode:Boolean" not in level:
    level = replace_once(
        level,
        enemy_literal,
        enemy_literal + "\n      \n      private var qolUnlimitedMode:Boolean = false;",
        "unlimited state",
    )

level = replace_once(
    level,
    '            this.qolSettings.addChild(this.qolLabel("Next-wave flags now appear immediately after the previous wave is sent.",28,330,14));',
    '            this.qolSettings.addChild(this.qolButton("Unlimited: " + (this.qolUnlimitedMode ? "ON" : "OFF"),28,322,250,"unlimited"));',
    "unlimited button",
)
level = replace_once(
    level,
    '            this.qolSettings.addChild(this.qolLabel("Send-all is paced across frames to reduce Ruffle spikes.",28,354,14));',
    '            this.qolSettings.addChild(this.qolButton("INSTANT WIN",302,322,250,"instant_win"));\n'
    '            this.qolSettings.addChild(this.qolLabel("Send-all pauses new waves while the board is overloaded.",28,382,14));',
    "instant-win button",
)

action_anchor = '''         else if(action == "all_waves")
         {
            this.qolSendAllWaves();
         }
'''
action_block = '''         else if(action == "unlimited")
         {
            this.qolUnlimitedMode = !this.qolUnlimitedMode;
            this.isReadyToWin = false;
            this.readyToWinTimeCounter = 0;
         }
         else if(action == "instant_win")
         {
            this.qolInstantWin();
            return;
         }
''' + action_anchor
level = replace_once(level, action_anchor, action_block, "level tool actions")

instant_helper = '''      private function qolInstantWin() : void
      {
         this.qolUnlimitedMode = false;
         this.qolSendAllPending = false;
         this.isReadyToWin = false;
         this.readyToWinTimeCounter = 0;
         this.qolHideSettings();
         this.§_-BF§ = LEVEL_PRE_WIN;
         this.onPreWin();
         this.§try each§();
      }
      
'''
level = replace_once(
    level,
    "      private function qolSendAllWaves() : void\n",
    instant_helper + "      private function qolSendAllWaves() : void\n",
    "instant-win helper",
)

level = replace_once(
    level,
    "            else if(!this.hasEnemies())",
    "            else if(!this.qolUnlimitedMode && !this.hasEnemies())",
    "unlimited win gate",
)

count_helper = '''      private function qolEnemySpawnCount() : int
      {
         var name:String = String(this.qolEnemies[this.qolEnemyIndex]);
         if(name == "EnemyEfreeti" || name == "EnemyGorillaBoss" || name == "EnemyFinalBoss")
         {
            return 1;
         }
         if(name == "EnemyFinalBossPiece")
         {
            return Math.min(3,this.qolEnemyCount);
         }
         return this.qolEnemyCount;
      }
      
'''
level = replace_once(
    level,
    "      private function qolSendCustomRound() : void\n",
    count_helper + "      private function qolSendCustomRound() : void\n",
    "enemy count helper",
)
level = replace_once(
    level,
    '         var spawn:§_-VY§ = new §_-VY§(String(this.qolEnemies[this.qolEnemyIndex]),"",0,this.qolEnemyCount,18,0,false,0);',
    '         var spawn:§_-VY§ = new §_-VY§(String(this.qolEnemies[this.qolEnemyIndex]),"",0,this.qolEnemySpawnCount(),18,0,false,0);',
    "custom enemy count",
)

level = replace_once(
    level,
    "var heavy:Boolean = this.entities.numChildren > 180 || this.bullets.numChildren > 220;\n         var extreme:Boolean = this.entities.numChildren > 300 || this.bullets.numChildren > 380;",
    "var heavy:Boolean = this.entities.numChildren > 160 || this.bullets.numChildren > 200;\n         var extreme:Boolean = this.entities.numChildren > 260 || this.bullets.numChildren > 330;",
    "swarm thresholds",
)
level = replace_once(
    level,
    "if(!heavy || !extreme && (this.qolPerfFrame & 1) == 0 || extreme && this.qolPerfFrame % 4 == 0)",
    "if(!heavy || !extreme && (this.qolPerfFrame & 1) == 0 || extreme && this.qolPerfFrame % 6 == 0)",
    "extreme cosmetic cadence",
)

queue_anchor = '''         if(this.qolSendAllPending)
         {
            if(this.qolSendAllCooldown <= 0)
'''
queue_replacement = '''         if(this.qolSendAllPending)
         {
            if(this.entities.numChildren > 340 || this.bullets.numChildren > 420)
            {
               this.qolSendAllCooldown = Math.max(this.qolSendAllCooldown,6);
            }
            else if(this.qolSendAllCooldown <= 0)
'''
level = replace_once(level, queue_anchor, queue_replacement, "send-all backpressure")
level = replace_once(
    level,
    "               this.qolSendAllCooldown = 2;",
    "               this.qolSendAllCooldown = this.entities.numChildren > 240 || this.bullets.numChildren > 300 ? 5 : 2;",
    "adaptive send-all cooldown",
)
write("Level.as", level)


# ---------------------------------------------------------------------------
# TowerHolder.as: expose the three original-stage specials omitted by V5.
# Keep the existing pages intact and add a fourth map-special page.
# ---------------------------------------------------------------------------
holder = read("TowerHolder.as")

old_page3 = '''            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,1,"TooltipBasic",{
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
new_page3 = '''            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_dwaarp","tw_engineer",this.cRoot.gameSettings.engineers.dwaarp.cost,false,0,0,0,1,"TooltipBasic",{
               "title":"DWAARP",
               "text":"Build the DWAARP specialization directly."
            }),new Array("qol_mech","tw_engineer",this.cRoot.gameSettings.engineers.mech.cost,false,0,0,0,2,"TooltipBasic",{
               "title":"Battle-Mecha T200",
               "text":"Build the Battle-Mecha specialization directly."
            }),new Array("qol_piratecamp","tw_archer",0,false,0,0,0,3,"TooltipBasic",{
               "title":"Pirate Cpt.",
               "text":"Place the map-special pirate cannon battery."
            }),new Array("qol_specials4","tw_clean",0,false,0,0,0,4,"TooltipBasic",{
               "title":"More map specials →",
               "text":"Open the remaining original-stage special buildings."
            }),new Array("qol_specials","tw_clean",0,false,0,0,0,7,"TooltipBasic",{
               "title":"← Special towers",
               "text":"Return to the first special-tower page."
            })));'''
holder = replace_once(holder, old_page3, new_page3, "special page 3 expansion")

page4 = '''         if(param1 == "qol_specials4")
         {
            this.cRoot.quickMenu.load(this.x,this.y - 10 + this.yAdjust,this,false,0,true,new Array(new Array("qol_legion_archer","tw_archer",0,false,0,0,0,1,"TooltipBasic",{
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
            })));
            this.cRoot.quickMenu.show(this.cRoot.§else const native§);
            return;
         }
'''
holder = replace_once(
    holder,
    '         if(param1 == "qol_piratecamp")\n',
    page4 + '         if(param1 == "qol_piratecamp")\n',
    "special page 4 insertion",
)

missing_actions = '''         if(param1 == "qol_legion_archer")
         {
            this.qolPlaceSpecial(new §_-Xb§(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
         if(param1 == "qol_mercenary")
         {
            this.qolPlaceSpecial(new §return const if§(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
         if(param1 == "qol_amazona")
         {
            this.qolPlaceSpecial(new §override import§(this.x,this.y + this.yAdjust,this.§_-EV§));
            return;
         }
'''
holder = replace_once(
    holder,
    '         if(param1 == "qol_crossbow")\n',
    missing_actions + '         if(param1 == "qol_crossbow")\n',
    "missing special-building actions",
)
write("TowerHolder.as", holder)


checks = {
    "Level.as": [
        "EnemyCanibalZombie", "EnemyEfreeti", "EnemyFinalBoss", "EnemyGorillaBoss",
        "EnemyJungleSpiderTiny", "qolUnlimitedMode", "qolInstantWin",
        "numChildren > 340", "qolEnemySpawnCount",
    ],
    "TowerHolder.as": [
        "qol_legion_archer", "new §_-Xb§",
        "qol_mercenary", "new §return const if§",
        "qol_amazona", "new §override import§",
        "qol_specials4",
    ],
}
for name, needles in checks.items():
    text = read(name)
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"validation failed: {needle!r} missing from {name}")

# This file intentionally patches only Level.as and TowerHolder.as on top of V5.
print(f"V6 patches applied successfully. Enemy selector entries: {len(enemies)}")
