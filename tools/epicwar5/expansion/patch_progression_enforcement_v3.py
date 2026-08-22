#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_progression_enforcement_v3.py <exported-scripts-root>')
root=Path(sys.argv[1]); base=root/'scripts'/'Game'

# Battle: even if an older save has units stored in slots that are now locked,
# those slots must not instantiate until progression unlocks them.
p=base/'System'/'Battle'/'BattleControlPlayer.as'; t=p.read_text(encoding='utf-8-sig')
for i in range(1,7):
    old=f'this.mGF.datMgr.expansionGetUnitEquip({i}),{i+1})'
    new=f'({i} <= this.mGF.datMgr.expansionArmySlotsUnlocked() ? this.mGF.datMgr.expansionGetUnitEquip({i}) : 0),{i+1})'
    if old not in t: raise SystemExit(f'locked-slot battle anchor missing for slot {i}')
    t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')

# Skill UI: advanced upgrades exist in the binary but cannot be browsed or
# purchased until the campaign progression helper says they are unlocked.
p=base/'Interface'/'WorldMapFormationSkill.as'; t=p.read_text(encoding='utf-8-sig')
t=t.replace('this.mGF.datMgr.expansionContentCleared() < 10','!this.mGF.datMgr.expansionAdvancedUpgradesUnlocked()')
t=t.replace('this.mGF.datMgr.expansionContentCleared() >= 10','this.mGF.datMgr.expansionAdvancedUpgradesUnlocked()')
t=t.replace('advanced upgrades unlock after 10 cleared battles !','advanced upgrades unlock after 18 unique battle clears !')
t=t.replace('Advanced locked: 10 clears','Advanced locked: 18 clears')
p.write_text(t,encoding='utf-8',newline='\n')

for needle in [
    '1 <= this.mGF.datMgr.expansionArmySlotsUnlocked()',
    '6 <= this.mGF.datMgr.expansionArmySlotsUnlocked()',
    'expansionAdvancedUpgradesUnlocked()',
    'Advanced locked: 18 clears'
]:
    z=(base/'System'/'Battle'/'BattleControlPlayer.as').read_text(encoding='utf-8-sig') + (base/'Interface'/'WorldMapFormationSkill.as').read_text(encoding='utf-8-sig')
    if needle not in z: raise SystemExit('missing '+needle)
print('Expansion V3 locked-slot deployment and advanced-upgrade progression enforced')
