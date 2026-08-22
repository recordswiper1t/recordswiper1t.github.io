#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: build_expansion_storage_v3.py <exported-scripts-root>')
root=Path(sys.argv[1]); p=root/'scripts'/'Game'/'Manager'/'DataManager.as'
t=p.read_text(encoding='utf-8-sig')

def one(old,new,label):
    global t
    n=t.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    t=t.replace(old,new,1)

def two_in_order(old,new,label):
    global t
    n=t.count(old)
    if n!=2: raise SystemExit(f'{label}: expected 2 matches, got {n}')
    t=t.replace(old,new,1)
    t=t.replace(old,new,1)

# 12 persistent army slots.
one('      public var unit_equip6_id:int = 0;\n','''      public var unit_equip6_id:int = 0;
      
      public var unit_equip7_id:int = 0;
      public var unit_equip8_id:int = 0;
      public var unit_equip9_id:int = 0;
      public var unit_equip10_id:int = 0;
      public var unit_equip11_id:int = 0;
      public var unit_equip12_id:int = 0;
''','army vars')
one('''         this.unit_equip6_id = 0;
         this.total_kill = 0;
''','''         this.unit_equip6_id = 0;
         this.unit_equip7_id = 0;
         this.unit_equip8_id = 0;
         this.unit_equip9_id = 0;
         this.unit_equip10_id = 0;
         this.unit_equip11_id = 0;
         this.unit_equip12_id = 0;
         this.total_kill = 0;
''','army reset')
one('''         so.data.unit_equip6_id = new int(this.unit_equip6_id);
         so.data.total_kill = new int(this.total_kill);
''','''         so.data.unit_equip6_id = new int(this.unit_equip6_id);
         so.data.unit_equip7_id = new int(this.unit_equip7_id);
         so.data.unit_equip8_id = new int(this.unit_equip8_id);
         so.data.unit_equip9_id = new int(this.unit_equip9_id);
         so.data.unit_equip10_id = new int(this.unit_equip10_id);
         so.data.unit_equip11_id = new int(this.unit_equip11_id);
         so.data.unit_equip12_id = new int(this.unit_equip12_id);
         so.data.total_kill = new int(this.total_kill);
''','army save')
one('''         this.unit_equip6_id = so.data.unit_equip6_id;
         this.total_kill = so.data.total_kill;
''','''         this.unit_equip6_id = so.data.unit_equip6_id;
         this.unit_equip7_id = int(so.data.unit_equip7_id);
         this.unit_equip8_id = int(so.data.unit_equip8_id);
         this.unit_equip9_id = int(so.data.unit_equip9_id);
         this.unit_equip10_id = int(so.data.unit_equip10_id);
         this.unit_equip11_id = int(so.data.unit_equip11_id);
         this.unit_equip12_id = int(so.data.unit_equip12_id);
         this.total_kill = so.data.total_kill;
''','army load')

# 25 new expansion encounter completion values.
EXP='0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'
one('      public var stage_trial_stat:String = "0,0,0,0,0";\n',f'''      public var stage_trial_stat:String = "0,0,0,0,0";
      
      public var stage_expansion_stat:String = "{EXP}";
''','expansion stage var')
one('      private var dat_stage_trial_stat:*;\n','''      private var dat_stage_trial_stat:*;
      
      private var dat_stage_expansion_stat:*;
''','expansion stage array')
one('''         this.stage_trial_stat = "0,0,0,0,0";
         this.item_inv =''',f'''         this.stage_trial_stat = "0,0,0,0,0";
         this.stage_expansion_stat = "{EXP}";
         this.item_inv =''','expansion reset')

stage_helpers='''      private function stageExpansionSetValue(ID:int = 0, VAL:int = 0) : *
      {
         if(ID >= 1 && ID <= this.dat_stage_expansion_stat.length) this.dat_stage_expansion_stat[ID - 1] = VAL;
      }
      
      private function stageExpansionGetValue(ID:int = 0) : int
      {
         if(ID >= 1 && ID <= this.dat_stage_expansion_stat.length) return int(this.dat_stage_expansion_stat[ID - 1]);
         return 0;
      }
      
'''
one('      public function stageSetValue(TYPE:String = "normal", ID:int = 0, VAL:int = 0) : *\n',stage_helpers+'      public function stageSetValue(TYPE:String = "normal", ID:int = 0, VAL:int = 0) : *\n','stage helpers')
one('''         if(TYPE == "extra")
         {
            this.stageExtraSetValue(ID,VAL);
         }
         else if(TYPE == "trial")
''','''         if(TYPE == "expansion")
         {
            this.stageExpansionSetValue(ID,VAL);
         }
         else if(TYPE == "extra")
         {
            this.stageExtraSetValue(ID,VAL);
         }
         else if(TYPE == "trial")
''','stage set route')
one('''         if(TYPE == "extra")
         {
            return this.stageExtraGetValue(ID);
         }
         if(TYPE == "trial")
''','''         if(TYPE == "expansion") return this.stageExpansionGetValue(ID);
         if(TYPE == "extra")
         {
            return this.stageExtraGetValue(ID);
         }
         if(TYPE == "trial")
''','stage get route')
one('         this.stage_trial_stat = this.mergeArrayString(this.dat_stage_trial_stat);\n','         this.stage_trial_stat = this.mergeArrayString(this.dat_stage_trial_stat);\n         this.stage_expansion_stat = this.mergeArrayString(this.dat_stage_expansion_stat);\n','stage merge')
one('         this.dat_stage_trial_stat = this.stage_trial_stat.split(",");\n','         this.dat_stage_trial_stat = this.stage_trial_stat.split(",");\n         this.dat_stage_expansion_stat = this.stage_expansion_stat.split(",");\n','stage split')
one('         so.data.stage_trial_stat = new String(this.stage_trial_stat);\n','         so.data.stage_trial_stat = new String(this.stage_trial_stat);\n         so.data.stage_expansion_stat = new String(this.stage_expansion_stat);\n','stage save')
one('''         this.stage_trial_stat = so.data.stage_trial_stat;
         this.loadArrayStringData();
''',f'''         this.stage_trial_stat = so.data.stage_trial_stat;
         this.stage_expansion_stat = so.data.stage_expansion_stat == undefined ? "{EXP}" : String(so.data.stage_expansion_stat);
         this.loadArrayStringData();
         this.expansionEnsureData();
''','stage load')
one('''         this.loadArrayStringData();
         trace(" reset data ... ");
''','''         this.loadArrayStringData();
         this.expansionEnsureData();
         trace(" reset data ... expansion storage ready ");
''','new save migration')

# Preserve old row indexes, append item2/item3 and ability10..18 at indexes 12..22.
extra_cases='''               break;
            case "item2":
               statID = 12;
               break;
            case "item3":
               statID = 13;
               break;
            case "ability10":
               statID = 14;
               break;
            case "ability11":
               statID = 15;
               break;
            case "ability12":
               statID = 16;
               break;
            case "ability13":
               statID = 17;
               break;
            case "ability14":
               statID = 18;
               break;
            case "ability15":
               statID = 19;
               break;
            case "ability16":
               statID = 20;
               break;
            case "ability17":
               statID = 21;
               break;
            case "ability18":
               statID = 22;
'''
anchor='''            case "ability9":
               statID = 11;
         }
'''
replacement='''            case "ability9":
               statID = 11;
'''+extra_cases+'''         }
'''
two_in_order(anchor,replacement,'unit set/get expansion fields')

helpers='''      public function expansionContentCleared() : int
      {
         var total:int = 0;
         var i:int = 0;
         for(i = 1; i <= 12; i++) if(this.stageGetValue("normal",i) >= 1) total++;
         for(i = 1; i <= 8; i++) if(this.stageGetValue("extra",i) >= 1) total++;
         for(i = 1; i <= 5; i++) if(this.stageGetValue("trial",i) >= 1) total++;
         for(i = 1; i <= 25; i++) if(this.stageGetValue("expansion",i) >= 1) total++;
         return total;
      }
      
      public function expansionArmySlotsUnlocked() : int
      {
         var c:int = this.expansionContentCleared();
         if(c >= 42) return 12;
         if(c >= 34) return 11;
         if(c >= 27) return 10;
         if(c >= 22) return 9;
         if(c >= 18) return 8;
         if(c >= 14) return 7;
         if(c >= 10) return 6;
         if(c >= 6) return 5;
         if(c >= 3) return 4;
         return 3;
      }
      
      public function expansionEquipmentSlotsUnlocked() : int
      {
         var c:int = this.expansionContentCleared();
         if(c >= 27) return 3;
         if(c >= 14) return 2;
         return 1;
      }
      
      public function expansionGetUnitEquip(SLOT:int) : int
      {
         switch(SLOT)
         {
            case 1: return this.unit_equip1_id; case 2: return this.unit_equip2_id; case 3: return this.unit_equip3_id;
            case 4: return this.unit_equip4_id; case 5: return this.unit_equip5_id; case 6: return this.unit_equip6_id;
            case 7: return this.unit_equip7_id; case 8: return this.unit_equip8_id; case 9: return this.unit_equip9_id;
            case 10: return this.unit_equip10_id; case 11: return this.unit_equip11_id; case 12: return this.unit_equip12_id;
         }
         return 0;
      }
      
      public function expansionSetUnitEquip(SLOT:int, ID:int) : void
      {
         if(SLOT < 1 || SLOT > this.expansionArmySlotsUnlocked()) return;
         switch(SLOT)
         {
            case 1: this.unit_equip1_id=ID; break; case 2: this.unit_equip2_id=ID; break; case 3: this.unit_equip3_id=ID; break;
            case 4: this.unit_equip4_id=ID; break; case 5: this.unit_equip5_id=ID; break; case 6: this.unit_equip6_id=ID; break;
            case 7: this.unit_equip7_id=ID; break; case 8: this.unit_equip8_id=ID; break; case 9: this.unit_equip9_id=ID; break;
            case 10: this.unit_equip10_id=ID; break; case 11: this.unit_equip11_id=ID; break; case 12: this.unit_equip12_id=ID; break;
         }
      }
      
      private function expansionEnsureData() : void
      {
         var ids:Array=[1,2,3,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,50,51,52,53,54,55,56,57,58,59,60];
         var fields:Array=["item2","item3","ability10","ability11","ability12","ability13","ability14","ability15","ability16","ability17","ability18"];
         var id:int=0; var field:String="";
         for each(id in ids) for each(field in fields) this.unitSetValue(id,field,this.unitGetValue(id,field));
      }
      
'''
one('      public function cheatMode() : *\n',helpers+'      public function cheatMode() : *\n','expansion APIs')

p.write_text(t,encoding='utf-8',newline='\n')
for needle in ['unit_equip12_id','stage_expansion_stat','case "item2"','case "ability18"','expansionContentCleared','expansionArmySlotsUnlocked','expansionEquipmentSlotsUnlocked','so.data.unit_equip12_id','so.data.stage_expansion_stat']:
    if needle not in t: raise SystemExit('missing '+needle)
print('Expansion V3 persistent storage/progression foundation applied')
