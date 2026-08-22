#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_battle_12_units_v3.py <exported-scripts-root>')
p=Path(sys.argv[1])/'scripts'/'Game'/'System'/'Battle'/'BattleControlPlayer.as'
t=p.read_text(encoding='utf-8-sig')

def one(old,new,label):
    global t
    n=t.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    t=t.replace(old,new,1)

def two(old,new,label):
    global t
    n=t.count(old)
    if n!=2: raise SystemExit(f'{label}: expected 2 matches, got {n}')
    t=t.replace(old,new,2)

def replace_method(name,next_name,new_body):
    global t
    start=t.index('      public function '+name+'(')
    end=t.index('      public function '+next_name+'(',start)
    t=t[:start]+new_body+t[end:]

one('''   import flash.events.MouseEvent;
''','''   import flash.events.MouseEvent;
   import flash.utils.getDefinitionByName;
   import flash.utils.getQualifiedClassName;
''','battle clone imports')
one('''      private var mUnit6:*;
''','''      private var mUnit6:*;
      
      private var expansionUnits:Array = [];
      
      private var expansionUnitClips:Array = [];
''','expansion battle arrays')
one('''         this.mUnit6 = new PlayerUnit(this.mGF,this.bSys,this.bSys.ui.unit6,"unit",this.mGF.datMgr.unit_equip6_id,7);
         this.mSpell1 =''','''         this.mUnit6 = new PlayerUnit(this.mGF,this.bSys,this.bSys.ui.unit6,"unit",this.mGF.datMgr.expansionGetUnitEquip(6),7);
         this.expansionInitUnits();
         this.mSpell1 =''','battle init extra units')
for i,group in [(1,2),(2,3),(3,4),(4,5),(5,6)]:
    one(f'''         this.mUnit{i} = new PlayerUnit(this.mGF,this.bSys,this.bSys.ui.unit{i},"unit",this.mGF.datMgr.unit_equip{i}_id,{group});
''',f'''         this.mUnit{i} = new PlayerUnit(this.mGF,this.bSys,this.bSys.ui.unit{i},"unit",this.mGF.datMgr.expansionGetUnitEquip({i}),{group});
''',f'unit{i} generic getter')

helpers='''      private function expansionInitUnits() : void
      {
         this.expansionUnits = [];
         this.expansionUnitClips = [];
         var cls:Class = getDefinitionByName(getQualifiedClassName(this.bSys.ui.unit1)) as Class;
         var refs:Array = [this.bSys.ui.unit1,this.bSys.ui.unit2,this.bSys.ui.unit3,this.bSys.ui.unit4,this.bSys.ui.unit5,this.bSys.ui.unit6];
         var i:int = 0;
         var slot:int = 0;
         var clip:* = null;
         var unit:* = null;
         var id:int = 0;
         for(i = 0; i < 6; i++)
         {
            slot = i + 7;
            clip = new cls();
            clip.x = refs[i].x;
            clip.y = refs[i].y - Math.max(46,refs[i].height + 3);
            clip.scaleX = refs[i].scaleX;
            clip.scaleY = refs[i].scaleY;
            refs[i].parent.addChild(clip);
            this.expansionUnitClips.push(clip);
            id = slot <= this.mGF.datMgr.expansionArmySlotsUnlocked() ? this.mGF.datMgr.expansionGetUnitEquip(slot) : 0;
            unit = new PlayerUnit(this.mGF,this.bSys,clip,"unit",id,slot + 1);
            this.expansionUnits.push(unit);
         }
      }
      
      private function expansionDestroyUnits() : void
      {
         var unit:* = null;
         var clip:* = null;
         for each(unit in this.expansionUnits) if(unit != null) unit.destroy();
         for each(clip in this.expansionUnitClips) if(clip != null && clip.parent != null) clip.parent.removeChild(clip);
         this.expansionUnits = [];
         this.expansionUnitClips = [];
      }
      
      private function expansionForceMove(X:int) : void
      {
         var unit:* = null;
         for each(unit in this.expansionUnits) if(unit != null) unit.cmdForceMove(X);
      }
      
      private function expansionSelectedMove(X:int) : void
      {
         var unit:* = null;
         for each(unit in this.expansionUnits) if(unit != null) unit.cmdSelectedMove(X);
      }
      
      private function expansionSelectAll(VAL:Boolean) : void
      {
         var unit:* = null;
         for each(unit in this.expansionUnits) if(unit != null) unit.cmdSelect(VAL);
      }
      
      private function expansionExecuteSelected(X:int) : void
      {
         var unit:* = null;
         for each(unit in this.expansionUnits) if(unit != null) unit.cmdExecute(X);
      }
      
      private function expansionGetSelected() : *
      {
         var unit:* = null;
         for each(unit in this.expansionUnits) if(unit != null && unit.isSelected()) return unit;
         return null;
      }
      
'''
one('''      public function setStateControl(VAL:String) : *
''',helpers+'''      public function setStateControl(VAL:String) : *
''','battle helper insert')
one('''         if(this.mUnit6)
         {
            this.mUnit6.destroy();
            this.mUnit6 = null;
         }
         if(this.mSpell1)
''','''         if(this.mUnit6)
         {
            this.mUnit6.destroy();
            this.mUnit6 = null;
         }
         this.expansionDestroyUnits();
         if(this.mSpell1)
''','destroy extra units')
one('''         this.mUnit6.cmdForceMove(3500);
         trace("all unit Marching ...!!");
''','''         this.mUnit6.cmdForceMove(3500);
         this.expansionForceMove(3500);
         trace("all unit Marching ...!!");
''','march extras')
one('''         this.mUnit6.cmdSelectedMove(3500);
         this.cancelAllSelect();
''','''         this.mUnit6.cmdSelectedMove(3500);
         this.expansionSelectedMove(3500);
         this.cancelAllSelect();
''','selected march extras')
one('''         this.mUnit6.cmdForceMove(100);
         trace("all unit Retreat ...!!");
''','''         this.mUnit6.cmdForceMove(100);
         this.expansionForceMove(100);
         trace("all unit Retreat ...!!");
''','retreat extras')
one('''         this.mUnit6.cmdSelectedMove(100);
         this.cancelAllSelect();
''','''         this.mUnit6.cmdSelectedMove(100);
         this.expansionSelectedMove(100);
         this.cancelAllSelect();
''','selected retreat extras')

select_tail='''         if(this.mUnit6)
         {
            this.mUnit6.cmdSelect(true);
         }
         this.showCursor("unit");
'''
select_tail_new='''         if(this.mUnit6)
         {
            this.mUnit6.cmdSelect(true);
         }
         this.expansionSelectAll(true);
         this.showCursor("unit");
'''
two(select_tail,select_tail_new,'both select-all methods')

one('''         else if(NUM == 7)
         {
            if(this.mUnit6)
            {
               this.mUnit6.cmdSelect(true);
               this.mUnit6.getSpellList();
            }
         }
         this.showCursor("unit");
''','''         else if(NUM == 7)
         {
            if(this.mUnit6)
            {
               this.mUnit6.cmdSelect(true);
               this.mUnit6.getSpellList();
            }
         }
         else if(NUM >= 8 && NUM <= 13)
         {
            var expansionUnit:* = this.expansionUnits[NUM - 8];
            if(expansionUnit)
            {
               expansionUnit.cmdSelect(true);
               expansionUnit.getSpellList();
            }
         }
         this.showCursor("unit");
''','select expansion group')
one('''         if(this.mUnit6)
         {
            this.mUnit6.cmdSelect(false);
         }
      }
      
      public function getLastSelected()''','''         if(this.mUnit6)
         {
            this.mUnit6.cmdSelect(false);
         }
         this.expansionSelectAll(false);
      }
      
      public function getLastSelected()''','deselect extras')
one('''         if(this.mUnit6.isSelected())
         {
            this.showCursor("unit");
            this.mUnit6.getSpellList();
            return true;
         }
         return false;
''','''         if(this.mUnit6.isSelected())
         {
            this.showCursor("unit");
            this.mUnit6.getSpellList();
            return true;
         }
         var expansionSelected:* = this.expansionGetSelected();
         if(expansionSelected != null)
         {
            this.showCursor("unit");
            expansionSelected.getSpellList();
            return true;
         }
         return false;
''','last selected extras')
one('''               this.mUnit6.cmdExecute(this.cursorClip.x - this.mGF.contSCROLL.x);
               this.removeCursor();
''','''               this.mUnit6.cmdExecute(this.cursorClip.x - this.mGF.contSCROLL.x);
               this.expansionExecuteSelected(this.cursorClip.x - this.mGF.contSCROLL.x);
               this.removeCursor();
''','execute extras')

p.write_text(t,encoding='utf-8',newline='\n')
for needle in ['expansionUnits:Array','getQualifiedClassName','expansionInitUnits()','slot = i + 7','new PlayerUnit(this.mGF,this.bSys,clip','expansionForceMove(3500)','NUM >= 8 && NUM <= 13','expansionExecuteSelected']:
    if needle not in t: raise SystemExit('missing '+needle)
print('Expansion V3 real 12-unit battle controllers and second HUD row applied')
