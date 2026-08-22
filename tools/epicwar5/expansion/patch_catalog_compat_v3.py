#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_catalog_compat_v3.py <exported-scripts-root>')
p=Path(sys.argv[1])/'scripts'/'Game'/'Manager'/'DataManager.as'
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
print('Normalized Expansion V3 inventory migration anchor for equipment catalog')
