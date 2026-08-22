#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_campaign_newline_compat_v3.py <exported-scripts-root>')

p = Path(sys.argv[1]) / 'scripts' / 'Game' / 'Interface' / 'WorldMap.as'
t = p.read_text(encoding='utf-8-sig')

broken = '''? "
CLEARED" : (unlocked ? "
READY" : "
LOCKED"))'''
fixed = '? "\\nCLEARED" : (unlocked ? "\\nREADY" : "\\nLOCKED"))'

count = t.count(broken)
if count != 1:
    raise SystemExit(f'campaign newline compatibility anchor expected once, got {count}')

t = t.replace(broken, fixed, 1)
p.write_text(t, encoding='utf-8', newline='\n')

if '\\nCLEARED' not in t or '\\nREADY' not in t or '\\nLOCKED' not in t:
    raise SystemExit('campaign escaped status labels missing after normalization')

print('Normalized Expansion V3 campaign status label newlines for FFDec import')
