#!/usr/bin/env python3
from pathlib import Path
import re, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_polish_v32.py <exported-scripts-root>')
root = Path(sys.argv[1]) / 'scripts' / 'Game'


def read(rel):
    return (root / rel).read_text(encoding='utf-8-sig')

def write(rel, text):
    (root / rel).write_text(text, encoding='utf-8', newline='\n')

def one(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old, new, 1)

def replace_method(text, signature, next_signature, body, label):
    start = text.find(signature)
    if start < 0:
        raise SystemExit(f'{label}: start not found')
    end = text.find(next_signature, start + len(signature))
    if end < 0:
        raise SystemExit(f'{label}: end not found')
    return text[:start] + body + text[end:]

def replace_case(text, case_id, block, label):
    start = text.find(f'            case {case_id}:\n')
    if start < 0:
        raise SystemExit(f'{label}: case {case_id} not found')
    m = re.search(r'\n            case \d+:\n|\n            default:\n', text[start + 1:])
    if not m:
        raise SystemExit(f'{label}: end of case {case_id} not found')
    end = start + 1 + m.start() + 1
    return text[:start] + block + text[end:]

# ---------------------------------------------------------------------------
# Progression: trials accelerate progress but are no longer secretly required
# to obtain the twelfth army slot. Story + extra + 25 expansion clears = 45.
# Also centralize advanced-upgrade pricing and next-unlock thresholds.
# ---------------------------------------------------------------------------
rel = 'Manager/DataManager.as'
t = read(rel)
t = replace_method(t,
    '      public function expansionArmySlotsForClears(CLEARS:int) : int\n',
    '      public function expansionEquipmentSlotsForClears(CLEARS:int) : int\n',
'''      public function expansionArmySlotsForClears(CLEARS:int) : int
      {
         if(CLEARS >= 45) return 12;
         if(CLEARS >= 38) return 11;
         if(CLEARS >= 31) return 10;
         if(CLEARS >= 25) return 9;
         if(CLEARS >= 20) return 8;
         if(CLEARS >= 14) return 7;
         if(CLEARS >= 9) return 6;
         if(CLEARS >= 5) return 5;
         if(CLEARS >= 2) return 4;
         return 3;
      }
      
''', 'V3.2 army progression')
helpers = r'''      public function expansionUpgradeCostMultiplier(SLOT:int) : int
      {
         if(SLOT <= 9) return 15;
         var depth:int = (SLOT - 10) % 3;
         if(depth == 0) return 16;
         if(depth == 1) return 18;
         return 20;
      }
      
      public function expansionNextArmyUnlockClear() : int
      {
         var clears:int = this.expansionProgressCount();
         var marks:Array = [2,5,9,14,20,25,31,38,45];
         var i:int = 0;
         for(i = 0; i < marks.length; i++) if(clears < int(marks[i])) return int(marks[i]);
         return -1;
      }
      
      public function expansionNextEquipmentUnlockClear() : int
      {
         var clears:int = this.expansionProgressCount();
         if(clears < 15) return 15;
         if(clears < 35) return 35;
         return -1;
      }
      
'''
t = one(t, '      public function expansionArmySlotsUnlocked() : int\n', helpers + '      public function expansionArmySlotsUnlocked() : int\n', 'V3.2 progression helpers')
write(rel, t)

# ---------------------------------------------------------------------------
# Upgrade UI: advanced branch roots are approachable, middle nodes normal, and
# capstones cost more. One shared DataManager helper keeps all cost displays and
# purchase checks identical.
# ---------------------------------------------------------------------------
rel = 'Interface/WorldMapFormationSkill.as'
t = read(rel)
t = one(t,
    '         var cost:int = statABL.rank * (MATCH_NUM >= 10 ? 18 : 15);\n',
    '         var cost:int = statABL.rank * this.mGF.datMgr.expansionUpgradeCostMultiplier(MATCH_NUM);\n',
    'V3.2 displayed skill cost')
t = one(t,
    '            var costExp:int = stat.rank * (this.selectSlotNum >= 10 ? 18 : 15);\n',
    '            var costExp:int = stat.rank * this.mGF.datMgr.expansionUpgradeCostMultiplier(this.selectSlotNum);\n',
    'V3.2 purchased skill cost')
t = t.replace('else this.skillPageText.text = "< Original  •  Advanced upgrades";',
              'else this.skillPageText.text = "< Original  •  Advanced 10-18";')
write(rel, t)

# Formation upgrade badge must use the exact same pricing rules. Page two is no
# longer a dead screen before slot seven exists, and the label shows next unlock.
rel = 'Interface/WorldMapFormation.as'
t = read(rel)
t = one(t,
    '                  cost = abilityStat.rank * (slot >= 10 ? 18 : 15);\n',
    '                  cost = abilityStat.rank * this.mGF.datMgr.expansionUpgradeCostMultiplier(slot);\n',
    'V3.2 formation upgrade cost')
t = replace_method(t,
    '      private function expansionArmyPageClick(event:MouseEvent) : void\n',
    '      private function expansionUpdateArmyPageLabel() : void\n',
'''      private function expansionArmyPageClick(event:MouseEvent) : void
      {
         var unlocked:int = this.mGF.datMgr.expansionArmySlotsUnlocked();
         if(this.equipPage == 1 && unlocked < 7)
         {
            this.mGF.utilMgr.messagePop("army slots 7-12 unlock later in the campaign");
            return;
         }
         this.equipPage = this.equipPage == 1 ? 2 : 1;
         this.selectEquipNum = 0;
         this.selectEquipID = 0;
         this.updateView();
      }
      
''', 'V3.2 army page click')
t = replace_method(t,
    '      private function expansionUpdateArmyPageLabel() : void\n',
    '      private function selectEQUIP(CLIP:*, NUM:int = 0) : *\n',
'''      private function expansionUpdateArmyPageLabel() : void
      {
         if(this.armyPageText == null) return;
         var lo:int = this.equipPage == 1 ? 1 : 7;
         var hi:int = this.equipPage == 1 ? 6 : 12;
         var unlocked:int = this.mGF.datMgr.expansionArmySlotsUnlocked();
         var next:int = this.mGF.datMgr.expansionNextArmyUnlockClear();
         this.armyPageText.text = "A" + lo + "-" + hi + " • " + unlocked + "/12" + (next > 0 ? " • next " + next : " • MAX");
      }
      
''', 'V3.2 army page label')
write(rel, t)

# ---------------------------------------------------------------------------
# Advanced trees: keep the exact same nine advanced slots and existing ability
# catalog, but remove repeated filler nodes. Duplicate entries are replaced by
# broadly useful existing passives appropriate to hero/unit/special tiers.
# ---------------------------------------------------------------------------
rel = 'System/StatDef/CharTotalStat.as'
t = read(rel)
start = t.find('      private function expansionAdvancedTree() : Array\n')
end = t.find('      private function expansionAdvancedAbility(SLOT:int) : int\n', start)
if start < 0 or end < 0:
    raise SystemExit('V3.2 advanced tree region not found')
region = t[start:end]
region2, count = re.subn(r'return \[([^\]]+)\];', r'return this.expansionPolishTree([\1]);', region)
if count < 20:
    raise SystemExit(f'V3.2 advanced tree wraps too few returns: {count}')
polish_helper = r'''      private function expansionPolishTree(RAW:Array) : Array
      {
         var fallback:Array = null;
         if(this.id >= 1 && this.id <= 3)
            fallback = [35,36,37,39,40,41,42,29,26,27,28,30,31,32,33,34,38];
         else if(this.id >= 50)
            fallback = [35,36,37,39,40,41,42,38,29,26,27,28,30,31,32,33,34];
         else
            fallback = [35,36,37,39,46,47,48,25,20,15,42,26,27,28,29,30,31,32,33,34];
         var out:Array = [];
         var i:int = 0;
         var j:int = 0;
         var id:int = 0;
         var candidate:int = 0;
         while(i < RAW.length)
         {
            id = int(RAW[i]);
            if(out.indexOf(id) < 0)
               out.push(id);
            else
            {
               j = 0;
               while(j < fallback.length)
               {
                  candidate = int(fallback[j]);
                  if(out.indexOf(candidate) < 0)
                  {
                     out.push(candidate);
                     break;
                  }
                  j++;
               }
            }
            i++;
         }
         return out;
      }
      
'''
t = t[:start] + region2 + polish_helper + t[end:]
write(rel, t)

# ---------------------------------------------------------------------------
# Gear: preserve all 55 items, but rebalance the most dominant late-game pieces
# so three equipment slots create choices rather than one obvious loadout.
# ---------------------------------------------------------------------------
rel = 'System/StatDef/CharAbilityStat.as'
t = read(rel)
gear_cases = {
82: '''            case 82:\n               this.name_id = "x_bastion"; this.name_str = "Bastion"; this.desc = "Health +35%, defense +12%"; this.health_boost = 0.35; this.defense_mult = 0.12; this.rank = 55; break;\n''',
83: '''            case 83:\n               this.name_id = "x_windstep"; this.name_str = "Windstep"; this.desc = "Speed +1.0, damage +10%"; this.speed = 1.0; this.damage_mult = 0.10; this.rank = 52; break;\n''',
85: '''            case 85:\n               this.name_id = "x_titanbelt"; this.name_str = "Titan Belt"; this.desc = "Population +2, health +15%"; this.pop = 2; this.health_boost = 0.15; this.rank = 60; break;\n''',
90: '''            case 90:\n               this.name_id = "x_phoenixcore"; this.name_str = "Phoenix Core"; this.desc = "Regen +200, health +15%"; this.health_regen = 200; this.health_boost = 0.15; this.rank = 68; break;\n''',
97: '''            case 97:\n               this.name_id = "x_warlord"; this.name_str = "Warlord Crest"; this.desc = "Damage +18%, defense +12%, population +1"; this.damage_mult = 0.18; this.defense_mult = 0.12; this.pop = 1; this.rank = 78; break;\n''',
98: '''            case 98:\n               this.name_id = "x_colossus"; this.name_str = "Colossus Heart"; this.desc = "Health +45%, speed -0.45"; this.health_boost = 0.45; this.speed = -0.45; this.rank = 80; break;\n''',
100: '''            case 100:\n               this.name_id = "x_paladin"; this.name_str = "Paladin Reliquary"; this.desc = "Health +25%, defense +15%, regen +50"; this.health_boost = 0.25; this.defense_mult = 0.15; this.health_regen = 50; this.rank = 84; break;\n''',
102: '''            case 102:\n               this.name_id = "x_beasttotem"; this.name_str = "Beast Totem"; this.desc = "Population +2, damage +15%"; this.pop = 2; this.damage_mult = 0.15; this.rank = 88; break;\n''',
103: '''            case 103:\n               this.name_id = "x_guardianhalo"; this.name_str = "Guardian Halo"; this.desc = "All resistance, health +10%, damage -15%"; this.resist_strike = 1; this.resist_slash = 1; this.resist_pierce = 1; this.resist_magic = 1; this.health_boost = 0.10; this.damage_mult = -0.15; this.rank = 92; break;\n''',
104: '''            case 104:\n               this.name_id = "x_berserkercrown"; this.name_str = "Berserker Crown"; this.desc = "Damage +50%, health -25%"; this.damage_mult = 0.50; this.health_boost = -0.25; this.rank = 96; break;\n''',
105: '''            case 105:\n               this.name_id = "x_artlogicprime"; this.name_str = "Artlogic Prime"; this.desc = "Damage +25%, health +25%, defense +15%, regen +75"; this.damage_mult = 0.25; this.health_boost = 0.25; this.defense_mult = 0.15; this.health_regen = 75; this.rank = 110; break;\n'''
}
for cid, block in gear_cases.items():
    t = replace_case(t, cid, block, 'V3.2 gear balance')
write(rel, t)

rel = 'System/StatDef/CharItemStat.as'
t = read(rel)
desc_updates = {
'Health +40%, defense +15%':'Health +35%, defense +12%',
'Speed +1.5, damage +10%':'Speed +1.0, damage +10%',
'Population +3, health +20%':'Population +2, health +15%',
'Regen +250, health +20%':'Regen +200, health +15%',
'Damage +20%, defense +15%, population +1':'Damage +18%, defense +12%, population +1',
'Health +50%, speed -0.3':'Health +45%, speed -0.45',
'Health +30%, defense +20%, regen +50':'Health +25%, defense +15%, regen +50',
'Population +2, damage +20%':'Population +2, damage +15%',
'All resistance, health +15%':'All resistance, health +10%, damage -15%',
'Damage +60%, health -15%':'Damage +50%, health -25%',
'Damage +35%, health +35%, defense +20%, regen +100':'Damage +25%, health +25%, defense +15%, regen +75'
}
for old, new in desc_updates.items():
    if t.count(old) != 1:
        raise SystemExit(f'V3.2 item description expected once: {old!r}, got {t.count(old)}')
    t = t.replace(old, new, 1)
write(rel, t)

# Do not allow the exact same item to occupy two gear slots on one character.
rel = 'Interface/WorldMapFormationAcc.as'
t = read(rel)
helper = r'''      private function expansionItemEquippedInOtherSlot(ITEM_ID:int) : Boolean
      {
         if(ITEM_ID <= 0) return false;
         var field:String = this.expansionEquipField();
         if(field != "item" && this.mGF.datMgr.unitGetValue(this.unitID,"item") == ITEM_ID) return true;
         if(field != "item2" && this.mGF.datMgr.unitGetValue(this.unitID,"item2") == ITEM_ID) return true;
         if(field != "item3" && this.mGF.datMgr.unitGetValue(this.unitID,"item3") == ITEM_ID) return true;
         return false;
      }
      
'''
t = one(t, '      private function selectEQUIP(CLIP:*) : *\n', helper + '      private function selectEQUIP(CLIP:*) : *\n', 'V3.2 duplicate gear helper')
t = one(t,
'''         if(this.selectSlotNum > 0)
         {
            itemTotal = 0;
''',
'''         if(this.selectSlotNum > 0)
         {
            if(this.expansionItemEquippedInOtherSlot(this.selectSlotID))
            {
               this.mGF.utilMgr.messagePop("that item is already equipped in another gear slot");
               return;
            }
            itemTotal = 0;
''', 'V3.2 duplicate gear guard')
write(rel, t)

# ---------------------------------------------------------------------------
# Expansion encounters: smooth raw-stat spikes while preserving high endgame
# pressure through multiple portals/bosses. Gear rewards are first-clear only;
# repeats remain useful by granting extra XP instead of infinite item farming.
# ---------------------------------------------------------------------------
rel = 'System/Battle/BattleControlEnemy.as'
t = read(rel)
t = one(t, '         var tier:int = index + 1;\n', '         var tier:int = index + 1;\n         var firstClear:Boolean = this.mGF.datMgr.stageGetValue("expansion",tier) < 1;\n', 'V3.2 first clear marker')
repls = {
'         var bossHP:int = 120000 + tier * 30000 + tier * tier * 900;\n':'         var bossHP:int = 135000 + tier * 26000 + tier * tier * 720;\n',
'         var bossATK:int = 950 + tier * 245;\n':'         var bossATK:int = 950 + tier * 205;\n',
'         var eliteHP:int = 18000 + tier * 6200;\n':'         var eliteHP:int = 18000 + tier * 5200;\n',
'         var eliteATK:int = 320 + tier * 115;\n':'         var eliteATK:int = 320 + tier * 95;\n',
'         var portalHP:int = 22000 + tier * 8000;\n':'         var portalHP:int = 22000 + tier * 6500;\n',
'         if(tier >= 8)\n':'         if(tier >= 9)\n',
'         if(tier >= 16)\n':'         if(tier >= 17)\n',
'            this.bSys.charMgr.createEnemyUnit("boss",String(bosses[(index + 7) % bosses.length]),length - 1100,0,50,int(bossHP * 0.48),int(bossATK * 0.72),String(elements[(index + 2) % elements.length]),0.85 + tier * 0.006);\n':'            this.bSys.charMgr.createEnemyUnit("boss",String(bosses[(index + 7) % bosses.length]),length - 1100,0,50,int(bossHP * 0.42),int(bossATK * 0.66),String(elements[(index + 2) % elements.length]),0.85 + tier * 0.006);\n',
'         this.bSys.battle_exp_reward = 120 + tier * 14;\n':'         this.bSys.battle_exp_reward = 135 + tier * 15 + (firstClear ? 0 : 40 + tier * 3);\n',
'         this.bSys.battle_item_reward = String(rewardNames[index]);\n':'         this.bSys.battle_item_reward = firstClear ? String(rewardNames[index]) : "";\n',
'         if(tier >= 20)\n':'         if(tier >= 21)\n'
}
for old,new in repls.items():
    if t.count(old) != 1:
        raise SystemExit(f'V3.2 encounter anchor expected once, got {t.count(old)}: {old.strip()}')
    t = t.replace(old,new,1)
write(rel, t)

# Expansion first-clear gear grants exactly one copy; preserve vanilla two-copy
# item behavior for the original game. Repeat expansion clears now have no item.
rel = 'Interface/BattleResult.as'
t = read(rel)
old = '''         if(itemReward > 0)
         {
            if(this.mGF.datMgr.itemGetValue(itemReward) <= 0)
            {
               this.mGF.datMgr.itemSetValue(itemReward,1);
            }
            this.mGF.datMgr.itemSetValue(itemReward,this.mGF.datMgr.itemGetValue(itemReward) + 1);
         }
'''
new = '''         if(itemReward > 0)
         {
            if(this.bSys.battle_stage >= 26 && this.bSys.battle_stage <= 50)
               this.mGF.datMgr.itemSetValue(itemReward,Math.min(this.mGF.datMgr.itemGetValue(itemReward) + 1,99));
            else
            {
               if(this.mGF.datMgr.itemGetValue(itemReward) <= 0) this.mGF.datMgr.itemSetValue(itemReward,1);
               this.mGF.datMgr.itemSetValue(itemReward,this.mGF.datMgr.itemGetValue(itemReward) + 1);
            }
         }
'''
t = one(t, old, new, 'V3.2 expansion reward quantity')
write(rel, t)

# ---------------------------------------------------------------------------
# World map: add compact threat bands to the same 25 stages. No content is
# added; this simply tells the player when the encounter tier steps up.
# ---------------------------------------------------------------------------
rel = 'Interface/WorldMap.as'
t = read(rel)
t = one(t,
'         var i:int = 0; var b:Sprite = null; var tx:TextField = null; var unlocked:Boolean = false;\n',
'         var i:int = 0; var b:Sprite = null; var tx:TextField = null; var unlocked:Boolean = false; var threat:int = 1;\n',
'V3.2 threat variable')
old = '            tx.text = String(25 + i) + ". " + String(stageNames[i - 1]) + (this.mGF.datMgr.stageGetValue("expansion",i) >= 1 ? "\\nCLEARED" : (unlocked ? "\\nREADY" : "\\nLOCKED"));\n'
new = '            threat = Math.min(5,1 + int((i - 1) / 5));\n            tx.text = String(25 + i) + ". " + String(stageNames[i - 1]) + "\\nT" + threat + " • " + (this.mGF.datMgr.stageGetValue("expansion",i) >= 1 ? "CLEARED" : (unlocked ? "READY" : "LOCKED"));\n'
t = one(t, old, new, 'V3.2 threat labels')
write(rel, t)

# Self-checks before FFDec import.
checks = {
'Manager/DataManager.as':['if(CLEARS >= 45) return 12;','expansionUpgradeCostMultiplier','expansionNextArmyUnlockClear'],
'Interface/WorldMapFormationSkill.as':['expansionUpgradeCostMultiplier(MATCH_NUM)','Advanced 10-18'],
'Interface/WorldMapFormation.as':['next " + next','expansionUpgradeCostMultiplier(slot)'],
'System/StatDef/CharTotalStat.as':['expansionPolishTree','return this.expansionPolishTree([20,15,47'],
'Interface/WorldMapFormationAcc.as':['expansionItemEquippedInOtherSlot','already equipped in another gear slot'],
'System/Battle/BattleControlEnemy.as':['firstClear:Boolean','firstClear ? String(rewardNames[index]) : ""','tier >= 21'],
'Interface/BattleResult.as':['battle_stage >= 26 && this.bSys.battle_stage <= 50','Math.min(this.mGF.datMgr.itemGetValue(itemReward) + 1,99)'],
'Interface/WorldMap.as':['"\\nT" + threat','var threat:int = 1']
}
for rel, needles in checks.items():
    z=read(rel)
    for needle in needles:
        if needle not in z:
            raise SystemExit(f'V3.2 validation failed: {rel} missing {needle}')

print('Epic War 5 Expansion V3.2 quality pass applied')
