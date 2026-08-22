#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: patch_expansion_campaign_v3.py <exported-scripts-root>')
root = Path(sys.argv[1]); base = root/'scripts'/'Game'


def once(text, old, new, label):
    n=text.count(old)
    if n != 1: raise SystemExit(f'{label}: expected 1 match, got {n}')
    return text.replace(old,new,1)

# ------------------------------------------------------------------
# BattleControlEnemy: add 25 real battle inputs (101..125). Each new level
# has a distinct boss/minion/theme/reward combination and scales aggressively.
# ------------------------------------------------------------------
p=base/'System'/'Battle'/'BattleControlEnemy.as'; t=p.read_text(encoding='utf-8-sig')
switch_cases=''
for i in range(1,26):
    switch_cases += f'''            case {100+i}:\n               this.initExpansion({i});\n               break;\n'''
t=once(t,
'''            case 55:
               this.initTrial5();
               break;
            default:
''',
'''            case 55:
               this.initTrial5();
               break;
'''+switch_cases+'''            default:
''','expansion battle switch')

helper=r'''      public function initExpansion(ID:int) : *
      {
         var themes:Array = ["forest","ruin","sand","ice","village","lava"];
         var bosses:Array = ["troll","witch","vampire","anubis","golem","beastrider","centaurion","lamia","lich","tiger","phoenix","valkyrie","diablos","dragon","devil","angelevil","gaia","baal","tigerevil","wizard","golem","dragon","diablos","baal","devil"];
         var elites:Array = ["goblinred","goblingreen","goblinblue","goblinyellow","goblinpink","taurus","gorila","beastrider","succubus","lich","phoenix","angel","dwarf","witch","vampire","anubis","centaurion","lamia","tiger","valkyrie","gaia","dragon","devil","diablos","baal"];
         var elites2:Array = ["troll","bomber","imp","goblinred","goblinblue","centaurion","taurus","vampire","witch","anubis","beastrider","lamia","golem","lich","tiger","phoenix","valkyrie","gaia","diablos","dragon","devil","angelevil","baal","tigerevil","wizard"];
         var elements:Array = ["","poison","ice","thunder","dark","fire"];
         var waveNames:Array = ["peon","goblin","archer","warrior","mystic","bomber","brute","giant"];
         var rewardNames:Array = ["exp_vanguard","exp_bastion","exp_windstep","exp_bloodsigil","exp_titanbelt","exp_arcaneguard","exp_spearbreaker","exp_bladebreaker","exp_hammerbreaker","exp_phoenixcore","exp_hellfire","exp_frostbite","exp_stormcrown","exp_venomfang","exp_abysslens","exp_siegegauntlet","exp_warlord","exp_colossus","exp_duelist","exp_paladin","exp_sorcerer","exp_beasttotem","exp_guardianhalo","exp_berserkercrown","exp_artlogicprime"];
         var index:int = Math.max(1,Math.min(25,ID)) - 1;
         var tier:int = index + 1;
         var bossHP:int = 120000 + tier * 30000 + tier * tier * 900;
         var bossATK:int = 950 + tier * 245;
         var eliteHP:int = 18000 + tier * 6200;
         var eliteATK:int = 320 + tier * 115;
         var portalHP:int = 22000 + tier * 8000;
         var length:int = Math.min(4400,2800 + tier * 65);
         var theme:String = String(themes[index % themes.length]);
         var element:String = String(elements[index % elements.length]);
         this.bSys.battle_stage = 25 + tier;
         this.bSys.bgMgr.setupBackground(theme,index % 4);
         this.bSys.bgMgr.setLengthArea(length);
         this.bSys.charMgr.createEnemyUnit("boss",String(bosses[index]),length - 220,0,50,bossHP,bossATK,element,1 + tier * 0.012);
         this.bSys.charMgr.createEnemyUnit("unit",String(elites[index]),length - 520,0,50,eliteHP,eliteATK,element,1 + tier * 0.008);
         this.bSys.charMgr.createEnemyUnit("unit",String(elites2[index]),length - 680,0,50,int(eliteHP * 0.8),int(eliteATK * 0.9),"",1 + tier * 0.006);
         this.bSys.charMgr.createEnemyUnit("object",tier % 2 == 0 ? "wall2" : "wall",length - 940,0,50,portalHP);
         this.bSys.charMgr.createEnemyPortal(tier % 3 == 0 ? "portalhell" : (tier % 2 == 0 ? "portalwarp" : "portal"),length - 1250,53,portalHP,0,String(waveNames[index % waveNames.length]),Math.min(5,2 + int(tier / 6)));
         if(tier >= 8)
         {
            this.bSys.charMgr.createEnemyPortal("portal2",length - 1900,53,int(portalHP * 0.8),0,String(waveNames[(index + 3) % waveNames.length]),Math.min(5,2 + int(tier / 5)));
         }
         if(tier >= 16)
         {
            this.bSys.charMgr.createEnemyUnit("boss",String(bosses[(index + 7) % bosses.length]),length - 1100,0,50,int(bossHP * 0.48),int(bossATK * 0.72),String(elements[(index + 2) % elements.length]),0.85 + tier * 0.006);
         }
         this.eWave.init(String(waveNames[index % waveNames.length]),Math.min(5,2 + int(tier / 5)),Math.max(1,5 - int(tier / 7)));
         this.eWave2.init(String(waveNames[(index + 2) % waveNames.length]),Math.min(5,2 + int(tier / 4)),Math.max(1,7 - int(tier / 5)));
         this.eWave3.init(String(waveNames[(index + 5) % waveNames.length]),Math.min(5,3 + int(tier / 6)),Math.max(2,12 - int(tier / 3)));
         this.bSys.battle_exp_reward = 120 + tier * 14;
         this.bSys.battle_unit_reward = "";
         this.bSys.battle_item_reward = String(rewardNames[index]);
         if(tier % 3 == 0) this.mGF.soundMgr.playBgmBattle3();
         else if(tier % 2 == 0) this.mGF.soundMgr.playBgmBattle2();
         else this.mGF.soundMgr.playBgmBattle1();
         if(tier >= 20) this.bSys.x_fog = length;
         trace("EXPANSION LEVEL " + tier + " start .... ");
      }
      
'''
t=once(t,'      public function update() : *\n',helper+'      public function update() : *\n','expansion battle initializer')
p.write_text(t,encoding='utf-8',newline='\n')

# ------------------------------------------------------------------
# BattleResult: record expansion clears in the 25-value expansion bank.
# ------------------------------------------------------------------
p=base/'Interface'/'BattleResult.as'; t=p.read_text(encoding='utf-8-sig')
t=once(t,
'''            if(this.bSys.battle_stage == 25)
            {
               this.mGF.datMgr.stageSetValue("trial",5,this.mGF.datMgr.stageGetValue("trial",5) + 1);
            }
            this.mGF.datMgr.stat_total_battle += 1;
''',
'''            if(this.bSys.battle_stage == 25)
            {
               this.mGF.datMgr.stageSetValue("trial",5,this.mGF.datMgr.stageGetValue("trial",5) + 1);
            }
            if(this.bSys.battle_stage >= 26 && this.bSys.battle_stage <= 50)
            {
               var expansionStage:int = this.bSys.battle_stage - 25;
               this.mGF.datMgr.stageSetValue("expansion",expansionStage,this.mGF.datMgr.stageGetValue("expansion",expansionStage) + 1);
            }
            this.mGF.datMgr.stat_total_battle += 1;
''','expansion result persistence')
p.write_text(t,encoding='utf-8',newline='\n')

# ------------------------------------------------------------------
# WorldMap: add a dynamic 25-level Expansion campaign panel. The new campaign
# unlocks after all original 25 battles are cleared, then advances sequentially.
# ------------------------------------------------------------------
p=base/'Interface'/'WorldMap.as'; t=p.read_text(encoding='utf-8-sig')
t=once(t,
'''   import flash.display.MovieClip;
   import flash.display.SimpleButton;
''',
'''   import flash.display.MovieClip;
   import flash.display.SimpleButton;
   import flash.display.Sprite;
''','world map Sprite import')
t=once(t,
'''   import flash.net.*;
''',
'''   import flash.net.*;
   import flash.text.TextField;
   import flash.text.TextFormat;
''','world map text imports')
t=once(t,
'''      private var confirmQuit:* = null;
''',
'''      private var confirmQuit:* = null;
      
      private var expansionButton:Sprite = null;
      private var expansionPanel:Sprite = null;
      private var expansionStageButtons:Array = [];
''','expansion world map vars')
t=once(t,
'''         this.area4.buttonMode = true;
         this.area2.visible = false;
''',
'''         this.area4.buttonMode = true;
         this.expansionInstallButton();
         this.area2.visible = false;
''','install expansion map button')
t=once(t,
'''         this.link_kong.removeEventListener(MouseEvent.CLICK,this.linkKongClick);
         this.dispCont.removeChild(this);
''',
'''         this.link_kong.removeEventListener(MouseEvent.CLICK,this.linkKongClick);
         this.expansionDestroyPanel();
         if(this.expansionButton != null)
         {
            this.expansionButton.removeEventListener(MouseEvent.CLICK,this.expansionButtonClick);
            if(this.expansionButton.parent != null) this.expansionButton.parent.removeChild(this.expansionButton);
            this.expansionButton = null;
         }
         this.dispCont.removeChild(this);
''','destroy expansion map UI')

names=[
'Ashen Border','Broken Grove','Sandglass Pass','Frozen Oath','Blackwater Village',
'Ember Gate','Red Moon March','Witchwood Siege','Crypt of Kings','Tiger Shrine',
'Phoenix Fall','Valkyrie Road','Demon Foundry','Dragon Spine','Devil Crown',
'Fallen Heaven','Gaia Unbound','Baal Ascendant','Night Tiger','Archmage War',
'Colossus Keep','Twin Dragons','Hell Legion','Baal Prime','End of the Realms']
name_array=','.join('"'+x+'"' for x in names)
helpers=f'''      private function expansionInstallButton() : void
      {{
         this.expansionButton = new Sprite();
         this.expansionButton.graphics.beginFill(3937535,0.96);
         this.expansionButton.graphics.lineStyle(2,13408563,1);
         this.expansionButton.graphics.drawRoundRect(0,0,176,38,10,10);
         this.expansionButton.graphics.endFill();
         this.expansionButton.x = 568;
         this.expansionButton.y = 492;
         this.expansionButton.buttonMode = true;
         var label:TextField = new TextField();
         label.defaultTextFormat = new TextFormat("_sans",13,16777215,true,null,null,null,null,"center");
         label.width = 172; label.height = 30; label.x = 2; label.y = 8; label.mouseEnabled = false; label.selectable = false;
         label.text = this.mGF.datMgr.expansionOriginalCampaignComplete() ? "EXPANSION  0/25" : "EXPANSION  LOCKED";
         if(this.mGF.datMgr.expansionOriginalCampaignComplete())
         {{
            var cleared:int = 0; var q:int = 0;
            for(q = 1; q <= 25; q++) if(this.mGF.datMgr.stageGetValue("expansion",q) >= 1) cleared++;
            label.text = "EXPANSION  " + cleared + "/25";
         }}
         this.expansionButton.addChild(label);
         this.expansionButton.addEventListener(MouseEvent.CLICK,this.expansionButtonClick,false,0,true);
         this.addChild(this.expansionButton);
      }}
      
      private function expansionButtonClick(event:MouseEvent) : void
      {{
         if(!this.mGF.datMgr.expansionOriginalCampaignComplete())
         {{
            this.mGF.utilMgr.messagePop("Clear all 25 original battles to unlock the Expansion campaign.");
            return;
         }}
         this.expansionOpenPanel();
      }}
      
      private function expansionOpenPanel() : void
      {{
         this.expansionDestroyPanel();
         this.expansionPanel = new Sprite();
         this.expansionPanel.graphics.beginFill(657930,0.97);
         this.expansionPanel.graphics.lineStyle(2,10066329,1);
         this.expansionPanel.graphics.drawRoundRect(0,0,650,430,14,14);
         this.expansionPanel.graphics.endFill();
         this.expansionPanel.x = 55; this.expansionPanel.y = 72;
         var title:TextField = new TextField();
         title.defaultTextFormat = new TextFormat("_sans",19,16777215,true,null,null,null,null,"center");
         title.width = 620; title.height = 28; title.x = 15; title.y = 12; title.text = "EPIC WAR 5 — EXPANSION CAMPAIGN"; title.mouseEnabled = false;
         this.expansionPanel.addChild(title);
         var stageNames:Array = [{name_array}];
         var i:int = 0; var b:Sprite = null; var tx:TextField = null; var unlocked:Boolean = false;
         this.expansionStageButtons = [];
         for(i = 1; i <= 25; i++)
         {{
            unlocked = i == 1 || this.mGF.datMgr.stageGetValue("expansion",i - 1) >= 1;
            b = new Sprite();
            b.name = "expansionStage_" + i;
            b.graphics.beginFill(unlocked ? 2631720 : 1118481,0.98);
            b.graphics.lineStyle(1,unlocked ? 10066329 : 4473924,1);
            b.graphics.drawRoundRect(0,0,118,62,8,8); b.graphics.endFill();
            b.x = 20 + ((i - 1) % 5) * 124; b.y = 54 + int((i - 1) / 5) * 70;
            b.alpha = unlocked ? 1 : 0.45; b.buttonMode = unlocked;
            tx = new TextField(); tx.defaultTextFormat = new TextFormat("_sans",10,16777215,true,null,null,null,null,"center");
            tx.width = 112; tx.height = 56; tx.x = 3; tx.y = 5; tx.wordWrap = true; tx.mouseEnabled = false; tx.selectable = false;
            tx.text = String(25 + i) + ". " + String(stageNames[i - 1]) + (this.mGF.datMgr.stageGetValue("expansion",i) >= 1 ? "\nCLEARED" : (unlocked ? "\nREADY" : "\nLOCKED"));
            b.addChild(tx); b.addEventListener(MouseEvent.CLICK,this.expansionStageClick,false,0,true);
            this.expansionPanel.addChild(b); this.expansionStageButtons.push(b);
         }}
         var close:Sprite = new Sprite(); close.name = "expansionClose"; close.graphics.beginFill(6684672,1); close.graphics.drawRoundRect(0,0,110,30,8,8); close.graphics.endFill();
         close.x = 270; close.y = 394; close.buttonMode = true; close.addEventListener(MouseEvent.CLICK,this.expansionCloseClick,false,0,true);
         tx = new TextField(); tx.defaultTextFormat = new TextFormat("_sans",12,16777215,true,null,null,null,null,"center"); tx.width=106;tx.height=24;tx.x=2;tx.y=5;tx.text="CLOSE";tx.mouseEnabled=false;close.addChild(tx);
         this.expansionPanel.addChild(close); this.expansionStageButtons.push(close); this.addChild(this.expansionPanel);
      }}
      
      private function expansionStageClick(event:MouseEvent) : void
      {{
         var b:* = event.currentTarget;
         var id:int = int(String(b.name).replace("expansionStage_",""));
         if(id < 1 || id > 25) return;
         if(id > 1 && this.mGF.datMgr.stageGetValue("expansion",id - 1) < 1) return;
         var clip:* = new battle_mc();
         clip.init(this.mGF,100 + id);
         this.destroy();
      }}
      
      private function expansionCloseClick(event:MouseEvent) : void
      {{
         this.expansionDestroyPanel();
      }}
      
      private function expansionDestroyPanel() : void
      {{
         var b:* = null;
         for each(b in this.expansionStageButtons)
         {{
            if(b != null)
            {{
               b.removeEventListener(MouseEvent.CLICK,this.expansionStageClick);
               b.removeEventListener(MouseEvent.CLICK,this.expansionCloseClick);
            }}
         }}
         this.expansionStageButtons = [];
         if(this.expansionPanel != null && this.expansionPanel.parent != null) this.expansionPanel.parent.removeChild(this.expansionPanel);
         this.expansionPanel = null;
      }}
      
'''
t=once(t,'      private function formationClick(event:MouseEvent) : void\n',helpers+'      private function formationClick(event:MouseEvent) : void\n','expansion world map methods')
p.write_text(t,encoding='utf-8',newline='\n')

for rel,needles in {
    'System/Battle/BattleControlEnemy.as':['case 125:','initExpansion(25)','battle_stage = 25 + tier','exp_artlogicprime'],
    'Interface/BattleResult.as':['battle_stage >= 26 && this.bSys.battle_stage <= 50','stageSetValue("expansion",expansionStage'],
    'Interface/WorldMap.as':['EXPANSION CAMPAIGN','expansionOriginalCampaignComplete','expansionStage_','clip.init(this.mGF,100 + id)']
}.items():
    z=(base/rel).read_text(encoding='utf-8-sig')
    for n in needles:
        if n not in z: raise SystemExit(f'{rel} missing {n}')

print('Expansion V3 25-level campaign, progression panel, rewards, and enemy scaling applied')
