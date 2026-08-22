#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_polish_cleanup_v32.py <exported-scripts-root>')
p = Path(sys.argv[1])/'scripts'/'Game'/'System'/'StatDef'/'CharAbilityStat.as'
t = p.read_text(encoding='utf-8-sig')
sentinel = '''            case 106:
               this.name_id = "__v32_sentinel";
               break;
'''
if t.count(sentinel) != 1:
    raise SystemExit(f'V3.2 sentinel cleanup expected once, got {t.count(sentinel)}')
t = t.replace(sentinel,'',1)
p.write_text(t,encoding='utf-8',newline='\n')
if '__v32_sentinel' in t or 'case 106:' in t:
    raise SystemExit('V3.2 sentinel remained after cleanup')
print('Removed V3.2 final-case compatibility sentinel')
