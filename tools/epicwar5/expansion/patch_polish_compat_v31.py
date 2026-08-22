#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_polish_compat_v31.py <exported-scripts-root>')
p = Path(sys.argv[1])/'scripts'/'Game'/'Manager'/'DataManager.as'
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
print('Normalized Expansion V3 source formatting for V3.1 polish')
