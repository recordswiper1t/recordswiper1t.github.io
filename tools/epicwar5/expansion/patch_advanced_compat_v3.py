#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_advanced_compat_v3.py <exported-scripts-root>')
p=Path(sys.argv[1])/'scripts'/'Game'/'System'/'StatDef'/'CharTotalStat.as'
t=p.read_text(encoding='utf-8-sig')
for prop in ['resist_strike','resist_slash','resist_pierce']:
    old=f'''         if(ability9.{prop} != 0)\n         {{\n            this.{prop} = ability9.{prop};\n         }}\n'''
    new=f'''         if(ability9.{prop} != 0 && ability9.{prop} > this.{prop})\n         {{\n            this.{prop} = ability9.{prop};\n         }}\n'''
    if t.count(old)!=1: raise SystemExit(f'ability9 {prop} compatibility anchor expected once, got {t.count(old)}')
    t=t.replace(old,new,1)
old='''         if(ability9.resist_magic != 0)\n         {\n            this.resist_magic = ability9.resist_magic;\n         }\n'''
new='''         if(Boolean(ability9.resist_magic) && ability9.resist_magic > this.resist_magic)\n         {\n            this.resist_magic = ability9.resist_magic;\n         }\n'''
if t.count(old)!=1: raise SystemExit(f'ability9 magic compatibility anchor expected once, got {t.count(old)}')
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')
print('Normalized ability9 resistance stacking for Expansion V3 advanced upgrade layer')
