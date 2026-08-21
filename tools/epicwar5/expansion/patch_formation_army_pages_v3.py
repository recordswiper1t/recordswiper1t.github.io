#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_formation_army_pages_v3.py <exported-scripts-root>')
root=Path(sys.argv[1]); base=root/'scripts'/'Game'
fp=base/'Interface'/'WorldMapFormation.as'; t=fp.read_text(encoding='utf-8-sig')

def one(old,new,label):
    global t
    n=t.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    t=t.replace(old,new,1)

# Allow clearing a now-locked slot during migration/cleanup.
dp=base/'Manager'/'DataManager.as'; d=dp.read_text(encoding='utf-8-sig')
old='         if(SLOT < 1 || SLOT > this.expansionArmySlotsUnlocked()) return;\n'
new='         if(SLOT < 1 || SLOT > 12) return;\n         if(ID > 0 && SLOT > this.expansionArmySlotsUnlocked()) return;\n'
if d.count(old)!=1: raise SystemExit('DataManager expansionSetUnitEquip guard not found')
d=d.replace(old,new,1); dp.write_text(d,encoding='utf-8',newline='\n')

one('''   import flash.display.MovieClip;
   import flash.display.SimpleButton;
''','''   import flash.display.MovieClip;
   import flash.display.SimpleButton;
   import flash.display.Sprite;
''','Sprite import')
one('''   import flash.text.TextField;
''','''   import flash.text.TextField;
   import flash.text.TextFormat;
''','TextFormat import')
one('''      private var pageNum:int = 1;
''','''      private var pageNum:int = 1;
      
      private var equipPage:int = 1;
      
      private var armyPageButton:Sprite = null;
      
      private var armyPageText:TextField = null;
''','army page vars')

one('''         this.equip6.addEventListener(MouseEvent.CLICK,this.equip6Click,false,0,true);
         this.slot1.addEventListener''','''         this.equip6.addEventListener(MouseEvent.CLICK,this.equip6Click,false,0,true);
         this.expansionInstallArmyPageButton();
         this.slot1.addEventListener''','install army page button')

one('''         this.equip6.removeEventListener(MouseEvent.CLICK,this.equip6Click);
         this.slot1.removeEventListener''','''         this.equip6.removeEventListener(MouseEvent.CLICK,this.equip6Click);
         if(this.armyPageButton != null)
         {
            this.armyPageButton.removeEventListener(MouseEvent.CLICK,this.expansionArmyPageClick);
            if(this.armyPageButton.parent != null) this.armyPageButton.parent.removeChild(this.armyPageButton);
            this.armyPageButton = null;
            this.armyPageText = null;
         }
         this.slot1.removeEventListener''','destroy army page button')

old_top='''         this.unitEquipParsing(this.hero,this.mGF.datMgr.hero_select_id,this.selectEquipNum,99);
         this.unitEquipParsing(this.equip1,this.mGF.datMgr.unit_equip1_id,this.selectEquipNum,1);
         this.unitEquipParsing(this.equip2,this.mGF.datMgr.unit_equip2_id,this.selectEquipNum,2);
         this.unitEquipParsing(this.equip3,this.mGF.datMgr.unit_equip3_id,this.selectEquipNum,3);
         this.unitEquipParsing(this.equip4,this.mGF.datMgr.unit_equip4_id,this.selectEquipNum,4);
         this.unitEquipParsing(this.equip5,this.mGF.datMgr.unit_equip5_id,this.selectEquipNum,5);
         this.unitEquipParsing(this.equip6,this.mGF.datMgr.unit_equip6_id,this.selectEquipNum,6);
'''
new_top='''         this.unitEquipParsing(this.hero,this.mGF.datMgr.hero_select_id,this.selectEquipNum,99);
         var armyStart:int = (this.equipPage - 1) * 6;
         this.unitEquipParsing(this.equip1,this.mGF.datMgr.expansionGetUnitEquip(armyStart + 1),this.selectEquipNum,armyStart + 1);
         this.unitEquipParsing(this.equip2,this.mGF.datMgr.expansionGetUnitEquip(armyStart + 2),this.selectEquipNum,armyStart + 2);
         this.unitEquipParsing(this.equip3,this.mGF.datMgr.expansionGetUnitEquip(armyStart + 3),this.selectEquipNum,armyStart + 3);
         this.unitEquipParsing(this.equip4,this.mGF.datMgr.expansionGetUnitEquip(armyStart + 4),this.selectEquipNum,armyStart + 4);
         this.unitEquipParsing(this.equip5,this.mGF.datMgr.expansionGetUnitEquip(armyStart + 5),this.selectEquipNum,armyStart + 5);
         this.unitEquipParsing(this.equip6,this.mGF.datMgr.expansionGetUnitEquip(armyStart + 6),this.selectEquipNum,armyStart + 6);
         this.expansionUpdateArmyPageLabel();
'''
one(old_top,new_top,'paged equipped slots')

# Locked army sockets stay visible but dim and noninteractive.
one('''         CLIP.item.visible = false;
         if(ID > 0)
''','''         CLIP.item.visible = false;
         CLIP.learn.visible = false;
         CLIP.alpha = 1;
         if(MATCH_NUM >= 1 && MATCH_NUM <= 12 && MATCH_NUM > this.mGF.datMgr.expansionArmySlotsUnlocked())
         {
            CLIP.alpha = 0.25;
            return;
         }
         if(ID > 0)
''','locked equipped slots')
one('''         CLIP.learn.visible = false;
         if(this.testSurplusExp(ID))
''','''         if(this.testSurplusExp(ID))
''','dedupe learn visibility')

helpers='''      private function expansionInstallArmyPageButton() : void
      {
         this.armyPageButton = new Sprite();
         this.armyPageButton.graphics.beginFill(1973790,0.94);
         this.armyPageButton.graphics.lineStyle(1,6842472,1);
         this.armyPageButton.graphics.drawRoundRect(0,0,178,28,8,8);
         this.armyPageButton.graphics.endFill();
         this.armyPageButton.x = 548;
         this.armyPageButton.y = 38;
         this.armyPageButton.buttonMode = true;
         this.armyPageButton.addEventListener(MouseEvent.CLICK,this.expansionArmyPageClick,false,0,true);
         this.armyPageText = new TextField();
         this.armyPageText.defaultTextFormat = new TextFormat("_sans",12,16777215,true,null,null,null,null,"center");
         this.armyPageText.width = 174;
         this.armyPageText.height = 24;
         this.armyPageText.x = 2;
         this.armyPageText.y = 4;
         this.armyPageText.mouseEnabled = false;
         this.armyPageText.selectable = false;
         this.armyPageButton.addChild(this.armyPageText);
         this.addChild(this.armyPageButton);
         this.expansionUpdateArmyPageLabel();
      }
      
      private function expansionArmyPageClick(event:MouseEvent) : void
      {
         this.equipPage = this.equipPage == 1 ? 2 : 1;
         this.selectEquipNum = 0;
         this.selectEquipID = 0;
         this.updateView();
      }
      
      private function expansionUpdateArmyPageLabel() : void
      {
         if(this.armyPageText == null) return;
         var lo:int = this.equipPage == 1 ? 1 : 7;
         var hi:int = this.equipPage == 1 ? 6 : 12;
         this.armyPageText.text = "Army " + lo + "-" + hi + "  •  " + this.mGF.datMgr.expansionArmySlotsUnlocked() + "/12 unlocked";
      }
      
'''
one('      private function selectEQUIP(CLIP:*, NUM:int = 0) : *\n',helpers+'      private function selectEQUIP(CLIP:*, NUM:int = 0) : *\n','army page helpers')

old_select='''         var unitEquip:int = 0;
         if(NUM == 1)
         {
            unitEquip = int(this.mGF.datMgr.unit_equip1_id);
         }
         else if(NUM == 2)
         {
            unitEquip = int(this.mGF.datMgr.unit_equip2_id);
         }
         else if(NUM == 3)
         {
            unitEquip = int(this.mGF.datMgr.unit_equip3_id);
         }
         else if(NUM == 4)
         {
            unitEquip = int(this.mGF.datMgr.unit_equip4_id);
         }
         else if(NUM == 5)
         {
            unitEquip = int(this.mGF.datMgr.unit_equip5_id);
         }
         else if(NUM == 6)
         {
            unitEquip = int(this.mGF.datMgr.unit_equip6_id);
         }
         else if(NUM == 99)
         {
            unitEquip = int(this.mGF.datMgr.hero_select_id);
         }
'''
new_select='''         var unitEquip:int = 0;
         if(NUM >= 1 && NUM <= 12)
         {
            if(NUM <= this.mGF.datMgr.expansionArmySlotsUnlocked()) unitEquip = int(this.mGF.datMgr.expansionGetUnitEquip(NUM));
         }
         else if(NUM == 99)
         {
            unitEquip = int(this.mGF.datMgr.hero_select_id);
         }
'''
one(old_select,new_select,'generic equip selection')

# Equip into the first open unlocked army slot.
start=t.index('      private function equipClick(event:MouseEvent) : void\n')
end=t.index('      private function removeClick(event:MouseEvent) : void\n',start)
t=t[:start]+'''      private function equipClick(event:MouseEvent) : void
      {
         if(this.selectSlotNum > 0)
         {
            var i:int = 0;
            var placed:Boolean = false;
            var unlocked:int = this.mGF.datMgr.expansionArmySlotsUnlocked();
            for(i = 1; i <= unlocked; i++)
            {
               if(this.mGF.datMgr.expansionGetUnitEquip(i) == 0)
               {
                  this.mGF.datMgr.expansionSetUnitEquip(i,this.selectSlotID);
                  this.mGF.datMgr.unitSetValue(this.selectSlotID,"stat",2);
                  this.selectSlotNum = 0;
                  this.selectSlotID = 0;
                  placed = true;
                  if(i > 6) this.equipPage = 2;
                  break;
               }
            }
            if(!placed) this.mGF.utilMgr.messagePop("no unlocked army slot available !");
         }
         this.updateView();
      }
      
'''+t[end:]

# Generic removal works for all twelve positions.
start=t.index('      private function removeClick(event:MouseEvent) : void\n')
end=t.index('      private function heroClick(event:MouseEvent) : void\n',start)
t=t[:start]+'''      private function removeClick(event:MouseEvent) : void
      {
         if(this.selectEquipID > 0 && this.selectEquipNum >= 1 && this.selectEquipNum <= 12)
         {
            this.mGF.datMgr.expansionSetUnitEquip(this.selectEquipNum,0);
            this.mGF.datMgr.unitSetValue(this.selectEquipID,"stat",1);
            this.selectEquipNum = 0;
            this.selectEquipID = 0;
         }
         else
         {
            this.mGF.utilMgr.messagePop("empty slot !");
         }
         this.updateView();
      }
      
'''+t[end:]

# Six physical clips select the six positions on the current army page.
for local in range(1,7):
    old=f'''      private function equip{local}Click(event:MouseEvent) : void\n      {{\n         this.selectEQUIP(this.equip{local},{local});\n      }}\n'''
    new=f'''      private function equip{local}Click(event:MouseEvent) : void\n      {{\n         this.selectEQUIP(this.equip{local},(this.equipPage - 1) * 6 + {local});\n      }}\n'''
    one(old,new,f'equip{local} paged click')

fp.write_text(t,encoding='utf-8',newline='\n')
for needle in ['equipPage:int = 1','Army " + lo + "-" + hi','expansionArmySlotsUnlocked()','expansionGetUnitEquip(armyStart + 6)','no unlocked army slot available']:
    if needle not in t: raise SystemExit('missing '+needle)
print('Expansion V3 paged 12-slot formation UI applied')
