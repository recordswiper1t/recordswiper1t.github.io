#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_equipment_slots_v3.py <exported-scripts-root>')
root=Path(sys.argv[1]); base=root/'scripts'/'Game'

def patch_ui():
    p=base/'Interface'/'WorldMapFormationAcc.as'; t=p.read_text(encoding='utf-8-sig')
    def one(old,new,label):
        nonlocal t
        n=t.count(old)
        if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
        t=t.replace(old,new,1)
    one('''   import flash.display.MovieClip;
   import flash.display.SimpleButton;
''','''   import flash.display.MovieClip;
   import flash.display.SimpleButton;
   import flash.display.Sprite;
''','acc Sprite import')
    one('''   import flash.text.TextField;
''','''   import flash.text.TextField;
   import flash.text.TextFormat;
''','acc TextFormat import')
    one('''      private var selectSlotID:int = 0;
''','''      private var selectSlotID:int = 0;
      
      private var equipSlotPage:int = 1;
      private var equipSlotButton:Sprite = null;
      private var equipSlotText:TextField = null;
''','acc page vars')
    one('''         this.equip1.addEventListener(MouseEvent.CLICK,this.equip1Click,false,0,true);
         this.slot1.addEventListener''','''         this.equip1.addEventListener(MouseEvent.CLICK,this.equip1Click,false,0,true);
         this.expansionInstallEquipSlotButton();
         this.slot1.addEventListener''','acc install page button')
    one('''         this.equip1.removeEventListener(MouseEvent.CLICK,this.equip1Click);
         this.slot1.removeEventListener''','''         this.equip1.removeEventListener(MouseEvent.CLICK,this.equip1Click);
         if(this.equipSlotButton != null)
         {
            this.equipSlotButton.removeEventListener(MouseEvent.CLICK,this.expansionEquipSlotClick);
            if(this.equipSlotButton.parent != null) this.equipSlotButton.parent.removeChild(this.equipSlotButton);
            this.equipSlotButton = null;
            this.equipSlotText = null;
         }
         this.slot1.removeEventListener''','acc destroy page button')
    one('''         var itemEquip:int = int(this.mGF.datMgr.unitGetValue(this.unitID,"item"));
''','''         var itemEquip:int = int(this.mGF.datMgr.unitGetValue(this.unitID,this.expansionEquipField()));
         this.expansionUpdateEquipSlotLabel();
''','acc current equip field')
    helpers='''      private function expansionEquipField() : String
      {
         if(this.equipSlotPage == 2) return "item2";
         if(this.equipSlotPage == 3) return "item3";
         return "item";
      }
      
      private function expansionInstallEquipSlotButton() : void
      {
         this.equipSlotButton = new Sprite();
         this.equipSlotButton.graphics.beginFill(1973790,0.94);
         this.equipSlotButton.graphics.lineStyle(1,6842472,1);
         this.equipSlotButton.graphics.drawRoundRect(0,0,176,28,8,8);
         this.equipSlotButton.graphics.endFill();
         this.equipSlotButton.x = 292;
         this.equipSlotButton.y = 65;
         this.equipSlotButton.buttonMode = true;
         this.equipSlotButton.addEventListener(MouseEvent.CLICK,this.expansionEquipSlotClick,false,0,true);
         this.equipSlotText = new TextField();
         this.equipSlotText.defaultTextFormat = new TextFormat("_sans",12,16777215,true,null,null,null,null,"center");
         this.equipSlotText.width = 172;
         this.equipSlotText.height = 24;
         this.equipSlotText.x = 2;
         this.equipSlotText.y = 4;
         this.equipSlotText.mouseEnabled = false;
         this.equipSlotText.selectable = false;
         this.equipSlotButton.addChild(this.equipSlotText);
         this.addChild(this.equipSlotButton);
         this.expansionUpdateEquipSlotLabel();
      }
      
      private function expansionEquipSlotClick(event:MouseEvent) : void
      {
         var unlocked:int = this.mGF.datMgr.expansionEquipmentSlotsUnlocked();
         this.equipSlotPage++;
         if(this.equipSlotPage > unlocked) this.equipSlotPage = 1;
         this.selectEquipNum = 0;
         this.selectEquipID = 0;
         this.selectSlotNum = 0;
         this.selectSlotID = 0;
         this.updateView();
      }
      
      private function expansionUpdateEquipSlotLabel() : void
      {
         if(this.equipSlotText == null) return;
         var unlocked:int = this.mGF.datMgr.expansionEquipmentSlotsUnlocked();
         if(this.equipSlotPage > unlocked) this.equipSlotPage = 1;
         this.equipSlotText.text = "Equipment slot " + this.equipSlotPage + " / " + unlocked;
      }
      
'''
    one('''      private function selectEQUIP(CLIP:*) : *
''',helpers+'''      private function selectEQUIP(CLIP:*) : *
''','acc page helpers')
    one('''         var itemEquip:int = int(this.mGF.datMgr.unitGetValue(this.unitID,"item"));
         this.selectEquipID = 0;
''','''         var itemEquip:int = int(this.mGF.datMgr.unitGetValue(this.unitID,this.expansionEquipField()));
         this.selectEquipID = 0;
''','acc select current field')
    one('''            itemEquip = int(this.mGF.datMgr.unitGetValue(this.unitID,"item"));
            if(itemEquip > 0)
            {
               this.mGF.datMgr.unitSetValue(this.unitID,"item",0);
''','''            itemEquip = int(this.mGF.datMgr.unitGetValue(this.unitID,this.expansionEquipField()));
            if(itemEquip > 0)
            {
               this.mGF.datMgr.unitSetValue(this.unitID,this.expansionEquipField(),0);
''','acc replace current item')
    one('''            this.mGF.datMgr.unitSetValue(this.unitID,"item",this.selectSlotID);
''','''            this.mGF.datMgr.unitSetValue(this.unitID,this.expansionEquipField(),this.selectSlotID);
''','acc equip selected item')
    one('''               this.mGF.datMgr.unitSetValue(this.unitID,"item",0);
               itemTotal = int(this.mGF.datMgr.itemGetValue(this.selectEquipID));
''','''               this.mGF.datMgr.unitSetValue(this.unitID,this.expansionEquipField(),0);
               itemTotal = int(this.mGF.datMgr.itemGetValue(this.selectEquipID));
''','acc remove current item')
    p.write_text(t,encoding='utf-8',newline='\n')
    for needle in ['equipSlotPage:int = 1','Equipment slot " + this.equipSlotPage','return "item2"','return "item3"','unitGetValue(this.unitID,this.expansionEquipField())']:
        if needle not in t: raise SystemExit('WorldMapFormationAcc missing '+needle)

def patch_stats():
    p=base/'System'/'StatDef'/'CharTotalStat.as'; t=p.read_text(encoding='utf-8-sig')
    def one(old,new,label):
        nonlocal t
        n=t.count(old)
        if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
        t=t.replace(old,new,1)
    one('''      public var unit_item_ability_id:int = 0;
''','''      public var unit_item_ability_id:int = 0;
      
      public var unit_item2_ability_id:int = 0;
      
      public var unit_item3_ability_id:int = 0;
''','item ability fields')
    one('''         var itemAbility:* = new CharAbilityStat(this.unit_item_ability_id);
''','''         var itemAbility:* = new CharAbilityStat(this.unit_item_ability_id);
         var itemAbility2:* = new CharAbilityStat(this.unit_item2_ability_id);
         var itemAbility3:* = new CharAbilityStat(this.unit_item3_ability_id);
''','item ability locals')
    # Numeric additive/multiplier stats.
    for prop in ['pop','health','health_boost','health_regen','attack','damage_mult','attack_building','defense_mult','speed']:
        old=' + itemAbility.'+prop
        new=old+' + itemAbility2.'+prop+' + itemAbility3.'+prop
        if old not in t: raise SystemExit('missing item numeric property '+prop)
        t=t.replace(old,new)
    # Elemental override priority: slot 1, then 2, then 3.
    one('''         if(itemAbility.attack_elemental != "")
         {
            this.attack_elemental = itemAbility.attack_elemental;
         }
''','''         if(itemAbility.attack_elemental != "") this.attack_elemental = itemAbility.attack_elemental;
         if(itemAbility2.attack_elemental != "") this.attack_elemental = itemAbility2.attack_elemental;
         if(itemAbility3.attack_elemental != "") this.attack_elemental = itemAbility3.attack_elemental;
''','item elemental overrides')
    for prop in ['resist_strike','resist_slash','resist_pierce']:
        old=f'''         if(itemAbility.{prop} != 0 && itemAbility.{prop} > this.{prop})
         {{
            this.{prop} = itemAbility.{prop};
         }}
'''
        new=f'''         if(itemAbility.{prop} != 0 && itemAbility.{prop} > this.{prop}) this.{prop} = itemAbility.{prop};
         if(itemAbility2.{prop} != 0 && itemAbility2.{prop} > this.{prop}) this.{prop} = itemAbility2.{prop};
         if(itemAbility3.{prop} != 0 && itemAbility3.{prop} > this.{prop}) this.{prop} = itemAbility3.{prop};
'''
        one(old,new,'item '+prop+' overrides')
    one('''         if(Boolean(itemAbility.resist_magic) && itemAbility.resist_magic > this.resist_magic)
         {
            this.resist_magic = itemAbility.resist_magic;
         }
''','''         if(Boolean(itemAbility.resist_magic) && itemAbility.resist_magic > this.resist_magic) this.resist_magic = itemAbility.resist_magic;
         if(Boolean(itemAbility2.resist_magic) && itemAbility2.resist_magic > this.resist_magic) this.resist_magic = itemAbility2.resist_magic;
         if(Boolean(itemAbility3.resist_magic) && itemAbility3.resist_magic > this.resist_magic) this.resist_magic = itemAbility3.resist_magic;
''','item magic resist overrides')
    one('''         this.unit_item_ability_id = 0;
         this.init(this.id);
''','''         this.unit_item_ability_id = 0;
         this.unit_item2_ability_id = 0;
         this.unit_item3_ability_id = 0;
         this.init(this.id);
''','nonplayer item reset')
    one('''         var item:* = new CharItemStat(dat.unitGetValue(this.id,"item"));
         this.unit_item_ability_id = item.ability_id;
         this.init(this.id);
''','''         var item:* = new CharItemStat(dat.unitGetValue(this.id,"item"));
         var item2:* = new CharItemStat(dat.unitGetValue(this.id,"item2"));
         var item3:* = new CharItemStat(dat.unitGetValue(this.id,"item3"));
         this.unit_item_ability_id = item.ability_id;
         this.unit_item2_ability_id = item2.ability_id;
         this.unit_item3_ability_id = item3.ability_id;
         this.init(this.id);
''','player triple items')
    p.write_text(t,encoding='utf-8',newline='\n')
    for needle in ['unit_item2_ability_id','unit_item3_ability_id','itemAbility2.health','itemAbility3.attack','unitGetValue(this.id,"item2")','unitGetValue(this.id,"item3")']:
        if needle not in t: raise SystemExit('CharTotalStat missing '+needle)

patch_ui(); patch_stats(); print('Expansion V3 progressive three-slot equipment system applied')
