#!/usr/bin/env python3
from pathlib import Path
import re, sys

if len(sys.argv) != 2:
    raise SystemExit('usage: build_expansion_storage_v3.py <exported-scripts-root>')
root = Path(sys.argv[1])
path = root/'scripts'/'Game'/'Manager'/'DataManager.as'
text = path.read_text(encoding='utf-8-sig')

def once(old,new,label):
    global text
    n=text.count(old)
    if n != 1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    text=text.replace(old,new,1)

def sub_once(pattern,repl,label,flags=0):
    global text
    text2,n=re.subn(pattern,repl,text,count=1,flags=flags)
    if n != 1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    text=text2

# ------------------------------------------------------------------
# Persistent army slots: extend 6 -> 12 without changing vanilla slots.
# ------------------------------------------------------------------
once('''      public var unit_equip6_id:int = 0;\n''','''      public var unit_equip6_id:int = 0;\n      \n      public var unit_equip7_id:int = 0;\n      \n      public var unit_equip8_id:int = 0;\n      \n      public var unit_equip9_id:int = 0;\n      \n      public var unit_equip10_id:int = 0;\n      \n      public var unit_equip11_id:int = 0;\n      \n      public var unit_equip12_id:int = 0;\n''','army vars')

once('''         this.unit_equip6_id = 0;\n         this.total_kill = 0;\n''','''         this.unit_equip6_id = 0;\n         this.unit_equip7_id = 0;\n         this.unit_equip8_id = 0;\n         this.unit_equip9_id = 0;\n         this.unit_equip10_id = 0;\n         this.unit_equip11_id = 0;\n         this.unit_equip12_id = 0;\n         this.total_kill = 0;\n''','army reset')

once('''         so.data.unit_equip6_id = new int(this.unit_equip6_id);\n         so.data.total_kill = new int(this.total_kill);\n''','''         so.data.unit_equip6_id = new int(this.unit_equip6_id);\n         so.data.unit_equip7_id = new int(this.unit_equip7_id);\n         so.data.unit_equip8_id = new int(this.unit_equip8_id);\n         so.data.unit_equip9_id = new int(this.unit_equip9_id);\n         so.data.unit_equip10_id = new int(this.unit_equip10_id);\n         so.data.unit_equip11_id = new int(this.unit_equip11_id);\n         so.data.unit_equip12_id = new int(this.unit_equip12_id);\n         so.data.total_kill = new int(this.total_kill);\n''','army save')

once('''         this.unit_equip6_id = so.data.unit_equip6_id;\n         this.total_kill = so.data.total_kill;\n''','''         this.unit_equip6_id = so.data.unit_equip6_id;\n         this.unit_equip7_id = int(so.data.unit_equip7_id);\n         this.unit_equip8_id = int(so.data.unit_equip8_id);\n         this.unit_equip9_id = int(so.data.unit_equip9_id);\n         this.unit_equip10_id = int(so.data.unit_equip10_id);\n         this.unit_equip11_id = int(so.data.unit_equip11_id);\n         this.unit_equip12_id = int(so.data.unit_equip12_id);\n         this.total_kill = so.data.total_kill;\n''','army load')

# ------------------------------------------------------------------
# Expansion campaign storage: 25 additional encounter completion values.
# ------------------------------------------------------------------
once('''      public var stage_trial_stat:String = "0,0,0,0,0";\n''','''      public var stage_trial_stat:String = "0,0,0,0,0";\n      \n      public var stage_expansion_stat:String = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0";\n''','expansion stage string')
once('''      private var dat_stage_trial_stat:*;\n''','''      private var dat_stage_trial_stat:*;\n      \n      private var dat_stage_expansion_stat:*;\n''','expansion stage array')
once('''         this.stage_trial_stat = "0,0,0,0,0";\n         this.item_inv =''','''         this.stage_trial_stat = "0,0,0,0,0";\n         this.stage_expansion_stat = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0";\n         this.item_inv =''','expansion stage reset')

stage_helpers='''      private function stageExpansionSetValue(ID:int = 0, VAL:int = 0) : *\n      {\n         if(ID >= 1 && ID <= this.dat_stage_expansion_stat.length)\n         {\n            this.dat_stage_expansion_stat[ID - 1] = VAL;\n         }\n      }\n      \n      private function stageExpansionGetValue(ID:int = 0) : int\n      {\n         if(ID >= 1 && ID <= this.dat_stage_expansion_stat.length)\n         {\n            return int(this.dat_stage_expansion_stat[ID - 1]);\n         }\n         return 0;\n      }\n      \n'''
once('''      public function stageSetValue(TYPE:String = "normal", ID:int = 0, VAL:int = 0) : *\n''',stage_helpers+'''      public function stageSetValue(TYPE:String = "normal", ID:int = 0, VAL:int = 0) : *\n''','expansion stage helpers')
once('''         if(TYPE == "extra")\n         {\n            this.stageExtraSetValue(ID,VAL);\n         }\n         else if(TYPE == "trial")\n''','''         if(TYPE == "expansion")\n         {\n            this.stageExpansionSetValue(ID,VAL);\n         }\n         else if(TYPE == "extra")\n         {\n            this.stageExtraSetValue(ID,VAL);\n         }\n         else if(TYPE == "trial")\n''','expansion stage setter route')
once('''         if(TYPE == "extra")\n         {\n            return this.stageExtraGetValue(ID);\n         }\n         if(TYPE == "trial")\n''','''         if(TYPE == "expansion")\n         {\n            return this.stageExpansionGetValue(ID);\n         }\n         if(TYPE == "extra")\n         {\n            return this.stageExtraGetValue(ID);\n         }\n         if(TYPE == "trial")\n''','expansion stage getter route')

once('''         this.stage_trial_stat = this.mergeArrayString(this.dat_stage_trial_stat);\n''','''         this.stage_trial_stat = this.mergeArrayString(this.dat_stage_trial_stat);\n         this.stage_expansion_stat = this.mergeArrayString(this.dat_stage_expansion_stat);\n''','expansion stage merge')
once('''         this.dat_stage_trial_stat = this.stage_trial_stat.split(",");\n''','''         this.dat_stage_trial_stat = this.stage_trial_stat.split(",");\n         this.dat_stage_expansion_stat = this.stage_expansion_stat.split(",");\n''','expansion stage split')
once('''         so.data.stage_trial_stat = new String(this.stage_trial_stat);\n''','''         so.data.stage_trial_stat = new String(this.stage_trial_stat);\n         so.data.stage_expansion_stat = new String(this.stage_expansion_stat);\n''','expansion stage save')
once('''         this.stage_trial_stat = so.data.stage_trial_stat;\n         this.loadArrayStringData();\n''','''         this.stage_trial_stat = so.data.stage_trial_stat;\n         this.stage_expansion_stat = so.data.stage_expansion_stat == undefined ? "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0" : String(so.data.stage_expansion_stat);\n         this.loadArrayStringData();\n         this.expansionEnsureData();\n''','expansion stage load')

# New game also migrates/expands unit arrays after vanilla arrays are created.
once('''         this.loadArrayStringData();\n         trace(" reset data ... ");\n''','''         this.loadArrayStringData();\n         this.expansionEnsureData();\n         trace(" reset data ... expansion storage ready ");\n''','new-save expansion migrate')

# ------------------------------------------------------------------
# Unit data rows: preserve original positions, append item2/item3 + ability10..18.
# ------------------------------------------------------------------
set_cases='''            case "item2":\n               statID = 12;\n               break;\n            case "item3":\n               statID = 13;\n               break;\n            case "ability10":\n               statID = 14;\n               break;\n            case "ability11":\n               statID = 15;\n               break;\n            case "ability12":\n               statID = 16;\n               break;\n            case "ability13":\n               statID = 17;\n               break;\n            case "ability14":\n               statID = 18;\n               break;\n            case "ability15":\n               statID = 19;\n               break;\n            case "ability16":\n               statID = 20;\n               break;\n            case "ability17":\n               statID = 21;\n               break;\n            case "ability18":\n               statID = 22;\n               break;\n'''
once('''            case "ability9":\n               statID = 11;\n         }\n''','''            case "ability9":\n               statID = 11;\n               break;\n'''+set_cases+'''         }\n''','unitSet expansion fields')
# The same switch text occurs independently in unitGetValue after the first replacement.
once('''            case "ability9":\n               statID = 11;\n         }\n''','''            case "ability9":\n               statID = 11;\n               break;\n'''+set_cases+'''         }\n''','unitGet expansion fields')

# ------------------------------------------------------------------
# Progression helpers and migration. These are structural APIs for later UI/battle patches.
# ------------------------------------------------------------------
helpers=r'''      public function expansionArmySlotsUnlocked() : int
      {
         var s:int = Math.max(1,this.mission_stage);
         if(s >= 42) return 12;
         if(s >= 34) return 11;
         if(s >= 27) return 10;
         if(s >= 22) return 9;
         if(s >= 18) return 8;
         if(s >= 14) return 7;
         if(s >= 10) return 6;
         if(s >= 6) return 5;
         if(s >= 3) return 4;
         return 3;
      }
      
      public function expansionEquipmentSlotsUnlocked() : int
      {
         if(this.mission_stage >= 27) return 3;
         if(this.mission_stage >= 14) return 2;
         return 1;
      }
      
      public function expansionGetUnitEquip(SLOT:int) : int
      {
         switch(SLOT)
         {
            case 1: return this.unit_equip1_id;
            case 2: return this.unit_equip2_id;
            case 3: return this.unit_equip3_id;
            case 4: return this.unit_equip4_id;
            case 5: return this.unit_equip5_id;
            case 6: return this.unit_equip6_id;
            case 7: return this.unit_equip7_id;
            case 8: return this.unit_equip8_id;
            case 9: return this.unit_equip9_id;
            case 10: return this.unit_equip10_id;
            case 11: return this.unit_equip11_id;
            case 12: return this.unit_equip12_id;
         }
         return 0;
      }
      
      public function expansionSetUnitEquip(SLOT:int, ID:int) : void
      {
         if(SLOT < 1 || SLOT > 12) return;
         if(SLOT > this.expansionArmySlotsUnlocked()) return;
         switch(SLOT)
         {
            case 1: this.unit_equip1_id = ID; break;
            case 2: this.unit_equip2_id = ID; break;
            case 3: this.unit_equip3_id = ID; break;
            case 4: this.unit_equip4_id = ID; break;
            case 5: this.unit_equip5_id = ID; break;
            case 6: this.unit_equip6_id = ID; break;
            case 7: this.unit_equip7_id = ID; break;
            case 8: this.unit_equip8_id = ID; break;
            case 9: this.unit_equip9_id = ID; break;
            case 10: this.unit_equip10_id = ID; break;
            case 11: this.unit_equip11_id = ID; break;
            case 12: this.unit_equip12_id = ID; break;
         }
      }
      
      private function expansionEnsureData() : void
      {
         var ids:Array = [1,2,3,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,50,51,52,53,54,55,56,57,58,59,60];
         var fields:Array = ["item2","item3","ability10","ability11","ability12","ability13","ability14","ability15","ability16","ability17","ability18"];
         var id:int = 0;
         var field:String = "";
         for each(id in ids)
         {
            for each(field in fields)
            {
               this.unitSetValue(id,field,this.unitGetValue(id,field));
            }
         }
      }
      
'''
once('''      public function cheatMode() : *\n''',helpers+'''      public function cheatMode() : *\n''','expansion helpers')

path.write_text(text,encoding='utf-8',newline='\n')

needles=[
'unit_equip12_id','stage_expansion_stat','case "item2"','case "ability18"',
'expansionArmySlotsUnlocked','expansionEquipmentSlotsUnlocked','expansionGetUnitEquip',
'expansionEnsureData();','so.data.unit_equip12_id','so.data.stage_expansion_stat'
]
for n in needles:
    if n not in text: raise SystemExit(f'validation failed: {n}')
print('Expansion V3 persistent storage/progression foundation applied')
