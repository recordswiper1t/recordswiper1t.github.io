#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_worldmap_compile_compat_v3.py <exported-scripts-root>')
p=Path(sys.argv[1])/'scripts'/'Game'/'Interface'/'WorldMap.as'
t=p.read_text(encoding='utf-8-sig')

def one(old,new,label):
    global t
    n=t.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    t=t.replace(old,new,1)

one('''         label.text = this.mGF.datMgr.expansionOriginalCampaignComplete() ? "EXPANSION  0/25" : "EXPANSION  LOCKED";\n''','''         if(this.mGF.datMgr.expansionOriginalCampaignComplete()) label.text = "EXPANSION  0/25";\n         else label.text = "EXPANSION  LOCKED";\n''','expansion button label ternary')
one('''            b.graphics.beginFill(unlocked ? 2631720 : 1118481,0.98);\n''','''            if(unlocked) b.graphics.beginFill(2631720,0.98);\n            else b.graphics.beginFill(1118481,0.98);\n''','stage fill ternary')
one('''            b.graphics.lineStyle(1,unlocked ? 10066329 : 4473924,1);\n''','''            if(unlocked) b.graphics.lineStyle(1,10066329,1);\n            else b.graphics.lineStyle(1,4473924,1);\n''','stage border ternary')
one('''            b.alpha = unlocked ? 1 : 0.45; b.buttonMode = unlocked;\n''','''            if(unlocked) b.alpha = 1;\n            else b.alpha = 0.45;\n            b.buttonMode = unlocked;\n''','stage alpha ternary')
one('''            tx.text = String(25 + i) + ". " + String(stageNames[i - 1]) + (this.mGF.datMgr.stageGetValue("expansion",i) >= 1 ? "\\nCLEARED" : (unlocked ? "\\nREADY" : "\\nLOCKED"));\n''','''            var expansionStatus:String = "";\n            if(this.mGF.datMgr.stageGetValue("expansion",i) >= 1) expansionStatus = "\\nCLEARED";\n            else if(unlocked) expansionStatus = "\\nREADY";\n            else expansionStatus = "\\nLOCKED";\n            tx.text = String(25 + i) + ". " + String(stageNames[i - 1]) + expansionStatus;\n''','stage status nested ternary')
p.write_text(t,encoding='utf-8',newline='\n')
for needle in ['var expansionStatus:String','else if(unlocked) expansionStatus','if(unlocked) b.graphics.beginFill']:
    if needle not in t: raise SystemExit('missing '+needle)
print('Expansion V3 WorldMap panel rewritten to FFDec-import-safe if/else syntax')
