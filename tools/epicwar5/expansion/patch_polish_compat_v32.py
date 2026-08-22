#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_polish_compat_v32.py <exported-scripts-root>')
p = Path(sys.argv[1])/'scripts'/'Game'/'System'/'StatDef'/'CharAbilityStat.as'
t = p.read_text(encoding='utf-8-sig')
anchor = '''               this.health_regen = 100;
               this.rank = 110;
         }
      }
'''
replacement = '''               this.health_regen = 100;
               this.rank = 110;
               break;
            case 106:
               this.name_id = "__v32_sentinel";
               break;
         }
      }
'''
if t.count(anchor) != 1:
    raise SystemExit(f'V3.2 final-case compatibility anchor expected once, got {t.count(anchor)}')
t = t.replace(anchor,replacement,1)
p.write_text(t,encoding='utf-8',newline='\n')
print('Prepared final ability switch case for V3.2 deterministic replacement')
