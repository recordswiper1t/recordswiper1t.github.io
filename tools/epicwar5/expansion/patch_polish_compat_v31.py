#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_polish_compat_v31.py <exported-scripts-root>')
root = Path(sys.argv[1])/'scripts'/'Game'

# Normalize compact inventory padding emitted by the catalog patch.
p = root/'Manager'/'DataManager.as'
t = p.read_text(encoding='utf-8-sig')
old = '         while(this.dat_item_inv.length < 55) this.dat_item_inv.push(0);\n'
new = '''         while(this.dat_item_inv.length < 55)
         {
            this.dat_item_inv.push(0);
         }
'''
if t.count(old) != 1:
    raise SystemExit(f'polish compatibility inventory anchor expected once, got {t.count(old)}')
t = t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')

# FFDec's rebuild/re-export adds a redundant assignment block for ability10..18
# in the main stat initializer. The same declaration also exists in preview
# methods, so normalize only the first occurrence.
p = root/'System'/'StatDef'/'CharTotalStat.as'
t = p.read_text(encoding='utf-8-sig')
anchor = '         var ability18:* = new CharAbilityStat(this.unit_ability18_id);\n'
if t.count(anchor) < 1:
    raise SystemExit('advanced compatibility anchor missing')
dup = ''.join(f'         ability{i} = new CharAbilityStat(this.unit_ability{i}_id);\n' for i in range(10,19))
t = t.replace(anchor,anchor+dup,1)
p.write_text(t,encoding='utf-8',newline='\n')
print('Normalized Expansion V3 source formatting for V3.1 polish')
