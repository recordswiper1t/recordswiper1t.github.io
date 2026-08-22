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

# The catalog appender's Python triple-quoted anchor evaluates \' to a plain
# apostrophe. Emit exactly that ActionScript text so its replacement is stable.
p=root/'System'/'StatDef'/'CharItemStat.as'
t=p.read_text(encoding='utf-8-sig')
start=t.index('            case 30:\n')
end=t.index('         }\n         var a:*',start)
canonical='''            case 30:
               this.name_id = "itm_special";
               this.name_str = "Artlogic\'s Badge";
               this.desc = "Grants awesome skill!?";
               this.rank = 3;
               this.ability_name_id = "p_special";
'''
t=t[:start]+canonical+t[end:]
p.write_text(t,encoding='utf-8',newline='\n')

# The vanilla ninth ability uses "last nonzero wins" resistance blocks, while
# the advanced layer stacks abilities 10..18 with strongest-value semantics.
# Normalize ability 9 into that same shape before the advanced patch runs.
p=root/'System'/'StatDef'/'CharTotalStat.as'
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
print('Normalized Expansion V3 catalog and advanced-upgrade compatibility anchors')
