#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_catalog_compat_v3.py <exported-scripts-root>')
root=Path(sys.argv[1])/'scripts'/'Game'

# Normalize compact DataManager formatting emitted by the storage patcher.
p=root/'Manager'/'DataManager.as'
t=p.read_text(encoding='utf-8-sig')
old='''      private function expansionEnsureData() : void
      {
         var ids:Array=['''
new='''      private function expansionEnsureData() : void
      {
         var ids:Array =['''
if t.count(old)!=1: raise SystemExit('catalog compatibility anchor not found exactly once')
t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8',newline='\n')

# Normalize FFDec's apostrophe escaping in the final vanilla item so the
# catalog appender has one stable block to replace.
p=root/'System'/'StatDef'/'CharItemStat.as'
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
print('Normalized Expansion V3 inventory migration and legacy item anchors for equipment catalog')
