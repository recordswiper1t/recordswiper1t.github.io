#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv)!=2: raise SystemExit('usage: patch_advanced_upgrades_v3.py <exported-scripts-root>')
root=Path(sys.argv[1]); base=root/'scripts'/'Game'

def patch_stats():
    p=base/'System'/'StatDef'/'CharTotalStat.as'; t=p.read_text(encoding='utf-8-sig')
    def one(old,new,label):
        nonlocal t
        n=t.count(old)
        if n!=1: raise SystemExit(f'{label}: expected 1 match, got {n}')
        t=t.replace(old,new,1)
    one('''      public var unit_ability9_id:int = 0;
''','''      public var unit_ability9_id:int = 0;
      
      public var unit_ability10_id:int = 0;
      public var unit_ability11_id:int = 0;
      public var unit_ability12_id:int = 0;
      public var unit_ability13_id:int = 0;
      public var unit_ability14_id:int = 0;
      public var unit_ability15_id:int = 0;
      public var unit_ability16_id:int = 0;
      public var unit_ability17_id:int = 0;
      public var unit_ability18_id:int = 0;
''','advanced ability fields')
    one('''         var ability9:* = new CharAbilityStat(this.unit_ability9_id);
         var itemAbility:* =''','''         var ability9:* = new CharAbilityStat(this.unit_ability9_id);
         var ability10:* = new CharAbilityStat(this.unit_ability10_id);
         var ability11:* = new CharAbilityStat(this.unit_ability11_id);
         var ability12:* = new CharAbilityStat(this.unit_ability12_id);
         var ability13:* = new CharAbilityStat(this.unit_ability13_id);
         var ability14:* = new CharAbilityStat(this.unit_ability14_id);
         var ability15:* = new CharAbilityStat(this.unit_ability15_id);
         var ability16:* = new CharAbilityStat(this.unit_ability16_id);
         var ability17:* = new CharAbilityStat(this.unit_ability17_id);
         var ability18:* = new CharAbilityStat(this.unit_ability18_id);
         var itemAbility:* =''','advanced ability locals')
    # Equipment patch already runs before this script, so extend the nine-ability
    # arithmetic immediately before itemAbility for every numeric stat.
    for prop in ['pop','health','health_boost','health_regen','attack','damage_mult','attack_building','defense_mult','speed']:
        old=f' + ability9.{prop} + itemAbility.{prop}'
        ext=''.join(f' + ability{i}.{prop}' for i in range(10,19))
        new=f' + ability9.{prop}'+ext+f' + itemAbility.{prop}'
        if old not in t: raise SystemExit('advanced numeric anchor missing '+prop)
        t=t.replace(old,new)
    # Advanced elemental effects take priority after original abilities, before gear.
    anchor='''         if(ability9.attack_elemental != "")
         {
            this.attack_elemental = ability9.attack_elemental;
         }
'''
    extra=''.join(f'''         if(ability{i}.attack_elemental != "") this.attack_elemental = ability{i}.attack_elemental;\n''' for i in range(10,19))
    one(anchor,anchor+extra,'advanced elemental')
    # Resistances use strongest value. Insert after ability9 for each type.
    for prop in ['resist_strike','resist_slash','resist_pierce']:
        anchor=f'''         if(ability9.{prop} != 0 && ability9.{prop} > this.{prop})
         {{
            this.{prop} = ability9.{prop};
         }}
'''
        extra=''.join(f'''         if(ability{i}.{prop} != 0 && ability{i}.{prop} > this.{prop}) this.{prop} = ability{i}.{prop};\n''' for i in range(10,19))
        one(anchor,anchor+extra,'advanced '+prop)
    anchor='''         if(Boolean(ability9.resist_magic) && ability9.resist_magic > this.resist_magic)
         {
            this.resist_magic = ability9.resist_magic;
         }
'''
    extra=''.join(f'''         if(Boolean(ability{i}.resist_magic) && ability{i}.resist_magic > this.resist_magic) this.resist_magic = ability{i}.resist_magic;\n''' for i in range(10,19))
    one(anchor,anchor+extra,'advanced magic resistance')
    # Assign any spell/build advanced nodes into the existing four-spell tray.
    one('''         this.assignSpell(ability9.id);
''','''         this.assignSpell(ability9.id);
         this.assignSpell(ability10.id);
         this.assignSpell(ability11.id);
         this.assignSpell(ability12.id);
         this.assignSpell(ability13.id);
         this.assignSpell(ability14.id);
         this.assignSpell(ability15.id);
         this.assignSpell(ability16.id);
         this.assignSpell(ability17.id);
         this.assignSpell(ability18.id);
''','advanced spell assignment')

    # Advanced trees reuse stable existing ability IDs (and therefore existing
    # icons/timeline frames) but in new role-specific combinations.
    helper=r'''      private function expansionAdvancedTree() : Array
      {
         switch(this.id)
         {
            case 1: return [20,15,25,35,36,37,38,39,43];
            case 2: return [20,15,25,39,36,37,29,38,35];
            case 3: return [20,15,25,40,36,37,38,39,42];
            case 10: return [20,15,47,20,15,47,37,48,25];
            case 11: return [15,25,47,15,25,48,26,38,39];
            case 12: return [20,15,47,20,37,48,28,39,20];
            case 13: return [20,15,46,20,29,39,37,38,35];
            case 14: return [20,15,47,20,15,48,37,26,35];
            case 15: return [15,25,47,15,25,48,37,38,36];
            case 16: return [20,15,47,20,37,48,28,39,35];
            case 17: return [20,15,46,20,29,39,37,38,34];
            case 18: return [20,15,47,20,39,48,37,26,35];
            case 19: return [20,15,47,25,38,48,26,35,36];
            case 20: return [20,15,47,20,37,48,40,39,25];
            case 21: return [20,15,46,20,30,37,39,35,38];
            case 22: return [15,25,47,15,25,48,39,36,38];
            case 23: return [20,15,47,20,25,48,37,35,39];
            case 24: return [20,15,47,20,37,48,34,35,38];
            case 25: return [20,15,47,20,42,48,37,35,25];
            case 26: return [20,20,47,42,40,48,37,35,15];
            case 27: return [20,15,47,20,25,48,37,35,39];
            case 28: return [15,25,46,15,25,47,36,38,39];
            case 50: return [20,15,25,35,36,37,38,39,35];
            case 51: return [15,15,25,36,38,39,25,15,36];
            case 52: return [20,15,25,40,38,37,39,35,40];
            case 53: return [20,15,25,37,40,38,39,35,20];
            case 54: return [20,15,25,30,37,39,35,38,20];
            case 55: return [20,15,25,38,39,37,35,36,20];
            case 56: return [20,15,25,42,36,38,35,39,25];
            case 57: return [20,15,25,35,36,39,38,37,20];
            case 58: return [20,15,25,33,40,38,39,35,20];
            case 59: return [20,15,25,30,40,37,35,39,20];
            case 60: return [20,15,25,40,35,36,38,39,42];
         }
         return [20,15,25,35,36,37,38,39,20];
      }
      
      private function expansionAdvancedAbility(SLOT:int) : int
      {
         var tree:Array = this.expansionAdvancedTree();
         var index:int = SLOT - 10;
         if(index >= 0 && index < tree.length) return int(tree[index]);
         return 0;
      }
      
'''
    one('''      public function unlockAbility() : *
''',helper+'''      public function unlockAbility() : *
''','advanced tree helper')
    one('''         this.unit_ability9_id = ability9.id;
         this.unit_item_ability_id = 0;
''','''         this.unit_ability9_id = ability9.id;
         this.unit_ability10_id = this.expansionAdvancedAbility(10);
         this.unit_ability11_id = this.expansionAdvancedAbility(11);
         this.unit_ability12_id = this.expansionAdvancedAbility(12);
         this.unit_ability13_id = this.expansionAdvancedAbility(13);
         this.unit_ability14_id = this.expansionAdvancedAbility(14);
         this.unit_ability15_id = this.expansionAdvancedAbility(15);
         this.unit_ability16_id = this.expansionAdvancedAbility(16);
         this.unit_ability17_id = this.expansionAdvancedAbility(17);
         this.unit_ability18_id = this.expansionAdvancedAbility(18);
         this.unit_item_ability_id = 0;
''','advanced potential IDs')
    one('''         this.unit_ability9_id = dat.unitGetValue(this.id,"ability9");
         var item:* =''','''         this.unit_ability9_id = dat.unitGetValue(this.id,"ability9");
         this.unit_ability10_id = dat.unitGetValue(this.id,"ability10");
         this.unit_ability11_id = dat.unitGetValue(this.id,"ability11");
         this.unit_ability12_id = dat.unitGetValue(this.id,"ability12");
         this.unit_ability13_id = dat.unitGetValue(this.id,"ability13");
         this.unit_ability14_id = dat.unitGetValue(this.id,"ability14");
         this.unit_ability15_id = dat.unitGetValue(this.id,"ability15");
         this.unit_ability16_id = dat.unitGetValue(this.id,"ability16");
         this.unit_ability17_id = dat.unitGetValue(this.id,"ability17");
         this.unit_ability18_id = dat.unitGetValue(this.id,"ability18");
         var item:* =''','advanced player IDs')

    # getTotalHP / getTotalATK are used by equipment preview; extend them too.
    for method_prop in ['health','damage_mult']:
        pass
    # Add locals to each preview function by replacing its ability9 declaration twice.
    decl='''         var ability9:* = new CharAbilityStat(this.unit_ability9_id);
'''
    ext=decl+''.join(f'''         var ability{i}:* = new CharAbilityStat(this.unit_ability{i}_id);\n''' for i in range(10,19))
    if t.count(decl) < 2: raise SystemExit('preview ability9 declarations missing')
    # The first declaration belongs to init and was already replaced, so only two remain here.
    t=t.replace(decl,ext,2)
    for prop in ['health','health_boost','attack','damage_mult']:
        old=f' + ability9.{prop}'
        ext_expr=''.join(f' + ability{i}.{prop}' for i in range(10,19))
        # Replace only preview expressions that are not already extended in init.
        marker=old+ext_expr
        # init already contains marker; remaining plain occurrences are previews.
        while old in t and marker not in t[t.find(old):t.find(old)+len(marker)+4]:
            idx=t.find(old)
            t=t[:idx]+marker+t[idx+len(old):]
            # stop once expected preview properties are handled by total count naturally
            if t.count(old)==0: break
    p.write_text(t,encoding='utf-8',newline='\n')
    for n in ['unit_ability18_id','expansionAdvancedTree','case 60: return','assignSpell(ability18.id)','unitGetValue(this.id,"ability18")']:
        if n not in t: raise SystemExit('CharTotalStat missing '+n)

def patch_ui():
    p=base/'Interface'/'WorldMapFormationSkill.as'; t=p.read_text(encoding='utf-8-sig')
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
''','skill Sprite import')
    one('''   import flash.text.TextField;
''','''   import flash.text.TextField;
   import flash.text.TextFormat;
''','skill TextFormat import')
    one('''      private var skillID9:int = 0;
''','''      private var skillID9:int = 0;
      
      private var skillPage:int = 1;
      private var skillPageButton:Sprite = null;
      private var skillPageText:TextField = null;
''','skill page vars')
    one('''         this.skill9.addEventListener(MouseEvent.CLICK,this.skill9Click,false,0,true);
         this.unitID =''','''         this.skill9.addEventListener(MouseEvent.CLICK,this.skill9Click,false,0,true);
         this.expansionInstallSkillPageButton();
         this.unitID =''','skill page install')
    one('''         this.skill9.removeEventListener(MouseEvent.CLICK,this.skill9Click);
         this.dispCont.removeChild(this);
''','''         this.skill9.removeEventListener(MouseEvent.CLICK,this.skill9Click);
         if(this.skillPageButton != null)
         {
            this.skillPageButton.removeEventListener(MouseEvent.CLICK,this.expansionSkillPageClick);
            if(this.skillPageButton.parent != null) this.skillPageButton.parent.removeChild(this.skillPageButton);
            this.skillPageButton = null;
            this.skillPageText = null;
         }
         this.dispCont.removeChild(this);
''','skill page destroy')
    # Nine physical skill clips point at either 1..9 or 10..18.
    old=''.join(f'         this.skillSlotParsing(this.skill{i},this.selectSlotNum,{i});\n' for i in range(1,10))
    new='''         var skillStart:int = (this.skillPage - 1) * 9;
'''+''.join(f'         this.skillSlotParsing(this.skill{i},this.selectSlotNum,skillStart + {i});\n' for i in range(1,10))+'''         this.expansionUpdateSkillPageLabel();
'''
    one(old,new,'paged skill slots')
    # Replace selected saved ability lookup chain with generic field name.
    start=t.index('         var unitSkillUnlock:int = 0;\n')
    end=t.index('         if(this.selectSlotNum > 0 && unitSkillUnlock == 0)\n',start)
    t=t[:start]+'''         var unitSkillUnlock:int = 0;
         if(this.selectSlotNum > 0) unitSkillUnlock = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability" + this.selectSlotNum));
'''+t[end:]
    # Replace skillSlotParsing with generic 18-slot parent graph.
    start=t.index('      private function skillSlotParsing(')
    end=t.index('      public function selectSLOT(',start)
    t=t[:start]+r'''      private function skillSlotParsing(CLIP:*, SELECT_NUM:int = 0, MATCH_NUM:int = 0) : *
      {
         CLIP.icon.visible = false;
         CLIP.select.visible = false;
         CLIP.icon.alpha = 1;
         CLIP.cost.htmlText = String("");
         CLIP.buttonMode = false;
         if(MATCH_NUM >= 10 && this.mGF.datMgr.expansionContentCleared() < 10) return;
         var statCHR:* = new CharTotalStat(this.unitID);
         statCHR.unlockAbility();
         var unitSkillUnlock:int = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability" + MATCH_NUM));
         var unitSkillUnlockParent:int = 0;
         var unitSkillID:int = int(statCHR["unit_ability" + MATCH_NUM + "_id"]);
         if(MATCH_NUM == 1 || MATCH_NUM == 4 || MATCH_NUM == 7) unitSkillUnlockParent = 999;
         else if(MATCH_NUM == 2) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability1"));
         else if(MATCH_NUM == 3) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability2"));
         else if(MATCH_NUM == 5) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability4"));
         else if(MATCH_NUM == 6) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability5"));
         else if(MATCH_NUM == 8) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability7"));
         else if(MATCH_NUM == 9) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability8"));
         else if(MATCH_NUM == 10) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability3"));
         else if(MATCH_NUM == 11) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability10"));
         else if(MATCH_NUM == 12) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability11"));
         else if(MATCH_NUM == 13) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability6"));
         else if(MATCH_NUM == 14) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability13"));
         else if(MATCH_NUM == 15) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability14"));
         else if(MATCH_NUM == 16) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability9"));
         else if(MATCH_NUM == 17) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability16"));
         else if(MATCH_NUM == 18) unitSkillUnlockParent = int(this.mGF.datMgr.unitGetValue(this.unitID,"ability17"));
         var statABL:* = new CharAbilityStat(unitSkillID);
         var cost:int = statABL.rank * (MATCH_NUM >= 10 ? 45 : 15);
         if(unitSkillUnlock > 0)
         {
            CLIP.icon.gotoAndStop(unitSkillID);
            CLIP.cost.htmlText = String("MAX");
            CLIP.icon.visible = true;
            CLIP.buttonMode = true;
         }
         else if(unitSkillUnlockParent > 0 && unitSkillID > 0)
         {
            CLIP.icon.gotoAndStop(unitSkillID);
            CLIP.cost.htmlText = String(cost);
            CLIP.icon.visible = true;
            CLIP.icon.alpha = 0.5;
            CLIP.buttonMode = true;
         }
         if(SELECT_NUM == MATCH_NUM && CLIP.icon.visible) CLIP.select.visible = true;
      }
      
'''+t[end:]
    helpers=r'''      private function expansionInstallSkillPageButton() : void
      {
         this.skillPageButton = new Sprite();
         this.skillPageButton.graphics.beginFill(1973790,0.94);
         this.skillPageButton.graphics.lineStyle(1,6842472,1);
         this.skillPageButton.graphics.drawRoundRect(0,0,184,28,8,8);
         this.skillPageButton.graphics.endFill();
         this.skillPageButton.x = 540;
         this.skillPageButton.y = 44;
         this.skillPageButton.buttonMode = true;
         this.skillPageButton.addEventListener(MouseEvent.CLICK,this.expansionSkillPageClick,false,0,true);
         this.skillPageText = new TextField();
         this.skillPageText.defaultTextFormat = new TextFormat("_sans",12,16777215,true,null,null,null,null,"center");
         this.skillPageText.width=180; this.skillPageText.height=24; this.skillPageText.x=2; this.skillPageText.y=4;
         this.skillPageText.mouseEnabled=false; this.skillPageText.selectable=false;
         this.skillPageButton.addChild(this.skillPageText); this.addChild(this.skillPageButton);
         this.expansionUpdateSkillPageLabel();
      }
      
      private function expansionSkillPageClick(event:MouseEvent) : void
      {
         if(this.skillPage == 1 && this.mGF.datMgr.expansionContentCleared() < 10)
         {
            this.mGF.utilMgr.messagePop("advanced upgrades unlock after 10 cleared battles !");
            return;
         }
         this.skillPage = this.skillPage == 1 ? 2 : 1;
         this.selectSlotNum=0; this.selectSlotID=0; this.updateView();
      }
      
      private function expansionUpdateSkillPageLabel() : void
      {
         if(this.skillPageText == null) return;
         if(this.skillPage == 1)
         {
            this.skillPageText.text = this.mGF.datMgr.expansionContentCleared() >= 10 ? "Original upgrades  •  Advanced >" : "Advanced locked: 10 clears";
         }
         else this.skillPageText.text = "< Original  •  Advanced upgrades";
      }
      
'''
    one('''      public function selectSLOT(CLIP:*, NUM:int = 0) : *
''',helpers+'''      public function selectSLOT(CLIP:*, NUM:int = 0) : *
''','skill page helpers')
    # Generic learn path for slots 1..18, with advanced cost multiplier.
    start=t.index('      private function learnClick(event:MouseEvent) : void\n')
    end=t.index('      private function skill1Click(event:MouseEvent) : void\n',start)
    t=t[:start]+r'''      private function learnClick(event:MouseEvent) : void
      {
         if(this.selectSlotNum > 0)
         {
            var unitExp:int = int(this.mGF.datMgr.unitGetValue(this.unitID,"exp"));
            var stat:* = new CharAbilityStat(this.selectSlotID);
            var costExp:int = stat.rank * (this.selectSlotNum >= 10 ? 45 : 15);
            if(unitExp >= costExp)
            {
               this.mGF.datMgr.unitSetValue(this.unitID,"ability" + this.selectSlotNum,this.selectSlotID);
               this.mGF.datMgr.unitSetValue(this.unitID,"exp",Math.max(unitExp - costExp,0));
               this.selectSlotNum=0; this.selectSlotID=0;
            }
            else this.mGF.utilMgr.messagePop("not enough exp!");
            this.updateView();
         }
      }
      
'''+t[end:]
    # Physical clicks select current page's real slot number.
    for i in range(1,10):
        old=f'''      private function skill{i}Click(event:MouseEvent) : void\n      {{\n         this.selectSLOT(this.skill{i},{i});\n      }}\n'''
        new=f'''      private function skill{i}Click(event:MouseEvent) : void\n      {{\n         this.selectSLOT(this.skill{i},(this.skillPage - 1) * 9 + {i});\n      }}\n'''
        one(old,new,f'skill{i} paged click')
    p.write_text(t,encoding='utf-8',newline='\n')
    for n in ['skillPage:int = 1','Advanced locked: 10 clears','MATCH_NUM == 18','ability" + this.selectSlotNum','* (this.selectSlotNum >= 10 ? 45 : 15)']:
        if n not in t: raise SystemExit('WorldMapFormationSkill missing '+n)

patch_stats(); patch_ui(); print('Expansion V3 nine advanced upgrades per unit/hero applied')
