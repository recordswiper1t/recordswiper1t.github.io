#!/usr/bin/env python3
from pathlib import Path
import re, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_polish_v31.py <exported-scripts-root>')
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

# Safer migration and a less grindy campaign flow.
rel = 'Manager/DataManager.as'
t = read(rel)
t = replace_method(t,
    '      public function expansionOriginalCampaignComplete() : Boolean\n',
    '      public function expansionArmySlotsUnlocked() : int\n',
'''      public function expansionOriginalCampaignComplete() : Boolean
      {
         return this.getStageNormalClear() >= 12 && this.getStageExtraClear() >= 8;
      }
      
      public function expansionArmySlotsForClears(CLEARS:int) : int
      {
         if(CLEARS >= 48) return 12;
         if(CLEARS >= 41) return 11;
         if(CLEARS >= 34) return 10;
         if(CLEARS >= 27) return 9;
         if(CLEARS >= 20) return 8;
         if(CLEARS >= 14) return 7;
         if(CLEARS >= 9) return 6;
         if(CLEARS >= 5) return 5;
         if(CLEARS >= 2) return 4;
         return 3;
      }
      
      public function expansionEquipmentSlotsForClears(CLEARS:int) : int
      {
         if(CLEARS >= 35) return 3;
         if(CLEARS >= 15) return 2;
         return 1;
      }
      
''', 'progression helpers')
t = replace_method(t,
    '      public function expansionArmySlotsUnlocked() : int\n',
    '      public function expansionEquipmentSlotsUnlocked() : int\n',
'''      public function expansionArmySlotsUnlocked() : int
      {
         return this.expansionArmySlotsForClears(this.expansionProgressCount());
      }
      
''', 'army slots wrapper')
t = replace_method(t,
    '      public function expansionEquipmentSlotsUnlocked() : int\n',
    '      public function expansionAdvancedUpgradesUnlocked() : Boolean\n',
'''      public function expansionEquipmentSlotsUnlocked() : int
      {
         return this.expansionEquipmentSlotsForClears(this.expansionProgressCount());
      }
      
''', 'equipment slots wrapper')
anchor = '''      private function expansionEnsureData() : void
      {
         while(this.dat_item_inv.length < 55)
         {
            this.dat_item_inv.push(0);
         }
'''
replacement = '''      private function expansionEnsureData() : void
      {
         while(this.dat_item_inv.length < 55)
         {
            this.dat_item_inv.push(0);
         }
         while(this.dat_stage_expansion_stat.length < 25)
         {
            this.dat_stage_expansion_stat.push(0);
         }
         if(this.dat_stage_expansion_stat.length > 25)
         {
            this.dat_stage_expansion_stat.length = 25;
         }
         this.stage_expansion_stat = this.mergeArrayString(this.dat_stage_expansion_stat);
'''
t = one(t, anchor, replacement, 'expansion save-bank migration')
write(rel, t)

# Advanced upgrades remain meaningful without becoming grind-only.
rel = 'Interface/WorldMapFormationSkill.as'
t = read(rel)
if t.count('MATCH_NUM >= 10 ? 45 : 15') != 1 or t.count('this.selectSlotNum >= 10 ? 45 : 15') != 1:
    raise SystemExit('advanced upgrade cost anchors changed')
t = t.replace('MATCH_NUM >= 10 ? 45 : 15', 'MATCH_NUM >= 10 ? 18 : 15', 1)
t = t.replace('this.selectSlotNum >= 10 ? 45 : 15', 'this.selectSlotNum >= 10 ? 18 : 15', 1)
t = t.replace('Advanced locked: 18 clears', 'Advanced locked: 18 unique clears')
write(rel, t)

# Formation indicators understand all three gear slots and all 18 upgrades.
rel = 'Interface/WorldMapFormation.as'
t = read(rel)
needle = 'if(this.mGF.datMgr.unitGetValue(ID,"item") > 0)'
if t.count(needle) != 2:
    raise SystemExit(f'formation equipment marker expected twice, got {t.count(needle)}')
t = t.replace(needle, 'if(this.expansionHasAnyEquipment(ID))')
new_methods = r'''      private function expansionHasAnyEquipment(UNIT_ID:int) : Boolean
      {
         if(UNIT_ID <= 0) return false;
         return this.mGF.datMgr.unitGetValue(UNIT_ID,"item") > 0 || this.mGF.datMgr.unitGetValue(UNIT_ID,"item2") > 0 || this.mGF.datMgr.unitGetValue(UNIT_ID,"item3") > 0;
      }
      
      private function expansionSkillParentReady(UNIT_ID:int, SLOT:int) : Boolean
      {
         if(SLOT == 1 || SLOT == 4 || SLOT == 7) return true;
         if(SLOT == 10) return this.mGF.datMgr.unitGetValue(UNIT_ID,"ability3") > 0;
         if(SLOT == 13) return this.mGF.datMgr.unitGetValue(UNIT_ID,"ability6") > 0;
         if(SLOT == 16) return this.mGF.datMgr.unitGetValue(UNIT_ID,"ability9") > 0;
         return this.mGF.datMgr.unitGetValue(UNIT_ID,"ability" + (SLOT - 1)) > 0;
      }
      
      private function testSurplusExp(UNIT_ID:int = 0) : Boolean
      {
         if(UNIT_ID <= 0) return false;
         var unitExp:int = int(this.mGF.datMgr.unitGetValue(UNIT_ID,"exp"));
         var statCHR:* = new CharTotalStat(UNIT_ID);
         statCHR.unlockAbility();
         var maxSlot:int = this.mGF.datMgr.expansionAdvancedUpgradesUnlocked() ? 18 : 9;
         var slot:int = 1;
         var abilityID:int = 0;
         var abilityStat:* = null;
         var cost:int = 0;
         while(slot <= maxSlot)
         {
            if(this.mGF.datMgr.unitGetValue(UNIT_ID,"ability" + slot) <= 0 && this.expansionSkillParentReady(UNIT_ID,slot))
            {
               abilityID = int(statCHR["unit_ability" + slot + "_id"]);
               if(abilityID > 0)
               {
                  abilityStat = new CharAbilityStat(abilityID);
                  cost = abilityStat.rank * (slot >= 10 ? 18 : 15);
                  if(unitExp >= cost) return true;
               }
            }
            slot++;
         }
         return false;
      }
      
'''
t = replace_method(t,
    '      private function testSurplusExp(UNIT_ID:int = 0) : Boolean\n',
    '      private function expansionInstallArmyPageButton() : void\n',
    new_methods, 'formation 18-upgrade badge')
write(rel, t)

# Prevent late-game stacking from producing invulnerability/runaway unit counts.
rel = 'System/StatDef/CharTotalStat.as'
t = read(rel)
dup = ''.join(f'         ability{i} = new CharAbilityStat(this.unit_ability{i}_id);\n' for i in range(10,19))
if t.count(dup) != 1:
    raise SystemExit(f'advanced ability duplicate block expected once, got {t.count(dup)}')
t = t.replace(dup, '', 1)
m = re.search(r'(^\s*this\.pop = .*?;\n)', t, re.M)
if not m: raise SystemExit('population sum not found')
t = t[:m.end()] + '         this.pop = Math.min(Math.max(this.pop,1),16);\n' + t[m.end():]
m = re.search(r'(^\s*this\.reduce_damage = ability1\.defense_mult .*?;\n)', t, re.M)
if not m: raise SystemExit('damage reduction sum not found')
t = t[:m.end()] + '         this.reduce_damage = Math.min(Math.max(this.reduce_damage,0),0.8);\n' + t[m.end():]
write(rel, t)

# Battle results explain progression unlocks and immediately flush save changes.
rel = 'Interface/BattleResult.as'
t = read(rel)
t = one(t, '         var unitReward:int = 0;\n', '         var unitReward:int = 0;\n         var expansionProgressBefore:int = this.mGF.datMgr.expansionProgressCount();\n', 'battle progress baseline')
insert = '''            this.mGF.datMgr.stat_total_battle += 1;
            var expansionProgressAfter:int = this.mGF.datMgr.expansionProgressCount();
            if(expansionProgressAfter > expansionProgressBefore)
            {
               var unlockMessage:String = "";
               var armyBefore:int = this.mGF.datMgr.expansionArmySlotsForClears(expansionProgressBefore);
               var armyAfter:int = this.mGF.datMgr.expansionArmySlotsForClears(expansionProgressAfter);
               var equipBefore:int = this.mGF.datMgr.expansionEquipmentSlotsForClears(expansionProgressBefore);
               var equipAfter:int = this.mGF.datMgr.expansionEquipmentSlotsForClears(expansionProgressAfter);
               if(armyAfter > armyBefore) unlockMessage += "Army slot " + armyAfter + " unlocked! ";
               if(equipAfter > equipBefore) unlockMessage += "Equipment slot " + equipAfter + " unlocked! ";
               if(expansionProgressBefore < 18 && expansionProgressAfter >= 18) unlockMessage += "Advanced upgrades unlocked! ";
               if(expansionProgressBefore < 20 && expansionProgressAfter >= 20 && this.mGF.datMgr.expansionOriginalCampaignComplete()) unlockMessage += "Expansion campaign unlocked!";
               if(unlockMessage != "") this.mGF.utilMgr.messagePop(unlockMessage);
            }
'''
t = one(t, '            this.mGF.datMgr.stat_total_battle += 1;\n', insert, 'unlock feedback')
t = one(t, '         this.mGF.datMgr.total_kill += this.bSys.battle_enemy_kill;\n         this.mGF.isPaused = true;\n',
'''         this.mGF.datMgr.total_kill += this.bSys.battle_enemy_kill;
         this.mGF.datMgr.saveData();
         this.mGF.isPaused = true;
''', 'result autosave')
write(rel, t)

# World-map progression is clearer; trials stay as parallel challenges.
rel = 'Interface/WorldMap.as'
t = read(rel)
t = t.replace('Clear all 25 original battles to unlock the Expansion campaign.', 'Clear all 12 story and 8 extra battles to unlock the Expansion campaign.')
t = t.replace('label.text = "EXPANSION  " + cleared + "/25";', 'label.text = "EXP " + cleared + "/25  •  A" + this.mGF.datMgr.expansionArmySlotsUnlocked() + "/12";')
t = t.replace('this.expansionPanel.graphics.drawRoundRect(0,0,650,430,14,14);', 'this.expansionPanel.graphics.drawRoundRect(0,0,650,445,14,14);')
subtitle_anchor = '         this.expansionPanel.addChild(title);\n         var stageNames:Array = '
if subtitle_anchor not in t: raise SystemExit('expansion panel subtitle anchor missing')
subtitle = '''         this.expansionPanel.addChild(title);
         var progressText:TextField = new TextField();
         progressText.defaultTextFormat = new TextFormat("_sans",11,13421772,false,null,null,null,null,"center");
         progressText.width = 620; progressText.height = 18; progressText.x = 15; progressText.y = 35; progressText.mouseEnabled = false; progressText.selectable = false;
         progressText.text = "Progress " + this.mGF.datMgr.expansionProgressCount() + "/50  •  Army " + this.mGF.datMgr.expansionArmySlotsUnlocked() + "/12  •  Equipment " + this.mGF.datMgr.expansionEquipmentSlotsUnlocked() + "/3";
         this.expansionPanel.addChild(progressText);
         var stageNames:Array = '''
t = t.replace(subtitle_anchor, subtitle, 1)
t = t.replace('close.x = 270;\n         close.y = 394;', 'close.x = 270;\n         close.y = 407;')
write(rel, t)

# Equipment screen makes the currently edited slot explicit.
rel = 'Interface/WorldMapFormationAcc.as'
t = read(rel)
t = t.replace('this.equipSlotText.text = "Equipment slot " + this.equipSlotPage + " / " + unlocked;', 'this.equipSlotText.text = "Gear slot " + this.equipSlotPage + "/" + unlocked + "  •  click to switch";')
t = t.replace('this.unit_info.htmlText = mItem.name_str + "\\n" + mItem.desc;', 'this.unit_info.htmlText = "Slot " + this.equipSlotPage + ": " + mItem.name_str + "\\n" + mItem.desc;')
write(rel, t)

# Performance: cache expensive unit-list scans for three frames.
rel = 'System/Battle/PlayerUnit.as'
t = read(rel)
t = one(t, '      private var _timer_spawn:int = 0;\n', '      private var _timer_spawn:int = 0;\n      \n      private var _count_refresh:int = 0;\n', 'PlayerUnit count field')
if '            this._timer_spawn = this.spawn_delay;\n' not in t: raise SystemExit('PlayerUnit count init missing')
t = t.replace('            this._timer_spawn = this.spawn_delay;\n', '            this._timer_spawn = this.spawn_delay;\n            this._count_refresh = this.group % 3;\n', 1)
t = one(t, '''               this.pop_total = this.getTotalSpawnUnit();
               if(this.pop_total < this.pop_max)
''', '''               this._count_refresh--;
               if(this._count_refresh <= 0)
               {
                  this.pop_total = this.getTotalSpawnUnit();
                  this._count_refresh = 3;
               }
               if(this.pop_total < this.pop_max)
''', 'PlayerUnit throttled count')
t = one(t, '                     this.bSys.charMgr.createPlayerUnit("unit",this.name_id,this.flag_pos_x,this.group);\n                     trace("pop = " + this.getTotalSpawnUnit() + "/" + this.pop_max);\n',
'''                     this.bSys.charMgr.createPlayerUnit("unit",this.name_id,this.flag_pos_x,this.group);
                     this.pop_total = Math.min(this.pop_total + 1,this.pop_max);
                     trace("pop = " + this.pop_total + "/" + this.pop_max);
''', 'PlayerUnit spawn count cache')
write(rel, t)

rel = 'System/Battle/EnemyWave.as'
t = read(rel)
t = one(t, '      private var GROUP:int = 90;\n', '      private var GROUP:int = 90;\n      \n      private var _cached_total:int = 0;\n      \n      private var _count_refresh:int = 0;\n', 'EnemyWave cache fields')
t = one(t, '         this.waveDelayCounter = this.waveTimerDelay * 1.5;\n', '         this.waveDelayCounter = this.waveTimerDelay * 1.5;\n         this._cached_total = 0;\n         this._count_refresh = 0;\n', 'EnemyWave cache init')
t = one(t, '''         if(this.bSys.playerMgr.getStateControl() == "battle")
         {
            if(this.getTotalEnemyWave() < this.MAX_UNIT)
            {
               this.waveSpawn();
            }
         }
''', '''         if(this.bSys.playerMgr.getStateControl() == "battle")
         {
            this._count_refresh--;
            if(this._count_refresh <= 0)
            {
               this._cached_total = this.getTotalEnemyWave();
               this._count_refresh = 3;
            }
            if(this._cached_total < this.MAX_UNIT)
            {
               this.waveSpawn();
            }
         }
''', 'EnemyWave throttled count')
write(rel, t)

checks = {
    'Manager/DataManager.as': ['expansionArmySlotsForClears','getStageExtraClear() >= 8;','dat_stage_expansion_stat.length < 25'],
    'Interface/WorldMapFormationSkill.as': ['MATCH_NUM >= 10 ? 18 : 15','Advanced locked: 18 unique clears'],
    'Interface/WorldMapFormation.as': ['expansionHasAnyEquipment','slot >= 10 ? 18 : 15','maxSlot:int = this.mGF.datMgr.expansionAdvancedUpgradesUnlocked() ? 18 : 9'],
    'System/StatDef/CharTotalStat.as': ['Math.min(Math.max(this.pop,1),16)','Math.min(Math.max(this.reduce_damage,0),0.8)'],
    'Interface/BattleResult.as': ['expansionProgressBefore','Advanced upgrades unlocked!','this.mGF.datMgr.saveData();'],
    'Interface/WorldMap.as': ['12 story and 8 extra','Progress " + this.mGF.datMgr.expansionProgressCount() + "/50'],
    'Interface/WorldMapFormationAcc.as': ['Gear slot " + this.equipSlotPage'],
    'System/Battle/PlayerUnit.as': ['_count_refresh:int','this.pop_total = Math.min(this.pop_total + 1,this.pop_max)'],
    'System/Battle/EnemyWave.as': ['_cached_total:int','this._cached_total = this.getTotalEnemyWave()']
}
for rel, needles in checks.items():
    z = read(rel)
    for n in needles:
        if n not in z: raise SystemExit(f'{rel}: missing polish marker {n}')

print('Epic War 5 Expansion V3.1 polish layer applied')
