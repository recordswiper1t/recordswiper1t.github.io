#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_polish_compat_v32.py <exported-scripts-root>')
base = Path(sys.argv[1])/'scripts'/'Game'

# CharAbilityStat: give the final generated case a deterministic following case
# so the generic V3.2 case replacer can replace case 105 safely.
p = base/'System'/'StatDef'/'CharAbilityStat.as'
t = p.read_text(encoding='utf-8-sig')
anchor = '''            case 105:
               this.name_id = "x_artlogicprime"; this.name_str = "Artlogic Prime"; this.desc = "Damage +35%, health +35%, defense +20%, regen +100"; this.damage_mult = 0.35; this.health_boost = 0.35; this.defense_mult = 0.20; this.health_regen = 100; this.rank = 110;
'''
replacement = anchor + '''               break;
            case 106:
               this.name_id = "__v32_sentinel";
               break;
'''
if t.count(anchor) != 1:
    raise SystemExit(f'V3.2 compact final-case compatibility anchor expected once, got {t.count(anchor)}')
t = t.replace(anchor,replacement,1)
p.write_text(t,encoding='utf-8',newline='\n')

# BattleControlEnemy: normalize the compact fog threshold to the block shape
# used by the V3.2 encounter-tuning patch.
p = base/'System'/'Battle'/'BattleControlEnemy.as'
t = p.read_text(encoding='utf-8-sig')
old = '         if(tier >= 20) this.bSys.x_fog = length;\n'
new = '''         if(tier >= 20)
         {
            this.bSys.x_fog = length;
         }
'''
if t.count(old) != 1:
    raise SystemExit(f'V3.2 compact fog compatibility anchor expected once, got {t.count(old)}')
t = t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')

print('Normalized compact V3 source shapes for V3.2 deterministic replacement')
