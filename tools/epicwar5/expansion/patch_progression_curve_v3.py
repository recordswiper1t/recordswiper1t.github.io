#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_progression_curve_v3.py <exported-scripts-root>')

root = Path(sys.argv[1])
p = root / 'scripts' / 'Game' / 'Manager' / 'DataManager.as'
t = p.read_text(encoding='utf-8-sig')


def replace_method(name, next_name, body):
    global t
    start = t.index('      public function ' + name + '(')
    end = t.index('      public function ' + next_name + '(', start)
    t = t[:start] + body + t[end:]


progress_methods = r'''      public function expansionProgressCount() : int
      {
         var total:int = 0;
         var i:int = 0;
         for(i = 1; i <= 12; i++) if(this.stageGetValue("normal",i) >= 1) total++;
         for(i = 1; i <= 8; i++) if(this.stageGetValue("extra",i) >= 1) total++;
         for(i = 1; i <= 5; i++) if(this.stageGetValue("trial",i) >= 1) total++;
         for(i = 1; i <= 25; i++) if(this.stageGetValue("expansion",i) >= 1) total++;
         return total;
      }
      
      public function expansionOriginalCampaignComplete() : Boolean
      {
         return this.getStageNormalClear() >= 12 && this.getStageExtraClear() >= 8 && this.getStageTrialClear() >= 5;
      }
      
      public function expansionArmySlotsUnlocked() : int
      {
         var clears:int = this.expansionProgressCount();
         if(clears >= 48) return 12;
         if(clears >= 41) return 11;
         if(clears >= 34) return 10;
         if(clears >= 27) return 9;
         if(clears >= 20) return 8;
         if(clears >= 14) return 7;
         if(clears >= 9) return 6;
         if(clears >= 5) return 5;
         if(clears >= 2) return 4;
         return 3;
      }
      
      public function expansionEquipmentSlotsUnlocked() : int
      {
         var clears:int = this.expansionProgressCount();
         if(clears >= 35) return 3;
         if(clears >= 15) return 2;
         return 1;
      }
      
      public function expansionAdvancedUpgradesUnlocked() : Boolean
      {
         return this.expansionProgressCount() >= 18;
      }
      
'''

start = t.index('      public function expansionArmySlotsUnlocked() : int\n')
end = t.index('      public function expansionGetUnitEquip(', start)
t = t[:start] + progress_methods + t[end:]

# The original percentage meter only knows about the original 25 battles. Make
# it describe the full 50-battle campaign while keeping the public method name.
replace_method('getStageClear', 'getStageNormalClear', r'''      public function getStageClear() : int
      {
         return this.expansionProgressCount() * 100 / 50;
      }
      
''')

p.write_text(t, encoding='utf-8', newline='\n')

for needle in [
    'expansionProgressCount()',
    'stageGetValue("expansion",i)',
    'if(clears >= 48) return 12;',
    'if(clears >= 35) return 3;',
    'expansionAdvancedUpgradesUnlocked()',
    'return this.expansionProgressCount() * 100 / 50;'
]:
    if needle not in t:
        raise SystemExit('validation failed: ' + needle)

if 'this.mission_stage >= 27' in t or 'var s:int = Math.max(1,this.mission_stage)' in t:
    raise SystemExit('old mission_stage-based expansion progression still present')

print('Expansion V3 clear-count progression curve applied: 3->12 army slots, 1->3 equipment slots')
