#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_catalog_item_compat_v3.py <exported-scripts-root>')
p=Path(sys.argv[1])/'scripts'/'Game'/'System'/'StatDef'/'CharItemStat.as'
t=p.read_text(encoding='utf-8-sig')
start=t.index('            case 30:\n')
end=t.index('         }\n         var a:*',start)
canonical='''            case 30:
               this.name_id = "itm_special";
               this.name_str = "Artlogic\\'s Badge";
               this.desc = "Grants awesome skill!?";
               this.rank = 3;
               this.ability_name_id = "p_special";
'''
t=t[:start]+canonical+t[end:]
p.write_text(t,encoding='utf-8',newline='\n')
print('Canonicalized legacy item 30 block before Expansion V3 catalog append')
