#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_battle_rewards_v3.py <exported-scripts-root>')
p=Path(sys.argv[1])/'scripts'/'Game'/'Interface'/'BattleResult.as'
t=p.read_text(encoding='utf-8-sig')
old='''         this.mGF.datMgr.unitSetValue(this.mGF.datMgr.hero_select_id,"exp",this.mGF.datMgr.unitGetValue(this.mGF.datMgr.hero_select_id,"exp") + expReward + expBonus);
         this.mGF.datMgr.unitSetValue(this.mGF.datMgr.unit_equip1_id,"exp",this.mGF.datMgr.unitGetValue(this.mGF.datMgr.unit_equip1_id,"exp") + expReward + expBonus);
         this.mGF.datMgr.unitSetValue(this.mGF.datMgr.unit_equip2_id,"exp",this.mGF.datMgr.unitGetValue(this.mGF.datMgr.unit_equip2_id,"exp") + expReward + expBonus);
         this.mGF.datMgr.unitSetValue(this.mGF.datMgr.unit_equip3_id,"exp",this.mGF.datMgr.unitGetValue(this.mGF.datMgr.unit_equip3_id,"exp") + expReward + expBonus);
         this.mGF.datMgr.unitSetValue(this.mGF.datMgr.unit_equip4_id,"exp",this.mGF.datMgr.unitGetValue(this.mGF.datMgr.unit_equip4_id,"exp") + expReward + expBonus);
         this.mGF.datMgr.unitSetValue(this.mGF.datMgr.unit_equip5_id,"exp",this.mGF.datMgr.unitGetValue(this.mGF.datMgr.unit_equip5_id,"exp") + expReward + expBonus);
         this.mGF.datMgr.unitSetValue(this.mGF.datMgr.unit_equip6_id,"exp",this.mGF.datMgr.unitGetValue(this.mGF.datMgr.unit_equip6_id,"exp") + expReward + expBonus);
'''
new='''         this.mGF.datMgr.unitSetValue(this.mGF.datMgr.hero_select_id,"exp",this.mGF.datMgr.unitGetValue(this.mGF.datMgr.hero_select_id,"exp") + expReward + expBonus);
         var expansionSlot:int = 0;
         var expansionUnitID:int = 0;
         for(expansionSlot = 1; expansionSlot <= this.mGF.datMgr.expansionArmySlotsUnlocked(); expansionSlot++)
         {
            expansionUnitID = this.mGF.datMgr.expansionGetUnitEquip(expansionSlot);
            if(expansionUnitID > 0)
            {
               this.mGF.datMgr.unitSetValue(expansionUnitID,"exp",this.mGF.datMgr.unitGetValue(expansionUnitID,"exp") + expReward + expBonus);
            }
         }
'''
n=t.count(old)
if n!=1: raise SystemExit(f'battle XP block: expected 1 match, got {n}')
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')
for needle in ['expansionArmySlotsUnlocked()','expansionGetUnitEquip(expansionSlot)','expansionUnitID > 0']:
    if needle not in t: raise SystemExit('missing '+needle)
print('Expansion V3 battle XP rewards extended to all unlocked army slots')
